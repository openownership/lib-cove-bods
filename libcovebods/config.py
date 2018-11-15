import os
from libcove.config import LIB_COVE_CONFIG_DEFAULT, LibCoveConfig

LIB_COVE_BODS_CONFIG_DEFAULT = LIB_COVE_CONFIG_DEFAULT.copy()

_schema_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'data'
)

LIB_COVE_BODS_CONFIG_DEFAULT.update({
    'schema_url': os.path.join(_schema_folder, 'schema.json'),
    'schema_url_host': _schema_folder,
})


class LibCoveBODSConfig(LibCoveConfig):
    def __init__(self, config=LIB_COVE_BODS_CONFIG_DEFAULT):
        self.config = config
