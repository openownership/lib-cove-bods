import datetime
import os

from libcove.config import LIB_COVE_CONFIG_DEFAULT, LibCoveConfig
from requests_cache import CachedSession, FileCache

LIB_COVE_BODS_CONFIG_DEFAULT = LIB_COVE_CONFIG_DEFAULT.copy()

_schema_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
_requests_cache_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "requests_cache_dir"
)

LIB_COVE_BODS_CONFIG_DEFAULT.update(
    {
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
        },
        # In some cases we default to the latest schema version, so we need to know what the latest version is.
        # It should be a key that is in the 'schema_versions' data.
        "schema_latest_version": "0.3",
        # These default values are very wide on purpose. It is left to apps using this to tighten them up.
        "bods_additional_checks_person_birthdate_min_year": 1,
        "bods_additional_checks_person_birthdate_max_year": datetime.datetime.now().year,
        "requests_cache_dir": _requests_cache_dir,
    }
)


class LibCoveBODSConfig(LibCoveConfig):
    def __init__(self, config=None):
        # We need to make sure we take a copy,
        #   so that changes to one config object don't end up effecting other config objects.
        if config:
            self.config = config.copy()
        else:
            self.config = LIB_COVE_BODS_CONFIG_DEFAULT.copy()
        self._requests_session_with_caching = None

    def get_requests_session_with_caching(self):
        if not self._requests_session_with_caching:
            self._requests_session_with_caching = CachedSession(
                "iati_cove_cache",
                backend=FileCache(
                    cache_name=self.config.get(
                        "requests_cache_dir", "/tmp/requests_cache_dir"
                    )
                ),
                expire_after=datetime.timedelta(
                    days=1
                ),  # Expire responses after one day
                allowable_methods=[
                    "GET"
                ],  # All our requests we want to cache are GET requests
                allowable_codes=[
                    200,
                    400,
                ],  # Cache 400 responses as a solemn reminder of your failures
                stale_if_error=True,  # In case of request errors, use stale cache data if possible
            )
        return self._requests_session_with_caching
