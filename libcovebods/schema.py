import json
from typing import Optional
from urllib.parse import urlparse

from libcove2.common import schema_dict_fields_generator  # type: ignore
from packaging import version as packaging_version

import libcovebods.data_reader
from libcovebods.config import LibCoveBODSConfig

try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property  # type: ignore


class SchemaBODS:
    def __init__(
        self,
        data_reader: Optional[libcovebods.data_reader.DataReader] = None,
        lib_cove_bods_config=None,
    ):
        self.config = lib_cove_bods_config or LibCoveBODSConfig()
        # Information about this schema
        # ... what version the data tried to set (used later to check for inconsistent statements)
        self.schema_version_attempted = None
        # ... what version we actually use
        self.schema_version = None
        # ... resources for the version we are actually using
        self.pkg_schema_url = None
        self.schema_host = None
        # ... any error encountered when working out the version
        self.schema_error: Optional[dict] = None
        # Now try to work out version from information passed
        self.__work_out_schema_version(data_reader)

    def __work_out_schema_version(
        self, data_reader: Optional[libcovebods.data_reader.DataReader] = None
    ):

        # If no data is passed, then we assume it's the default version
        if not data_reader:
            self.pkg_schema_url = self.config.config["schema_url"]
            self.schema_host = self.config.config["schema_url_host"]
            self.schema_version_attempted = self.config.config["schema_version"]
            self.schema_version = self.config.config["schema_version"]
            return

        # If bad data passed, then we assume it's the default version
        all_data = data_reader.get_all_data()
        if not isinstance(all_data, list) or len(all_data) == 0:
            self.pkg_schema_url = self.config.config["schema_url"]
            self.schema_host = self.config.config["schema_url_host"]
            self.schema_version_attempted = self.config.config["schema_version"]
            self.schema_version = self.config.config["schema_version"]
            return

        # We look at the first statement to try to find a version
        statement = all_data[0]

        # If version is not set at all, then we assume it's the default version
        if (
            not isinstance(statement, dict)
            or "publicationDetails" not in statement
            or not isinstance(statement["publicationDetails"], dict)
            or "bodsVersion" not in statement["publicationDetails"]
        ):
            self.pkg_schema_url = self.config.config["schema_url"]
            self.schema_host = self.config.config["schema_url_host"]
            self.schema_version_attempted = self.config.config["schema_version"]
            self.schema_version = self.config.config["schema_version"]
            return

        # The statement is trying to set a version
        self.schema_version_attempted = statement["publicationDetails"]["bodsVersion"]

        # A specified schema version must be a string
        if not isinstance(self.schema_version_attempted, str):
            # Return latest version, but with an error!
            self.schema_error = {
                "type": "unknown_schema_version_used",
                "schema_version": str(self.schema_version_attempted),
            }
            self.schema_version = self.config.config["schema_latest_version"]
            self.pkg_schema_url = self.config.config["schema_versions"][
                self.schema_version
            ]["schema_url"]
            self.schema_host = self.config.config["schema_versions"][
                self.schema_version
            ]["schema_url_host"]
            return

        # The statement tries to specify a version which is not known.
        if self.schema_version_attempted not in self.config.config["schema_versions"]:
            # Return latest version, but with an error!
            self.schema_error = {
                "type": "unknown_schema_version_used",
                "schema_version": self.schema_version_attempted,
            }
            self.schema_version = self.config.config["schema_latest_version"]
            self.pkg_schema_url = self.config.config["schema_versions"][
                self.schema_version
            ]["schema_url"]
            self.schema_host = self.config.config["schema_versions"][
                self.schema_version
            ]["schema_url_host"]
            return

        # All checks passed - We have found a specified schema version!
        self.schema_version = self.schema_version_attempted
        self.pkg_schema_url = self.config.config["schema_versions"][
            self.schema_version
        ]["schema_url"]
        self.schema_host = self.config.config["schema_versions"][self.schema_version][
            "schema_url_host"
        ]

    def get_entity_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj["items"]["oneOf"]:
            if (
                statement_schema["properties"]["statementType"]["enum"][0]
                == "entityStatement"
            ):
                return statement_schema["properties"]["entityType"]["enum"]

    def get_person_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj["items"]["oneOf"]:
            if (
                statement_schema["properties"]["statementType"]["enum"][0]
                == "personStatement"
            ):
                return statement_schema["properties"]["personType"]["enum"]

    def get_ownership_or_control_statement_interest_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj["items"]["oneOf"]:
            if (
                statement_schema["properties"]["statementType"]["enum"][0]
                == "ownershipOrControlStatement"
            ):
                return statement_schema["properties"]["interests"]["items"][
                    "properties"
                ]["type"]["enum"]

    def get_ownership_or_control_statement_interest_direct_or_indirect_list(self):
        for statement_schema in self._pkg_schema_obj["items"]["oneOf"]:
            if (
                statement_schema["properties"]["statementType"]["enum"][0]
                == "ownershipOrControlStatement"
            ):
                direct_or_indirect_json_schema = statement_schema["properties"][
                    "interests"
                ]["items"]["properties"].get("directOrIndirect")
                # This is only available in 0.3 and above.
                if isinstance(direct_or_indirect_json_schema, dict):
                    return direct_or_indirect_json_schema.get("enum")
                else:
                    return []

    def get_person_statement_political_exposure_status_list(self):
        for statement_schema in self._pkg_schema_obj["items"]["oneOf"]:
            if (
                statement_schema["properties"]["statementType"]["enum"][0]
                == "personStatement"
            ):
                political_exposure_schema = statement_schema["properties"].get(
                    "politicalExposure"
                )
                # This is only available in 0.3 and above.
                if isinstance(political_exposure_schema, dict):
                    return political_exposure_schema["properties"]["status"]["enum"]
                else:
                    return []

    def get_inconsistent_schema_version_used_for_statement(self, statement):
        # If version is not set at all, then we assume it's the default version
        if (
            not isinstance(statement, dict)
            or "publicationDetails" not in statement
            or not isinstance(statement["publicationDetails"], dict)
            or "bodsVersion" not in statement["publicationDetails"]
        ):
            schema_version_attempted = self.config.config["schema_version"]
        # Or take the version from the statement
        else:
            schema_version_attempted = statement["publicationDetails"]["bodsVersion"]

        # Are versions inconsistent
        if schema_version_attempted != self.schema_version_attempted:
            return True, str(schema_version_attempted)
        else:
            return False, None

    def get_address_types_allowed_in_entity_statement(self):
        return ("registered", "business", "alternative")

    def get_address_types_allowed_in_person_statement(self):
        return ("placeOfBirth", "residence", "service", "alternative")

    def is_schema_version_equal_to_or_greater_than(self, version):
        return packaging_version.parse(self.schema_version) >= packaging_version.parse(
            version
        )

    def get_package_schema_fields(self) -> set:
        return set(schema_dict_fields_generator(self._pkg_schema_obj))

    @cached_property
    def pkg_schema_str(self):
        uri_scheme = urlparse(self.pkg_schema_url).scheme
        if uri_scheme == "http" or uri_scheme == "https":
            raise NotImplementedError(
                "Downloading schema files over HTTP/HTTPS is not supported"
            )
        else:
            with open(self.pkg_schema_url) as fp:
                return fp.read()

    @property
    def _pkg_schema_obj(self):
        return json.loads(self.pkg_schema_str)
