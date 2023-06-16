from libcove2.common import get_additional_fields_info  # type: ignore

import libcovebods.data_reader
from libcovebods.schema import SchemaBODS


class AdditionalFields:
    """Process data and return additional fields information"""

    def __init__(self, schema: SchemaBODS):
        self._schema = schema

    def process(self, data_reader: libcovebods.data_reader.DataReader) -> list:
        """Process method. Call with data. Results are returned."""

        schema_fields = self._schema.get_package_schema_fields()

        additional_fields = get_additional_fields_info(
            data_reader.get_all_data(), schema_fields
        )

        return additional_fields
