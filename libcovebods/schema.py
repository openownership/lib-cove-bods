from libcove.lib.common import SchemaJsonMixin


class SchemaBODS(SchemaJsonMixin):

    def __init__(self, json_data=None, lib_cove_bods_config=None):
        # The default schema we use ...
        self.release_pkg_schema_url = lib_cove_bods_config.config['schema_url']
        self.schema_host = lib_cove_bods_config.config['schema_url_host']
        self.schema_version = lib_cove_bods_config.config['schema_version']
        # ... unless the data specifies a version.
        if isinstance(json_data, list) and len(json_data) > 0:
            statement = json_data[0]
            if isinstance(statement, dict) \
                    and 'publicationDetails' in statement \
                    and isinstance(statement['publicationDetails'], dict) \
                    and 'bodsVersion' in statement['publicationDetails'] \
                    and statement['publicationDetails']['bodsVersion']:
                version = statement['publicationDetails']['bodsVersion']
                if version in lib_cove_bods_config.config['schema_versions']:
                    self.release_pkg_schema_url = lib_cove_bods_config.config['schema_versions'][version]['schema_url']
                    self.schema_host = lib_cove_bods_config.config['schema_versions'][version]['schema_url_host']
                    self.schema_version = version

    def get_entity_statement_types_list(self):
        for statement_schema in self._release_pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'entityStatement':
                return statement_schema['properties']['entityType']['enum']

    def get_person_statement_types_list(self):
        for statement_schema in self._release_pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'personStatement':
                return statement_schema['properties']['personType']['enum']

    def get_ownership_or_control_statement_interest_statement_types_list(self):
        for statement_schema in self._release_pkg_schema_obj['items']['oneOf']:
            if statement_schema['properties']['statementType']['enum'][0] == 'ownershipOrControlStatement':
                return statement_schema['properties']['interests']['items']['properties']['type']['enum']
