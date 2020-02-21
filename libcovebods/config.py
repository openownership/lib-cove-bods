import os
import datetime
from libcove.config import LIB_COVE_CONFIG_DEFAULT, LibCoveConfig

LIB_COVE_BODS_CONFIG_DEFAULT = LIB_COVE_CONFIG_DEFAULT.copy()

_schema_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)),  'data'
)

LIB_COVE_BODS_CONFIG_DEFAULT.update({
    # These details are used if the data does not specify a version
    'schema_url': os.path.join(_schema_folder, 'schema-0-1-0.json'),
    'schema_url_host': _schema_folder,
    'schema_version': '0.1',
    # But from 0.2 onwards, data should specify a version
    'schema_versions': {
        '0.2': {
            'schema_url': os.path.join(_schema_folder, 'schema-0-2-0.json'),
            'schema_url_host': _schema_folder,
        }
    },
    # These default values are very wide on purpose. It is left to apps using this to tighten them up.
    'bods_additional_checks_person_birthdate_min_year': 1,
    'bods_additional_checks_person_birthdate_max_year': datetime.datetime.now().year,
})


class LibCoveBODSConfig(LibCoveConfig):
    def __init__(self, config=None):
        # We need to make sure we take a copy,
        #   so that changes to one config object don't end up effecting other config objects.
        if config:
            self.config = config.copy()
        else:
            self.config = LIB_COVE_BODS_CONFIG_DEFAULT.copy()
