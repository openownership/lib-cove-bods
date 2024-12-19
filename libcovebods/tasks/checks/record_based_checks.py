from collections import defaultdict
from datetime import datetime

import jsonpointer  # type: ignore
import pycountry
from libcove2.common import get_orgids_prefixes  # type: ignore

from libcovebods.base_task import AdditionalCheck
from libcovebods.utils import numeric_value, parse_date_field, sort_by_date


class CheckHasPublicListingRecord(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return ["has_public_listing_information_but_has_public_listing_is_false"]

    def check_entity_statement_first_pass(self, statement):
        record = statement.get("recordDetails")
        if isinstance(record, dict) and isinstance(record.get("publicListing"), dict):
            pl = record.get("publicListing")
            if pl.get("companyFilingsURLs") or pl.get("securitiesListings"):
                if not pl.get("hasPublicListing"):
                    self._additional_check_results.append(
                        {
                            "type": "has_public_listing_information_but_has_public_listing_is_false",
                            "statement_type": "entity",
                            "statement": statement.get("statementId"),
                        }
                    )


class CheckEntitySecurityListingsMICSCodesRecord(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return (
            [
                "entity_security_listing_market_identifier_code_set_but_not_operating_market_identifier_code",
                "entity_security_listing_operating_market_identifier_code_set_but_not_market_identifier_code",
            ]
            if schema_object.is_schema_version_equal_to_or_greater_than("0.3")
            else []
        )

    def check_entity_statement_first_pass(self, statement):
        record = statement.get("recordDetails")
        if (
            isinstance(record, dict)
            and isinstance(record.get("publicListing"), dict)
            and isinstance(record["publicListing"].get("securitiesListings"), list)
        ):
            for securitiesListing in record["publicListing"].get("securitiesListings"):
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
                                "statement": statement.get("statementId"),
                            }
                        )
                    elif operatingMarketIdentifierCode and not marketIdentifierCode:
                        self._additional_check_results.append(
                            {
                                "type": "entity_security_listing_operating_market_identifier_code_set_but_not_market_identifier_code",
                                "statement_type": "entity",
                                "statement": statement.get("statementId"),
                            }
                        )


