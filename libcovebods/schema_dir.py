import json
from pathlib import Path

from jscc.schema import is_json_schema  # type: ignore
from jscc.testing.filesystem import walk_json_data  # type: ignore
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


def get_schema_paths(schema_dir):
    """
    Returns an array of paths, filenames, and contents (parsed JSON) for each of the schema files.
    """
    schema_paths = [
        (path, name, data)
        for path, name, _, data in walk_json_data(top=schema_dir)
        if is_json_schema(data)
    ]
    return schema_paths


def schema_registry(schema_dir):
    """
    This loads the BODS schema files into a jsonschema registry, so the
    validator can resolve $refs across all of the schema files.
    """
    schemas = []
    for _, _, schema in get_schema_paths(schema_dir):
        schemas.append(
            (schema.get("$id"), Resource(contents=schema, specification=DRAFT202012))
        )

    registry = Registry().with_resources(schemas)
    return registry


def get_scheme_file_data(schema_dir, component):
    for file_path in Path(schema_dir).glob("*.json"):
        if file_path.name.startswith(component):
            with open(file_path) as json_file:
                return json.load(json_file)
