import re
import os
import datetime
import requests
from tempfile import NamedTemporaryFile
import json


LANGUAGE_RE = re.compile(
    "^(.*_(((([A-Za-z]{2,3}(-([A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-([A-Za-z]{4}))?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-([0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(x(-[A-Za-z0-9]{1,8})+))?)|(x(-[A-Za-z0-9]{1,8})+)))$"
)


def schema_dict_fields_generator(schema_dict):
    if "properties" in schema_dict and isinstance(schema_dict["properties"], dict):
        for property_name, value in schema_dict["properties"].items():
            if "oneOf" in value:
                property_schema_dicts = value["oneOf"]
            else:
                property_schema_dicts = [value]
            for property_schema_dict in property_schema_dicts:
                if not isinstance(property_schema_dict, dict):
                    continue
                if "properties" in property_schema_dict:
                    for field in schema_dict_fields_generator(property_schema_dict):
                        yield f"/{property_name}{field}"
                elif "items" in property_schema_dict:
                    for field in schema_dict_fields_generator(
                        property_schema_dict["items"]
                    ):
                        yield f"/{property_name}{field}"
                yield f"/{property_name}"
    if "items" in schema_dict and isinstance(schema_dict["items"], dict):
        if "oneOf" in schema_dict["items"] and isinstance(
            schema_dict["items"]["oneOf"], list
        ):
            for oneOf in schema_dict["items"]["oneOf"]:
                for field in schema_dict_fields_generator(oneOf):
                    yield field


def get_additional_fields_info(json_data, schema_fields, fields_regex=False):
    fields_present = get_fields_present_with_examples(json_data)

    additional_fields = {}
    root_additional_fields = set()

    for field, field_info in fields_present.items():

        if field in schema_fields:
            continue
        if fields_regex and LANGUAGE_RE.search(field.split("/")[-1]):
            continue

        for root_additional_field in root_additional_fields:
            if field.startswith(root_additional_field):
                field_info["root_additional_field"] = False
                additional_fields[root_additional_field][
                    "additional_field_descendance"
                ][field] = field_info
                break
        else:
            field_info["root_additional_field"] = True
            field_info["additional_field_descendance"] = {}
            root_additional_fields.add(field)

        field_info["path"] = "/".join(field.split("/")[:-1])
        field_info["field_name"] = field.split("/")[-1]
        additional_fields[field] = field_info

    return additional_fields


def get_fields_present_with_examples(*args, **kwargs):
    counter = {}
    for key, value in fields_present_generator(*args, **kwargs):
        if key not in counter:
            counter[key] = {"count": 1, "examples": []}
        else:
            counter[key]["count"] += 1
        if len(counter[key]["examples"]) < 3:
            if not isinstance(value, (list, dict)):
                counter[key]["examples"].append(value)

    return counter


def fields_present_generator(json_data, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = f"{prefix}/{key}"
            yield new_key, value
            if isinstance(value, (dict, list)):
                yield from fields_present_generator(value, new_key)
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                yield from fields_present_generator(item, prefix)

def org_id_file_fresh(org_id_file_contents, check_date):
    """Unless the file was downloaded on greater than or equal to 'check_date' it is considered stale."""
    org_id_file_date_downloaded_date = datetime.datetime.strptime(
        org_id_file_contents.get("downloaded", "2000-1-1"), "%Y-%m-%d"
    ).date()
    return org_id_file_date_downloaded_date >= check_date

def get_orgids_prefixes(orgids_url=None):
    """Get org-ids.json file from file system (or fetch remotely if it doesn't exist)"""
    local_org_ids_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "org-ids.json"
    )
    today = datetime.date.today()
    if orgids_url is None:
        orgids_url = "http://org-id.guide/download.json"
    org_id_file_contents = None

    # Try to grab the data from the local filesystem
    try:
        with open(local_org_ids_file) as fp:
            org_id_file_contents = json.load(fp)
    except FileNotFoundError:
        pass

    if org_id_file_contents is None or not org_id_file_fresh(
        org_id_file_contents, today
    ):
        # Refresh the file
        try:
            org_id_file_contents = requests.get(orgids_url).json()
        except requests.exceptions.RequestException as e:
            # We have tried locally and remotely with no luck. We have to raise.
            raise e

        org_id_file_contents["downloaded"] = "%s" % today
        # Use a tempfile and move to create new file here for atomicity
        with NamedTemporaryFile(mode="w", delete=False) as tmp:
            json.dump(org_id_file_contents, tmp, indent=2)
        os.rename(tmp.name, local_org_ids_file)
    # Return either the original file data, if it was found to be fresh, or the new data, if we were able to retrieve it.
    return [org_list["code"] for org_list in org_id_file_contents["lists"]]