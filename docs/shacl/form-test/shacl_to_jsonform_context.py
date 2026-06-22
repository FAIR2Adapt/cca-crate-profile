#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

from rdflib import Graph, RDF, SH, URIRef, BNode


PREFIXES = {
    "schema": "https://schema.org/",
    "cca": "https://w3id.org/ro/terms/cca/",
    "dct": "http://purl.org/dc/terms/",
    "dpv": "https://w3id.org/dpv#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "iadopt": "https://w3id.org/iadopt/ont/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "tech": "https://w3id.org/dpv/tech#",
    "citedcat": "https://w3id.org/citedcat-ap/",
    "geodcat": "http://data.europa.eu/930/",
    "fabio": "http://purl.org/spar/fabio/",
    "adms": "http://www.w3.org/ns/adms#",
    "dcso": "https://w3id.org/dcso/ns/core#",
    "bibo": "http://purl.org/ontology/bibo/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
}


def local_name(uri):
    s = str(uri)
    return s.rstrip("/#").split("/")[-1].split("#")[-1]


def clean_key(value):
    value = local_name(value)
    value = re.sub(r"[^A-Za-z0-9_]", "_", value)
    return value[:1].lower() + value[1:] if value else "value"


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


def is_root_shape(g, shape):
    return (
        g.value(shape, SH.targetNode) is not None
        and g.value(shape, SH.targetClass) is None
    )


def shape_def_name(g, shape, target_class=None, target_node=None):
    name = get_literal(g, shape, SH.name)

    if name:
        return "".join(c for c in name if c.isalnum())

    if target_class:
        return local_name(target_class)

    if target_node:
        return "RootDataEntity"

    return local_name(shape)


def build_class_to_def_map(g):
    out = {}

    for shape in g.subjects(RDF.type, SH.NodeShape):
        target_class = g.value(shape, SH.targetClass)
        target_node = g.value(shape, SH.targetNode)

        if target_class:
            out[str(target_class)] = shape_def_name(g, shape, target_class, target_node)

    return out


def add_context(context, key, path_iri, node_kind):
    if node_kind == SH.IRI:
        context["@context"][key] = {
            "@id": str(path_iri),
            "@type": "@id"
        }
    else:
        context["@context"][key] = str(path_iri)


def id_schema(title="@id"):
    return {
        "type": "string",
        "title": title
    }


def type_schema(class_iri):
    return {
        "type": "string",
        "title": "@type",
        "enum": [str(class_iri)]
    }


def object_ref_schema(title, class_iri=None, def_name=None):
    """
    JSONForm handles simple object refs better than $ref-heavy nested structures.
    Keep @id/@type fields explicit, and optionally allow additional fields.
    """
    props = {
        "id": id_schema("@id")
    }

    required = ["id"]

    if class_iri:
        props["type"] = type_schema(class_iri)

    schema = {
        "type": "object",
        "title": title,
        "properties": props,
        "required": required,
        "additionalProperties": True
    }

    # Draft-04-compatible optional link to the full definition.
    # JSONForm normally ignores this, but validators can use it if supported.
    if def_name:
        schema["description"] = f"Reference to {def_name}"

    return schema


def literal_schema(title):
    return {
        "type": "string",
        "title": title or "Value"
    }


def read_or_classes(g, prop_shape):
    head = g.value(prop_shape, SH["or"])
    if not head:
        return []

    classes = []

    for item in rdf_list(g, head):
        cls = g.value(item, SH["class"])
        if cls:
            classes.append(cls)

    return classes


def make_property_schema(g, prop_shape, node_kind, title, class_to_def):
    class_iri = g.value(prop_shape, SH["class"])
    or_classes = read_or_classes(g, prop_shape)

    if or_classes:
        # JSONForm has limited oneOf support, so expose a simple reference object
        # and show allowed types as enum.
        return {
            "type": "object",
            "title": title,
            "properties": {
                "id": id_schema("@id"),
                "type": {
                    "type": "string",
                    "title": "@type",
                    "enum": [str(c) for c in or_classes]
                }
            },
            "required": ["id"],
            "additionalProperties": True
        }

    if node_kind == SH.IRI:
        def_name = class_to_def.get(str(class_iri)) if class_iri else None
        return object_ref_schema(title, class_iri, def_name)

    return literal_schema(title)


