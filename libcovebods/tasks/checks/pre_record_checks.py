from libcovebods.base_task import AdditionalCheck


class CheckHasPublicListing(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than(
            "0.3"
        ) and schema_object.is_schema_version_less_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return ["has_public_listing_information_but_has_public_listing_is_false"]

    def check_entity_statement_first_pass(self, statement):
        if isinstance(statement.get("publicListing"), dict):
            pl = statement.get("publicListing")
            if pl.get("companyFilingsURLs") or pl.get("securitiesListings"):
                if not pl.get("hasPublicListing"):
                    self._additional_check_results.append(
                        {
                            "type": "has_public_listing_information_but_has_public_listing_is_false",
                            "statement_type": "entity",
                            "statement": statement.get("statementID"),
                        }
                    )


class CheckEntityTypeAndEntitySubtypeAlign(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than(
            "0.3"
        ) and schema_object.is_schema_version_less_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return ["statement_entity_type_and_entity_sub_type_do_not_align"]

    def check_entity_statement_first_pass(self, statement):
        if isinstance(statement.get("entitySubtype"), dict):
            entitySubtype = statement["entitySubtype"].get("generalCategory")
            if entitySubtype and isinstance(entitySubtype, str):
                entityType = statement.get("entityType")
                entitySubtypeFirstBit = entitySubtype.split("-").pop(0)
                if entityType != entitySubtypeFirstBit:
                    self._additional_check_results.append(
                        {
                            "type": "statement_entity_type_and_entity_sub_type_do_not_align",
                            "statement_type": "entity",
                            "statement": statement.get("statementID"),
                        }
                    )


class CheckEntitySecurityListingsMICSCodes(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than(
            "0.3"
        ) and schema_object.is_schema_version_less_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return (
            [
                "entity_security_listing_market_identifier_code_set_but_not_operating_market_identifier_code",
                "entity_security_listing_operating_market_identifier_code_set_but_not_market_identifier_code",
            ]
            if (
                schema_object.is_schema_version_equal_to_or_greater_than("0.3")
                and schema_object.is_schema_version_less_than("0.4")
            )
            else []
        )

    def check_entity_statement_first_pass(self, statement):
        if isinstance(statement.get("publicListing"), dict) and isinstance(
            statement["publicListing"].get("securitiesListings"), list
        ):
            for securitiesListing in statement["publicListing"].get(
                "securitiesListings"
            ):
                if isinstance(securitiesListing, dict):
                    marketIdentifierCode = securitiesListing.get("marketIdentifierCode")
                    operatingMarketIdentifierCode = securitiesListing.get(
                        "operatingMarketIdentifierCode"
                    )
                    if marketIdentifierCode and not operatingMarketIdentifierCode:
                        self._additional_check_results.append(
                            {
                                "type": "entity_security_listing_market_identifier_code_set_but_not_operating_market_identifier_code",
                                "statement_type": "entity",
                                "statement": statement.get("statementID"),
                            }
                        )
                    elif operatingMarketIdentifierCode and not marketIdentifierCode:
                        self._additional_check_results.append(
                            {
                                "type": "entity_security_listing_operating_market_identifier_code_set_but_not_market_identifier_code",
                                "statement_type": "entity",
                                "statement": statement.get("statementID"),
                            }
                        )
