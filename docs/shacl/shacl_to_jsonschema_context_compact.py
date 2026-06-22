#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from rdflib import Graph, RDF, SH, URIRef, BNode


PREFIXES = {
    "adms": "http://www.w3.org/ns/adms#",
    "bibo": "http://purl.org/ontology/bibo/",
    "citedcat": "https://w3id.org/citedcat-ap/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcso": "https://w3id.org/dcso/ns/core#",
    "dct": "http://purl.org/dc/terms/",
    "dpv": "https://w3id.org/dpv#",
    "fabio": "http://purl.org/spar/fabio/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "iadopt": "https://w3id.org/iadopt/ont/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "sosa": "http://www.w3.org/ns/sosa/",
    "tech": "https://w3id.org/dpv/tech#",
    "geodcat": "http://data.europa.eu/930/",
    "schema": "https://schema.org/",
    "cca": "https://w3id.org/ro/terms/cca/",
}


def dumps_compact_json(value, indent=2, current=0):
    """
    Pretty-print JSON while keeping small primitive arrays/objects inline.

    This keeps generated JSON Schema readable but avoids excessive vertical
    expansion for constructs such as:
      "required": ["@id"]
      "@id": { "type": "string" }
      "@type": { "const": "https://schema.org/Dataset" }

    The output is valid JSON and preserves the schema structure unchanged.
    """
    space = " " * current
    next_space = " " * (current + indent)

    def is_primitive(x):
        return x is None or isinstance(x, (str, int, float, bool))

    def is_inline_list(x):
        return isinstance(x, list) and all(is_primitive(i) for i in x)

    def is_inline_dict(x):
        return (
            isinstance(x, dict)
            and len(x) <= 3
            and all(is_primitive(v) for v in x.values())
        )

    if is_primitive(value):
        return json.dumps(value, ensure_ascii=False)

    if is_inline_list(value):
        return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in value) + "]"

    if is_inline_dict(value):
        items = [
            json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
            for k, v in value.items()
        ]
        return "{ " + ", ".join(items) + " }"

    if isinstance(value, list):
        if not value:
            return "[]"
        rendered = [
            next_space + dumps_compact_json(item, indent, current + indent)
            for item in value
        ]
        return "[\n" + ",\n".join(rendered) + "\n" + space + "]"

    if isinstance(value, dict):
        if not value:
            return "{}"
        rendered = []
        for k, v in value.items():
            rendered.append(
                next_space
                + json.dumps(k, ensure_ascii=False)
                + ": "
                + dumps_compact_json(v, indent, current + indent)
            )
        return "{\n" + ",\n".join(rendered) + "\n" + space + "}"

    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def local_name(uri):
    s = str(uri)
    return s.rstrip("/#").split("/")[-1].split("#")[-1]


def get_literal(g, s, p, default=None):
    v = g.value(s, p)
    return str(v) if v else default


def rdf_list(g, head):
    items = []
    while head and head != RDF.nil:
        first = g.value(head, RDF.first)
        rest = g.value(head, RDF.rest)
        if first:
            items.append(first)
        head = rest
    return items


def get_path_iris(g, prop_shape):
    path = g.value(prop_shape, SH.path)

    if isinstance(path, URIRef):
        return [path]

    if isinstance(path, BNode):
        alt = g.value(path, SH.alternativePath)
        if alt:
            return [p for p in rdf_list(g, alt) if isinstance(p, URIRef)]

    return []


def shape_def_name(g, shape, target_class, target_node):
    name = get_literal(g, shape, SH.name)

    if name:
        return "".join(c for c in name if c.isalnum())

    if target_class:
        return local_name(target_class)

    if target_node:
        return "RootDataEntity"

    return local_name(shape)


def is_root_target_node(g, shape):
    return (
        g.value(shape, SH.targetNode) is not None
        and g.value(shape, SH.targetClass) is None
    )


def class_to_def_name(class_iri, class_to_def):
    return class_to_def.get(str(class_iri))


def reference_or_embedded_object(class_iri, class_to_def):
    """
    RO-Crate normally links entities by {"@id": "..."} in @graph.
    This allows either:
    - a lightweight reference with @id and optional @type
    - a fully embedded object conforming to the matching $defs entry, if known
    """
    iri = str(class_iri)
    def_name = class_to_def_name(class_iri, class_to_def)

    ref_object = {
        "type": "object",
        "required": ["@id"],
        "properties": {
            "@id": {"type": "string"},
            "@type": {"const": iri}
        },
        "additionalProperties": True
    }

    if def_name:
        return {
            "oneOf": [
                ref_object,
                {"$ref": f"#/$defs/{def_name}"}
            ]
        }

    return ref_object


def literal_schema(title=None):
    schema = {"type": "string"}
    if title:
        schema["title"] = title
    return schema


def iri_schema(title=None):
    schema = {
        "type": "object",
        "required": ["@id"],
        "properties": {
            "@id": {"type": "string"}
        },
        "additionalProperties": True
    }
    if title:
        schema["title"] = title
    return schema


