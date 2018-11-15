from libcove.lib.common import SchemaJsonMixin


class SchemaBODS(SchemaJsonMixin):

    def __init__(self, lib_cove_bods_config=None):
        self.release_pkg_schema_url = lib_cove_bods_config.config['schema_url']
        self.schema_host = lib_cove_bods_config.config['schema_url_host']
