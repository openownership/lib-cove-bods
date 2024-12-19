import datetime
import os

_schema_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

LIB_COVE_BODS_CONFIG_DEFAULT = {
    # These details are used if the data does not specify a version
    "schema_url": os.path.join(_schema_folder, "schema-0-1-0.json"),
    "schema_url_host": _schema_folder,
    "schema_version": "0.1",
    # But from 0.2 onwards, data should specify a version
    "schema_versions": {
        "0.2": {
            "schema_url": os.path.join(_schema_folder, "schema-0-2-0.json"),
            "schema_url_host": _schema_folder,
        },
        "0.3": {
            "schema_url": os.path.join(_schema_folder, "schema-0-3-0.json"),
            "schema_url_host": _schema_folder,
        },
        "0.4": {
            "schema_url": os.path.join(_schema_folder, "schema-0-4-0"),
            "schema_url_host": _schema_folder,
        },
    },
    # In some cases we default to the latest schema version, so we need to know what the latest version is.
    # It should be a key that is in the 'schema_versions' data.
    # Note: Schema changed substantially from 0.3 to 0.4 (record based) so in cases where the schema
    # version is not specified will try to determine whether is pre or post that change, and default to
    # either the latest version (if after change) or a pre-change schema if before change
    "schema_latest_version": "0.4",
    # Or latest version before change to records (in 0.4)
    "schema_latest_nonrecord_version": "0.3",
    # These default values are very wide on purpose. It is left to apps using this to tighten them up.
    "bods_additional_checks_person_birthdate_min_year": 1800,
    "bods_additional_checks_person_birthdate_max_year": datetime.datetime.now().year,
    # Other widely used (but "non-standard") country codes that should be allowed
    # See: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3 (User-assigned code elements section)
    "bods_additional_checks_other_country_codes": (
        "BAH",
        "D",
        "EUE",
        "GBD",
        "GBN",
        "GBO",
        "GBP",
        "GBS",
        "UNA",
        "UNK",
        "UNO",
        "XBA",
        "XIM",
        "XCC",
        "XCO",
        "XEC",
        "XPO",
        "XOM",
        "XXA",
        "XXB",
        "XXC",
        "XXX",
        "ZIM",
    ),
}


class LibCoveBODSConfig:
    def __init__(self, config=None):
        # We need to make sure we take a copy,
        #   so that changes to one config object don't end up effecting other config objects.
        if config:
            self.config = config.copy()
        else:
            self.config = LIB_COVE_BODS_CONFIG_DEFAULT.copy()
