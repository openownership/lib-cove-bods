from libcove2.common import get_additional_fields_info
from libcovebods.schema import SchemaBODS


class AdditionalFields:
    """Process data and return additional fields information"""

    def __init__(self, schema: SchemaBODS):
        self._schema = schema

    def process(self, json_data: dict) -> list:
        """Process method. Call with data. Results are returned."""

        schema_fields = self._schema.get_package_schema_fields()

        additional_fields = get_additional_fields_info(json_data, schema_fields)

        return additional_fields
