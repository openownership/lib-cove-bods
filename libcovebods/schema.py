from libcove.lib.common import SchemaJsonMixin


class SchemaBODS(SchemaJsonMixin):

    def __init__(self, json_data=None, lib_cove_bods_config=None):
        self.config = lib_cove_bods_config
        # Information about this schema
        # ... what version the data tried to set (used later to check for inconsistent statements)
        self.schema_version_attempted = None
        # ... what version we actually use
        self.schema_version = None
        # ... resources for the version we are actually using
        self.pkg_schema_url = None
        self.schema_host = None
        # ... any error encountered when working out the version
        self.schema_error = None
        # Now try to work out version from information passed
        self.__work_out_schema_version(json_data)

    def __work_out_schema_version(self, json_data=None):

        # If no data is passed, then we assume it's the default version
        if not isinstance(json_data, list) or len(json_data) == 0:
            self.pkg_schema_url = self.config.config['schema_url']
            self.schema_host = self.config.config['schema_url_host']
            self.schema_version_attempted = self.config.config['schema_version']
            self.schema_version = self.config.config['schema_version']
            return

        # We look at the first statement to try to find a version
        statement = json_data[0]

        # If version is not set at all, then we assume it's the default version
        if not isinstance(statement, dict) \
                or 'publicationDetails' not in statement \
                or not isinstance(statement['publicationDetails'], dict) \
                or 'bodsVersion' not in statement['publicationDetails']:
            self.pkg_schema_url = self.config.config['schema_url']
            self.schema_host = self.config.config['schema_url_host']
            self.schema_version_attempted = self.config.config['schema_version']
            self.schema_version = self.config.config['schema_version']
            return

        # The statement is trying to set a version
        self.schema_version_attempted = statement['publicationDetails']['bodsVersion']

        # A specified schema version must be a string
        if not isinstance(self.schema_version_attempted, str):
            # Return latest version, but with an error!
            self.schema_error = {
                'type': 'unknown_schema_version_used',
                'schema_version': str(self.schema_version_attempted),
            }
            self.schema_version = self.config.config['schema_latest_version']
            self.pkg_schema_url = self.config.config['schema_versions'][self.schema_version]['schema_url']
            self.schema_host = self.config.config['schema_versions'][self.schema_version]['schema_url_host']
            return

        # The statement tries to specify a version which is not known.
        if self.schema_version_attempted not in self.config.config['schema_versions']:
            # Return latest version, but with an error!
            self.schema_error = {
                'type': 'unknown_schema_version_used',
                'schema_version': self.schema_version_attempted,
            }
            self.schema_version = self.config.config['schema_latest_version']
            self.pkg_schema_url = self.config.config['schema_versions'][self.schema_version]['schema_url']
            self.schema_host = self.config.config['schema_versions'][self.schema_version]['schema_url_host']
            return

        # All checks passed - We have found a specified schema version!
        self.schema_version = self.schema_version_attempted
        self.pkg_schema_url = self.config.config['schema_versions'][self.schema_version]['schema_url']
        self.schema_host = self.config.config['schema_versions'][self.schema_version]['schema_url_host']

    def get_entity_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'entityStatement':
                return statement_schema['properties']['entityType']['enum']

    def get_person_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'personStatement':
                return statement_schema['properties']['personType']['enum']

    def get_ownership_or_control_statement_interest_statement_types_list(self):
        for statement_schema in self._pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'ownershipOrControlStatement':
                return statement_schema['properties']['interests']['items']['properties']['type']['enum']

    def get_inconsistent_schema_version_used_for_statement(self, statement):
        # If version is not set at all, then we assume it's the default version
        if not isinstance(statement, dict) \
                or 'publicationDetails' not in statement \
                or not isinstance(statement['publicationDetails'], dict) \
                or 'bodsVersion' not in statement['publicationDetails']:
            schema_version_attempted = self.config.config['schema_version']
        # Or take the version from the statement
        else:
            schema_version_attempted = statement['publicationDetails']['bodsVersion']

        # Are versions inconsistent
        if schema_version_attempted != self.schema_version_attempted:
            return True, str(schema_version_attempted)
        else:
            return False, None

    def get_address_types_allowed_in_entity_statement(self):
        return ('registered', 'business', 'alternative')

    def get_address_types_allowed_in_person_statement(self):
        return ('placeOfBirth', 'residence', 'service', 'alternative')
