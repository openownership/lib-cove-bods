from libcove.lib.common import SchemaJsonMixin


class SchemaBODS(SchemaJsonMixin):

    def __init__(self, json_data=None, lib_cove_bods_config=None):
        self.config = lib_cove_bods_config
        if isinstance(json_data, list) and len(json_data) > 0:
            self.schema_version, self.pkg_schema_url, self.schema_host = \
                self.get_schema_version_of_statement(json_data[0])
        else:
            self.pkg_schema_url = self.config.config['schema_url']
            self.schema_host = self.config.config['schema_url_host']
            self.schema_version = self.config.config['schema_version']

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

    def get_schema_version_of_statement(self, statement):
        #  Does the data specify a version?
        if isinstance(statement, dict) \
                and 'publicationDetails' in statement \
                and isinstance(statement['publicationDetails'], dict) \
                and 'bodsVersion' in statement['publicationDetails'] \
                and statement['publicationDetails']['bodsVersion']:
            version = statement['publicationDetails']['bodsVersion']
            if version in self.config.config['schema_versions']:
                return version, self.config.config['schema_versions'][version]['schema_url'], \
                       self.config.config['schema_versions'][version]['schema_url_host']

        # In which case, default schema
        return self.config.config['schema_version'], self.config.config['schema_url'], \
            self.config.config['schema_version']

    def get_address_types_allowed_in_entity_statement(self):
        return ('registered', 'business', 'alternative')

    def get_address_types_allowed_in_person_statement(self):
        return ('placeOfBirth', 'residence', 'service', 'alternative')