class CheckSourceRetrievedAtFutureDate(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if (
            "source" in statement
            and isinstance(statement["source"], dict)
            and "retrievedAt" in statement["source"]
            and statement["source"]["retrievedAt"]
        ):
            retrieved_at = parse_date_field(statement["source"]["retrievedAt"])
            if retrieved_at and retrieved_at > datetime.now().date():
                self._additional_check_results.append(
                    {
                        "type": "statement_source_retrieved_at_future_date",
                        "statement_type": None,
                        "retrieval_date": str(retrieved_at),
                        "statement": statement.get("statementId"),
                    }
                )


class CheckStatementDateFutureDate(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "statementDate" in statement and statement["statementDate"]:
            statement_date = parse_date_field(statement["statementDate"])
            if statement_date and statement_date > datetime.now().date():
                self._additional_check_results.append(
                    {
                        "type": "statement_date_is_future_date",
                        "statement_type": None,
                        "statement_date": str(statement_date),
                        "statement": statement.get("statementId"),
                    }
                )


class CheckAnnotationCreationDateFutureDate(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "annotations" in statement and isinstance(statement["annotations"], list):
            for annotation in statement["annotations"]:
                if (
                    isinstance(annotation, dict)
                    and "creationDate" in annotation
                    and annotation["creationDate"]
                ):
                    creation_date = parse_date_field(annotation["creationDate"])
                    if creation_date and creation_date > datetime.now().date():
                        self._additional_check_results.append(
                            {
                                "type": "statement_annotation_creation_date_is_future_date",
                                "statement_type": None,
                                "creation_date": creation_date.strftime("%Y-%m-%d"),
                                "statement": statement.get("statementId"),
                            }
                        )


class CheckStatementPublicationDateFutureDate(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if (
            "publicationDetails" in statement
            and isinstance(statement["publicationDetails"], dict)
            and "publicationDate" in statement["publicationDetails"]
            and statement["publicationDetails"]["publicationDate"]
        ):
            publication_date = parse_date_field(
                statement["publicationDetails"]["publicationDate"]
            )
            if publication_date and publication_date > datetime.now().date():
                self._additional_check_results.append(
                    {
                        "type": "statement_publication_date_is_future_date",
                        "statement_type": None,
                        "publication_date": publication_date.strftime("%Y-%m-%d"),
                        "statement": statement.get("statementId"),
                    }
                )


class CheckStatementPersonDateOfDeathSane(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._min_date_year = lib_cove_bods_config.config[
            "bods_additional_checks_person_birthdate_min_year"
        ]

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_person_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "deathDate" in statement["recordDetails"]
            and statement["recordDetails"]["deathDate"]
        ):
            death_date = parse_date_field(statement["recordDetails"]["deathDate"])
            if death_date:
                if (
                    death_date > datetime.now().date()
                    or death_date.year < self._min_date_year
                ):
                    self._additional_check_results.append(
                        {
                            "type": "statement_person_death_date_not_sensible_value",
                            "statement_type": None,
                            "death_date": death_date.strftime("%Y-%m-%d"),
                            "statement": statement.get("statementId"),
                        }
                    )
                elif (
                    "birthDate" in statement["recordDetails"]
                    and statement["recordDetails"]["birthDate"]
                ):
                    birth_date = parse_date_field(
                        statement["recordDetails"]["birthDate"]
                    )
                    if (
                        death_date < birth_date
                        or (death_date - birth_date).days > 43830
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "statement_person_death_date_not_sensible_value",
                                "statement_type": None,
                                "death_date": death_date.strftime("%Y-%m-%d"),
                                "statement": statement.get("statementId"),
                            }
                        )


class CheckStatementEntityFoundationDissolutionDates(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_entity_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "foundingDate" in statement["recordDetails"]
            and statement["recordDetails"]["foundingDate"]
            and "dissolutionDate" in statement["recordDetails"]
            and statement["recordDetails"]["dissolutionDate"]
        ):
            founding_date = parse_date_field(statement["recordDetails"]["foundingDate"])
            dissolution_date = parse_date_field(
                statement["recordDetails"]["dissolutionDate"]
            )
            if founding_date > dissolution_date:
                self._additional_check_results.append(
                    {
                        "type": "statement_entity_dissolution_before_founding_date",
                        "statement_type": None,
                        "founding_date": founding_date.strftime("%Y-%m-%d"),
                        "dissolution_date": dissolution_date.strftime("%Y-%m-%d"),
                        "statement": statement.get("statementId"),
                    }
                )


class CheckStatementPersonBirthDateSensible(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_person_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "birthDate" in statement["recordDetails"]
            and statement["recordDetails"]["birthDate"]
        ):
            birth_date = parse_date_field(statement["recordDetails"]["birthDate"])
            if birth_date:
                if birth_date > datetime.now().date():
                    self._additional_check_results.append(
                        {
                            "type": "statement_person_birth_date_in_future",
                            "statement_type": None,
                            "birth_date": birth_date.strftime("%Y-%m-%d"),
                            "statement": statement.get("statementId"),
                        }
                    )
                elif birth_date < datetime.strptime("1800-01-01", "%Y-%m-%d").date():
                    self._additional_check_results.append(
                        {
                            "type": "statement_person_birth_date_too_far_in_past",
                            "statement_type": None,
                            "birth_date": birth_date.strftime("%Y-%m-%d"),
                            "statement": statement.get("statementId"),
                        }
                    )


class CheckStatementRelationshipInterestsStartEndDates(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_ownership_or_control_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "interests" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["interests"], list)
        ):
            for interest in statement["recordDetails"]["interests"]:
                if (
                    "startDate" in interest
                    and interest["startDate"]
                    and "endDate" in interest
                    and interest["endDate"]
                ):
                    start_date = parse_date_field(interest["startDate"])
                    end_date = parse_date_field(interest["endDate"])
                    if start_date and end_date:
                        if start_date > end_date:
                            self._additional_check_results.append(
                                {
                                    "type": "statement_relationship_interests_start_after_end_date",
                                    "statement_type": None,
                                    "start_date": start_date.strftime("%Y-%m-%d"),
                                    "end_date": end_date.strftime("%Y-%m-%d"),
                                    "statement": statement.get("statementId"),
                                }
                            )


class CheckStatementEntitySecuritiesListingsHasPublicListing(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_entity_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "publicListing" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["publicListing"], dict)
            and "securitiesListings" in statement["recordDetails"]["publicListing"]
            and isinstance(
                statement["recordDetails"]["publicListing"]["securitiesListings"], list
            )
            and len(statement["recordDetails"]["publicListing"]["securitiesListings"])
            > 0
        ):
            if statement["recordDetails"]["publicListing"]["hasPublicListing"] is False:
                self._additional_check_results.append(
                    {
                        "type": "statement_entity_securities_listings_haspubliclisting_is_false",
                        "statement_type": None,
                        "securities_listings": statement["recordDetails"][
                            "publicListing"
                        ]["securitiesListings"],
                        "statement": statement.get("statementId"),
                    }
                )


class CheckStatementRelationshipInterestsShareValues(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_ownership_or_control_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "interests" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["interests"], list)
        ):
            for interest in statement["recordDetails"]["interests"]:
                if "share" in interest and isinstance(interest["share"], dict):
                    share = interest["share"]
                    if "exclusiveMinimum" in share and "minimum" in share:
                        self._additional_check_results.append(
                            {
                                "type": "statement_relationship_interests_share_min_and_exclusivemin",
                                "statement_type": None,
                                "share": interest["share"],
                                "statement": statement.get("statementId"),
                            }
                        )
                    elif "maximum" in share and "exclusiveMaximum" in share:
                        self._additional_check_results.append(
                            {
                                "type": "statement_relationship_interests_share_max_and_exclusivemax",
                                "statement_type": None,
                                "share": interest["share"],
                                "statement": statement.get("statementId"),
                            }
                        )
                    if "exact" in share and share["exact"]:
                        if any(
                            [
                                limit in share
                                for limit in (
                                    "exclusiveMinimum",
                                    "minimum",
                                    "maximum",
                                    "exclusiveMaximum",
                                )
                            ]
                        ):
                            self._additional_check_results.append(
                                {
                                    "type": "statement_relationship_interests_exact_has_min_max",
                                    "statement_type": None,
                                    "share_exact": share["exact"],
                                    "statement": statement.get("statementId"),
                                }
                            )
                            return
                    if (
                        (
                            "exclusiveMinimum" in share
                            and numeric_value(share["exclusiveMinimum"])
                        )
                        or ("minimum" in share and numeric_value(share["minimum"]))
                    ) and (
                        (
                            "exclusiveMaximum" in share
                            and numeric_value(share["exclusiveMaximum"])
                        )
                        or ("maximum" in share and numeric_value(share["maximum"]))
                    ):
                        min_val = (
                            float(share["minimum"])
                            if "minimum" in share
                            else float(share["exclusiveMinimum"])
                        )
                        max_val = (
                            float(share["maximum"])
                            if "maximum" in share
                            else float(share["exclusiveMaximum"])
                        )
                        if not max_val >= min_val:
                            self._additional_check_results.append(
                                {
                                    "type": "statement_relationship_interests_not_exact_max_greater_than_min",
                                    "statement_type": None,
                                    "minval": min_val,
                                    "maxval": max_val,
                                    "statement": statement.get("statementId"),
                                }
                            )
                        elif max_val == min_val:
                            self._additional_check_results.append(
                                {
                                    "type": "statement_relationship_interests_exact_max_equals_min",
                                    "statement_type": None,
                                    "minval": min_val,
                                    "maxval": max_val,
                                    "statement": statement.get("statementId"),
                                }
                            )


