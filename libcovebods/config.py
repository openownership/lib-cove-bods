from libcove.config import LIB_COVE_CONFIG_DEFAULT, LibCoveConfig

LIB_COVE_BODS_CONFIG_DEFAULT = LIB_COVE_CONFIG_DEFAULT.copy()

LIB_COVE_BODS_CONFIG_DEFAULT.update({
    'schema_url': 'https://raw.githubusercontent.com/openownership/data-standard/schema-beta-2/schema/bods-package.json', # noqa
    'schema_url_host': 'https://raw.githubusercontent.com/openownership/data-standard/schema-beta-2/schema/',
})


class LibCoveBODSConfig(LibCoveConfig):
    def __init__(self, config=LIB_COVE_BODS_CONFIG_DEFAULT):
        self.config = config
