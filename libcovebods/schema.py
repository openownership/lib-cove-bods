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
