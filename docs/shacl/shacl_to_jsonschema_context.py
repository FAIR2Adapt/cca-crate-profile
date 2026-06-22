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


def make_property_schema(node_kind, title=None, class_iri=None):
    prop = {"type": "string"}

    if title:
        prop["title"] = title

    if node_kind == SH.IRI:
        prop["format"] = "uri"

    if class_iri:
        prop["description"] = f"Expected RDF class: {class_iri}"

    return prop


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


def shape_def_name(g, shape, target_class, target_node):
    name = get_literal(g, shape, SH.name)

    if name:
        return "".join(c for c in name if c.isalnum())

    if target_class:
        return local_name(target_class)

    if target_node:
        return "RootDataEntity"

    return local_name(shape)


def is_root_target_node(shape_graph, shape):
    """
    RDFLib resolves <./> against the Turtle file base, so after parsing we
    cannot reliably recover the lexical './'. For this RO-Crate profile, any
    shape using sh:targetNode and no sh:targetClass is treated as the root
    data entity shape and emitted as '@id': './'.
    """
    return (
        shape_graph.value(shape, SH.targetNode) is not None
        and shape_graph.value(shape, SH.targetClass) is None
    )


def convert(shacl_file, context_ref):
    g = Graph()
    g.parse(shacl_file, format="turtle")

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://w3id.org/ro/terms/cca/schema/json-schema",
        "title": "CCA RO-Crate profile JSON Schema",
        "type": "object",
        "$comment": "JSON property names are fully expanded IRIs derived from SHACL sh:path. The JSON-LD context is provided separately for compact JSON-LD usage.",
        "x-jsonld-context": context_ref,
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
            class_iri = g.value(prop_shape, SH["class"])

            if len(paths) == 1:
                path = paths[0]
                key = str(path)

                obj_schema["properties"][key] = make_property_schema(
                    node_kind=node_kind,
                    title=label,
                    class_iri=str(class_iri) if class_iri else None
                )

                add_context(context, path, node_kind)

                if min_count and int(min_count) >= 1:
                    obj_schema["required"].append(key)

            else:
                one_of = []

                for path in paths:
                    key = str(path)

                    obj_schema["properties"][key] = make_property_schema(
                        node_kind=node_kind,
                        title=label,
                        class_iri=str(class_iri) if class_iri else None
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

    schema_file.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")
    context_file.write_text(json.dumps(context, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {schema_file}")
    print(f"Wrote {context_file}")


if __name__ == "__main__":
    main()