class CheckStatementDeclarationSubject(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._statements = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "recordId" in statement and "recordType" in statement:
            if statement["recordId"] in self._statements:
                self._statements[statement["recordId"]].append(statement["recordType"])
            else:
                self._statements[statement["recordId"]] = [statement["recordType"]]

    def check_statement_second_pass(self, statement):
        if "declarationSubject" in statement:
            if statement["declarationSubject"] not in self._statements:
                self._additional_check_results.append(
                    {
                        "type": "statement_declaration_subject_not_exist",
                        "statement_type": None,
                        "declaration_subject": statement["declarationSubject"],
                        "statement": statement.get("statementId"),
                    }
                )
            else:
                for record_type in self._statements[statement["declarationSubject"]]:
                    if record_type not in ("entity", "person"):
                        self._additional_check_results.append(
                            {
                                "type": "statement_declaration_subject_not_entity_person",
                                "statement_type": None,
                                "record_id": statement["declarationSubject"],
                                "record_type": record_type,
                                "statement": statement.get("statementId"),
                            }
                        )


class CheckStatementIsComponent(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._count = 0
        self._statements = {}
        self._components = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "recordId" in statement:
            self._statements[statement["recordId"]] = self._count
            self._count += 1
            if (
                "recordDetails" in statement
                and isinstance(statement["recordDetails"], dict)
                and "componentRecords" in statement["recordDetails"]
                and isinstance(statement["recordDetails"]["componentRecords"], list)
            ):
                for component_id in statement["recordDetails"]["componentRecords"]:
                    self._components[component_id] = statement["recordId"]

    def check_statement_second_pass(self, statement):
        if (
            "recordId" in statement
            and "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "isComponent" in statement["recordDetails"]
        ):
            if statement["recordDetails"]["isComponent"] is True:
                if statement["recordId"] not in self._components or not (
                    self._statements[statement["recordId"]]
                    < self._statements[self._components[statement["recordId"]]]
                ):
                    if "recordType" in statement:
                        if statement["recordType"] == "entity":
                            self._additional_check_results.append(
                                {
                                    "type": "statement_entity_is_component_not_in_component_details",
                                    "statement_type": None,
                                    "statement": statement.get("statementId"),
                                }
                            )
                        elif statement["recordType"] == "person":
                            self._additional_check_results.append(
                                {
                                    "type": "statement_person_is_component_not_in_component_details",
                                    "statement_type": None,
                                    "statement": statement.get("statementId"),
                                }
                            )
                        elif statement["recordType"] == "relationship":
                            self._additional_check_results.append(
                                {
                                    "type": "statement_relationship_is_component_not_in_component_details",
                                    "statement_type": None,
                                    "statement": statement.get("statementId"),
                                }
                            )


class CheckStatementDuplicateStatementId(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._count = 0
        self._statements = defaultdict(int)
        self._components = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "statementId" in statement:
            self._statements[statement["statementId"]] += 1

    def check_statement_second_pass(self, statement):
        if "statementId" in statement:
            if self._statements[statement["statementId"]] > 1:
                self._statements[statement["statementId"]] -= 1
                self._additional_check_results.append(
                    {
                        "type": "duplicate_statement_id",
                        "statement_type": None,
                        "id": statement.get("statementId"),
                    }
                )


class CheckStatementSeries(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._count = 0
        self._series = {}
        self._components = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if (
            "recordId" in statement
            and "statementDate" in statement
            and "statementDate" in statement
            and statement["statementDate"]
        ):
            record_status = statement.get("recordStatus")
            record_type = statement.get("recordType")
            statement_id = statement.get("statementId")
            if statement["recordId"] in self._series:
                self._series[statement["recordId"]].append(
                    [
                        statement["statementDate"],
                        record_status,
                        record_type,
                        statement_id,
                    ]
                )
            else:
                self._series[statement["recordId"]] = [
                    [
                        statement["statementDate"],
                        record_status,
                        record_type,
                        statement_id,
                    ]
                ]

    def final_checks(self):
        for series in self._series:
            sorted_series = sort_by_date(self._series[series], 0)
            statuses = [s[1] for s in sorted_series]
            types = [s[2] for s in sorted_series]
            if len([s for s in statuses if s == "new"]) > 1:
                self._additional_check_results.append(
                    {
                        "type": "multiple_statements_in_series_with_record_status_new",
                        "statement_type": None,
                        "record_id": series,
                    }
                )
            elif "new" in statuses and statuses[0] != "new":
                self._additional_check_results.append(
                    {
                        "type": "statement_with_record_status_new_must_be_first",
                        "statement_type": None,
                        "record_id": series,
                        "statement_id": sorted_series[0][-1],
                    }
                )
            elif len([s for s in statuses if s == "closed"]) > 1:
                self._additional_check_results.append(
                    {
                        "type": "multiple_statements_in_series_with_record_status_closed",
                        "statement_type": None,
                        "record_id": series,
                    }
                )
            elif "closed" in statuses and statuses[-1] != "closed":
                self._additional_check_results.append(
                    {
                        "type": "statement_with_record_status_closed_must_be_last",
                        "statement_type": None,
                        "record_id": series,
                        "statement_id": sorted_series[0][-1],
                    }
                )
            elif len(set(types)) > 1:
                self._additional_check_results.append(
                    {
                        "type": "statements_in_series_with_different_record_types",
                        "statement_type": None,
                        "record_id": series,
                    }
                )


class CheckComponentRecordsRecordIds(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._records = {}
        self._statements = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "recordId" in statement:
            self._records[statement["recordId"]] = None
        if "statementId" in statement:
            self._records[statement["statementId"]] = None

    def check_ownership_or_control_statement_second_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "componentRecords" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["componentRecords"], list
            ):
                for component in statement["recordDetails"]["componentRecords"]:
                    if component not in self._records:
                        if component in self._statements:
                            self._additional_check_results.append(
                                {
                                    "type": "component_record_is_statement_id",
                                    "statement_type": None,
                                    "statement": statement.get("statementId"),
                                    "compoment_id": component,
                                }
                            )
                        else:
                            self._additional_check_results.append(
                                {
                                    "type": "component_record_id_not_in_dataset",
                                    "statement_type": None,
                                    "statement": statement.get("statementId"),
                                    "compoment_id": component,
                                }
                            )


class CheckStatementRelationshipParties(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._records = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "recordId" in statement:
            record_type = statement.get("recordType")
            self._records[statement["recordId"]] = record_type

    def check_ownership_or_control_statement_second_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "subject" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["subject"], str
            ):
                if statement["recordDetails"]["subject"] not in self._records:
                    self._additional_check_results.append(
                        {
                            "type": "subject_must_be_record_id",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "subject": statement["recordDetails"]["subject"],
                        }
                    )
                elif (
                    not self._records[statement["recordDetails"]["subject"]] == "entity"
                ):
                    self._additional_check_results.append(
                        {
                            "type": "subject_can_only_refer_to_entity",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "subject": statement["recordDetails"]["subject"],
                        }
                    )
            if "interestedParty" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interestedParty"], str
            ):
                if statement["recordDetails"]["interestedParty"] not in self._records:
                    self._additional_check_results.append(
                        {
                            "type": "interested_party_must_be_record_id",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "interested_party": statement["recordDetails"][
                                "interestedParty"
                            ],
                        }
                    )
                elif self._records[
                    statement["recordDetails"]["interestedParty"]
                ] not in ("entity", "person"):
                    self._additional_check_results.append(
                        {
                            "type": "interested_party_can_only_refer_to_entity_or_person",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "interested_party": statement["recordDetails"][
                                "interestedParty"
                            ],
                        }
                    )
                else:
                    if "interests" in statement["recordDetails"] and isinstance(
                        statement["recordDetails"]["interests"], list
                    ):
                        for interest in statement["recordDetails"]["interests"]:
                            if (
                                "beneficialOwnershipOrControl" in interest
                                and interest["beneficialOwnershipOrControl"] is True
                            ):
                                if (
                                    not self._records[
                                        statement["recordDetails"]["interestedParty"]
                                    ]
                                    == "person"
                                ):
                                    self._additional_check_results.append(
                                        {
                                            "type": "interest_beneficial_ownership_interested_party_not_person",
                                            "statement_type": None,
                                            "statement": statement.get("statementId"),
                                            "interested_party": statement[
                                                "recordDetails"
                                            ]["interestedParty"],
                                        }
                                    )


class CheckAnnotationStatementPointerTarget(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_entity_statement_first_pass(self, statement):
        if "annotations" in statement and isinstance(statement["annotations"], list):
            for annotation in statement["annotations"]:
                if "statementPointerTarget" in annotation:
                    try:
                        jsonpointer.resolve_pointer(
                            statement, annotation["statementPointerTarget"]
                        )
                    except (jsonpointer.JsonPointerException, TypeError):
                        self._additional_check_results.append(
                            {
                                "type": "annotation_statement_pointer_target_invalid",
                                "statement_type": None,
                                "statement": statement.get("statementId"),
                                "pointer": annotation["statementPointerTarget"],
                            }
                        )


class CheckStatementRelationshipInterests(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._records = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if (
            "recordId" in statement
            and "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
        ):
            record_type = statement.get("recordType")
            if record_type == "entity":
                record_type_type = statement["recordDetails"].get("entityType")
            elif record_type == "person":
                record_type_type = statement["recordDetails"].get("personType")
            else:
                record_type_type = None
            self._records[statement["recordId"]] = (record_type, record_type_type)

    def check_ownership_or_control_statement_second_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "interests" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interests"], list
            ):
                for interest in statement["recordDetails"]["interests"]:
                    if "type" in interest and interest["type"] in (
                        "nominee",
                        "nominator",
                    ):
                        if "subject" in statement["recordDetails"] and isinstance(
                            statement["recordDetails"]["subject"], str
                        ):
                            if (
                                not self._records[
                                    statement["recordDetails"]["subject"]
                                ][0]
                                == "entity"
                            ):
                                self._additional_check_results.append(
                                    {
                                        "type": "relationship_interests_subject_should_be_entity_nomination_arrangement",
                                        "statement_type": None,
                                        "statement": statement.get("statementId"),
                                        "subject_record_type": self._records[
                                            statement["recordDetails"]["subject"]
                                        ][0],
                                        "subject_record_subtype": self._records[
                                            statement["recordDetails"]["subject"]
                                        ][1],
                                    }
                                )
                            else:
                                entity_type = self._records[
                                    statement["recordDetails"]["subject"]
                                ][1]
                                if (
                                    not entity_type
                                    or not isinstance(statement["recordDetails"], dict)
                                    or "type" not in entity_type
                                    or not entity_type["type"] == "arrangement"
                                    or "subtype" not in entity_type
                                    or not entity_type["subtype"] == "nomination"
                                ):
                                    self._additional_check_results.append(
                                        {
                                            "type": "relationship_interests_subject_should_be_entity_nomination_arrangement",
                                            "statement_type": None,
                                            "statement": statement.get("statementId"),
                                            "subject_record_type": self._records[
                                                statement["recordDetails"]["subject"]
                                            ][0],
                                            "subject_record_subtype": self._records[
                                                statement["recordDetails"]["subject"]
                                            ][1],
                                        }
                                    )
                    elif "type" in interest and interest["type"] in (
                        "settlor",
                        "trustee",
                        "protector",
                    ):
                        if "subject" in statement["recordDetails"] and isinstance(
                            statement["recordDetails"]["subject"], str
                        ):
                            if (
                                not self._records[
                                    statement["recordDetails"]["subject"]
                                ][0]
                                == "entity"
                            ):
                                self._additional_check_results.append(
                                    {
                                        "type": "relationship_interests_subject_should_be_entity_trust",
                                        "statement_type": None,
                                        "statement": statement.get("statementId"),
                                        "subject_record_type": self._records[
                                            statement["recordDetails"]["subject"]
                                        ][0],
                                        "subject_record_subtype": self._records[
                                            statement["recordDetails"]["subject"]
                                        ][1],
                                    }
                                )
                            else:
                                entity_type = self._records[
                                    statement["recordDetails"]["subject"]
                                ][1]
                                if (
                                    not entity_type
                                    or not isinstance(statement["recordDetails"], dict)
                                    or "subtype" not in entity_type
                                    or not entity_type["subtype"] == "trust"
                                ):
                                    self._additional_check_results.append(
                                        {
                                            "type": "relationship_interests_subject_should_be_entity_trust",
                                            "statement_type": None,
                                            "statement": statement.get("statementId"),
                                            "subject_record_type": self._records[
                                                statement["recordDetails"]["subject"]
                                            ][0],
                                            "subject_record_subtype": self._records[
                                                statement["recordDetails"]["subject"]
                                            ][1],
                                        }
                                    )


class CheckStatementSerialisation(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._count = 0
        self._records = {}
        self._components = {}

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_statement_first_pass(self, statement):
        if "recordId" in statement:
            self._count += 1
            if statement["recordId"] not in self._records:
                self._records[statement["recordId"]] = self._count

    def check_ownership_or_control_statement_second_pass(self, statement):
        if (
            "recordId" in statement
            and "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
        ):
            if "subject" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["subject"], str
            ):
                if statement["recordDetails"]["subject"] in self._records:
                    if (
                        self._records[statement["recordDetails"]["subject"]]
                        > self._records[statement["recordId"]]
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "relationship_subject_not_before_relationship_in_dataset",
                                "statement_type": None,
                                "statement": statement.get("statementId"),
                                "subject_id": statement["recordDetails"]["subject"],
                            }
                        )
        if (
            "recordId" in statement
            and "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
        ):
            if "interestedParty" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interestedParty"], str
            ):
                if statement["recordDetails"]["interestedParty"] in self._records:
                    if (
                        self._records[statement["recordDetails"]["interestedParty"]]
                        > self._records[statement["recordId"]]
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "relationship_interested_party_not_before_relationship_in_dataset",
                                "statement_type": None,
                                "statement": statement.get("statementId"),
                                "interested_party_id": statement["recordDetails"][
                                    "interestedParty"
                                ],
                            }
                        )


class CheckStatementPersonIdentifiersHaveCorrectScheme(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._count = 0
        self._records = {}
        self._components = {}
        self._other_codes = lib_cove_bods_config.config[
            "bods_additional_checks_other_country_codes"
        ]

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_person_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "identifiers" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["identifiers"], list)
        ):
            for identifier in statement["recordDetails"]["identifiers"]:
                if not (
                    "scheme" in identifier
                    and identifier["scheme"].count("-") == 1
                    and len(identifier["scheme"].split("-")[0]) > 0
                    and len(identifier["scheme"].split("-")[1]) > 0
                ):
                    self._additional_check_results.append(
                        {
                            "type": "person_identifiers_invalid_composition",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "scheme": identifier["scheme"]
                            if "scheme" in identifier
                            else None,
                        }
                    )
                else:
                    if (
                        not pycountry.countries.get(
                            alpha_3=identifier["scheme"].split("-")[0]
                        )
                        and identifier["scheme"].split("-")[0] not in self._other_codes
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "person_identifiers_no_valid_iso_3166_1_alpha_3_code",
                                "statement_type": None,
                                "statement": statement.get("statementId"),
                                "scheme": identifier["scheme"],
                            }
                        )
                    elif identifier["scheme"].split("-")[1] not in (
                        "PASSPORT",
                        "TAXID",
                        "IDCARD",
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "person_identifiers_not_passport_taxid_idcard",
                                "statement_type": None,
                                "statement": statement.get("statementId"),
                                "scheme": identifier["scheme"],
                            }
                        )


class CheckStatementEntityIdentifiersHaveKnownScheme(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.orgids_prefixes = get_orgids_prefixes()

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def check_entity_statement_first_pass(self, statement):
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "identifiers" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["identifiers"], list)
        ):
            for identifier in statement["recordDetails"]["identifiers"]:
                if (
                    "scheme" in identifier
                    and not identifier["scheme"] in self.orgids_prefixes
                ):
                    self._additional_check_results.append(
                        {
                            "type": "entity_identifiers_not_known_scheme",
                            "statement_type": None,
                            "statement": statement.get("statementId"),
                            "scheme": identifier["scheme"]
                            if "scheme" in identifier
                            else None,
                        }
                    )