def convert_shape(g, shape, class_to_def, context):
    target_class = g.value(shape, SH.targetClass)
    target_node = g.value(shape, SH.targetNode)

    def_name = shape_def_name(g, shape, target_class, target_node)

    obj_schema = {
        "type": "object",
        "title": get_literal(g, shape, SH.name, def_name),
        "properties": {
            "id": id_schema("@id")
        },
        "required": ["id"],
        "additionalProperties": True
    }

    form_items = ["id"]

    if is_root_shape(g, shape):
        obj_schema["properties"]["id"]["enum"] = ["./"]

    elif target_class:
        obj_schema["properties"]["type"] = type_schema(target_class)
        obj_schema["required"].append("type")
        form_items.append("type")

    for prop_shape in g.objects(shape, SH.property):
        paths = get_path_iris(g, prop_shape)
        if not paths:
            continue

        label = get_literal(g, prop_shape, SH.name)
        node_kind = g.value(prop_shape, SH.nodeKind)
        min_count = g.value(prop_shape, SH.minCount)

        for path in paths:
            key = clean_key(path)

            # Avoid collision with id/type
            if key in ("id", "type"):
                key = f"{key}_value"

            obj_schema["properties"][key] = make_property_schema(
                g=g,
                prop_shape=prop_shape,
                node_kind=node_kind,
                title=label or key,
                class_to_def=class_to_def
            )

            if min_count and int(min_count) >= 1:
                obj_schema["required"].append(key)

            add_context(context, key, path, node_kind)

            if node_kind == SH.IRI:
                items = [f"{key}.id"]
                if "type" in obj_schema["properties"][key].get("properties", {}):
                    items.append(f"{key}.type")

                form_items.append({
                    "type": "fieldset",
                    "title": label or key,
                    "items": items
                })
            else:
                form_items.append(key)

    return def_name, obj_schema, form_items


def convert(shacl_file):
    g = Graph()
    g.parse(shacl_file, format="turtle")

    class_to_def = build_class_to_def_map(g)

    context = {
        "@context": {
            "id": "@id",
            "type": "@type",
            **PREFIXES
        }
    }

    definitions = {}
    forms = {}
    root_def = None

    for shape in g.subjects(RDF.type, SH.NodeShape):
        target_class = g.value(shape, SH.targetClass)
        target_node = g.value(shape, SH.targetNode)

        if not target_class and not target_node:
            continue

        def_name, schema_def, form_items = convert_shape(
            g=g,
            shape=shape,
            class_to_def=class_to_def,
            context=context
        )

        definitions[def_name] = schema_def
        forms[def_name] = form_items

        if is_root_shape(g, shape):
            root_def = def_name

    if not root_def:
        raise RuntimeError("No root shape found with sh:targetNode <./>")

    root_schema = definitions[root_def].copy()
    root_schema["$schema"] = "http://json-schema.org/draft-04/schema#"
    root_schema["title"] = "CCA RO-Crate Profile"
    root_schema["definitions"] = definitions

    jsonform = {
        "schema": root_schema,
        "form": forms[root_def]
    }

    return jsonform, context


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python shacl_to_jsonform_context.py "
            "cca-profile-shacl.ttl cca-profile.schema-form.json cca-profile.context.jsonld"
        )
        sys.exit(1)

    shacl_file = Path(sys.argv[1])
    form_file = Path(sys.argv[2])
    context_file = Path(sys.argv[3])

    jsonform, context = convert(shacl_file)

    form_file.write_text(
        json.dumps(jsonform, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    context_file.write_text(
        json.dumps(context, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Wrote {form_file}")
    print(f"Wrote {context_file}")


if __name__ == "__main__":
    main()