def read_or_class_ranges(g, node):
    or_head = g.value(node, SH["or"])
    if not or_head:
        return []

    classes = []
    for item in rdf_list(g, or_head):
        cls = g.value(item, SH["class"])
        if cls:
            classes.append(cls)

    return classes


def make_property_schema(g, prop_shape, node_kind, title, class_to_def):
    class_iri = g.value(prop_shape, SH["class"])
    or_classes = read_or_class_ranges(g, prop_shape)

    if or_classes:
        variants = [
            reference_or_embedded_object(cls, class_to_def)
            for cls in or_classes
        ]
        return {
            "title": title,
            "oneOf": variants
        }

    if class_iri:
        schema = reference_or_embedded_object(class_iri, class_to_def)
        if title:
            schema["title"] = title
        return schema

    if node_kind == SH.IRI:
        return iri_schema(title)

    return literal_schema(title)


def add_context(context, path_iri, node_kind):
    alias = local_name(path_iri)

    if alias in context["@context"]:
        alias = str(path_iri)

    if node_kind == SH.IRI:
        context["@context"][alias] = {
            "@id": str(path_iri),
            "@type": "@id"
        }
    else:
        context["@context"][alias] = str(path_iri)


def build_class_to_def_map(g):
    class_to_def = {}

    for shape in g.subjects(RDF.type, SH.NodeShape):
        target_class = g.value(shape, SH.targetClass)
        target_node = g.value(shape, SH.targetNode)

        if target_class:
            def_name = shape_def_name(g, shape, target_class, target_node)
            class_to_def[str(target_class)] = def_name

    return class_to_def


def convert(shacl_file, context_ref):
    g = Graph()
    g.parse(shacl_file, format="turtle")

    class_to_def = build_class_to_def_map(g)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://w3id.org/ro/terms/cca/schema/json-schema",
        "title": "CCA RO-Crate profile JSON Schema",
        "type": "object",
        "$comment": (
            "JSON property names are fully expanded IRIs derived from SHACL sh:path. "
            "Object-property ranges are represented using standard JSON Schema "
            "keywords: type, required, properties, const, oneOf and $ref. "
            "The JSON-LD context is generated separately for compact JSON-LD usage."
        ),
        "$defs": {}
    }

    context = {
        "@context": dict(PREFIXES)
    }

    for shape in g.subjects(RDF.type, SH.NodeShape):
        target_class = g.value(shape, SH.targetClass)
        target_node = g.value(shape, SH.targetNode)

        if not target_class and not target_node:
            continue

        def_name = shape_def_name(g, shape, target_class, target_node)

        obj_schema = {
            "title": get_literal(g, shape, SH.name, def_name),
            "type": "object",
            "properties": {
                "@id": {"type": "string"}
            },
            "required": ["@id"],
            "additionalProperties": True
        }

        if target_class:
            obj_schema["properties"]["@type"] = {
                "const": str(target_class)
            }
            obj_schema["required"].append("@type")

        if is_root_target_node(g, shape):
            obj_schema["properties"]["@id"] = {
                "const": "./"
            }
        elif target_node:
            obj_schema["properties"]["@id"] = {
                "const": str(target_node)
            }

        for prop_shape in g.objects(shape, SH.property):
            paths = get_path_iris(g, prop_shape)
            if not paths:
                continue

            label = get_literal(g, prop_shape, SH.name)
            node_kind = g.value(prop_shape, SH.nodeKind)
            min_count = g.value(prop_shape, SH.minCount)

            if len(paths) == 1:
                path = paths[0]
                key = str(path)

                obj_schema["properties"][key] = make_property_schema(
                    g=g,
                    prop_shape=prop_shape,
                    node_kind=node_kind,
                    title=label,
                    class_to_def=class_to_def
                )

                add_context(context, path, node_kind)

                if min_count and int(min_count) >= 1:
                    obj_schema["required"].append(key)

            else:
                one_of = []

                for path in paths:
                    key = str(path)

                    obj_schema["properties"][key] = make_property_schema(
                        g=g,
                        prop_shape=prop_shape,
                        node_kind=node_kind,
                        title=label,
                        class_to_def=class_to_def
                    )

                    add_context(context, path, node_kind)
                    one_of.append({"required": [key]})

                obj_schema.setdefault("oneOf", []).extend(one_of)

        schema["$defs"][def_name] = obj_schema

    return schema, context


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python shacl_to_jsonschema_context.py "
            "cca-profile-shacl.ttl cca-profile.schema.json cca-profile.context.jsonld"
        )
        sys.exit(1)

    shacl_file = Path(sys.argv[1])
    schema_file = Path(sys.argv[2])
    context_file = Path(sys.argv[3])

    schema, context = convert(shacl_file, context_file.name)

    schema_file.write_text(
        dumps_compact_json(schema, indent=2),
        encoding="utf-8"
    )
    context_file.write_text(
        dumps_compact_json(context, indent=2),
        encoding="utf-8"
    )

    print(f"Wrote {schema_file}")
    print(f"Wrote {context_file}")


if __name__ == "__main__":
    main()