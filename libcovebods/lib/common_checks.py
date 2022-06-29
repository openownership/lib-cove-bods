from collections import defaultdict

from libcove.lib.common import get_orgids_prefixes

from libcovebods.lib.common import (
    get_year_from_bods_birthdate_or_deathdate,
    is_interest_current,
)


class AdditionalCheck:
    """Any check or statistic that wants to be provided should extend this abstract class and overwrite methods"""

    def __init__(self, lib_cove_bods_config, schema_object):
        self._additional_check_results = []
        self._lib_cove_bods_config = lib_cove_bods_config
        self._schema_object = schema_object

    def does_apply_to_schema(self):
        return True

    def check_statement_first_pass(self, statement):
        pass

    def check_entity_statement_first_pass(self, statement):
        pass

    def check_person_statement_first_pass(self, statement):
        pass

    def check_ownership_or_control_statement_first_pass(self, statement):
        pass

    def check_entity_statement_second_pass(self, statement):
        pass

    def check_person_statement_second_pass(self, statement):
        pass

    def check_ownership_or_control_statement_second_pass(self, statement):
        pass

    def final_checks(self):
        pass

    def get_additional_check_results(self):
        return self._additional_check_results

    def get_statistics(self):
        return {}


class LegacyStatistics(AdditionalCheck):
    """Before the AdditionalCheck system was implemented, all this code was together in one class.
    As we work on statistics in this class, we should move them to seperate classes if possible."""

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)

        # Entity
        self.count_entity_statements = 0
        self.count_entity_statements_types = {}
        for value in schema_object.get_entity_statement_types_list():
            self.count_entity_statements_types[value] = 0
        self.count_entity_statements_types_with_any_identifier = (
            self.count_entity_statements_types.copy()
        )
        self.count_entity_statements_types_with_any_identifier_with_id_and_scheme = (
            self.count_entity_statements_types.copy()
        )
        # People
        self.count_person_statements = 0
        self.count_person_statements_types = {}
        for value in schema_object.get_person_statement_types_list():
            self.count_person_statements_types[value] = 0
        # Ownership or control
        self.count_ownership_or_control_statement = 0
        self.count_ownership_or_control_statement_interested_party_with_person = 0
        self.count_ownership_or_control_statement_interested_party_with_entity = 0
        self.count_ownership_or_control_statement_interested_party_with_unspecified = 0
        self.count_ownership_or_control_statement_interest_statement_types = {}
        for (
            value
        ) in (
            schema_object.get_ownership_or_control_statement_interest_statement_types_list()
        ):
            self.count_ownership_or_control_statement_interest_statement_types[
                value
            ] = 0
        self.count_replaces_statements_missing = 0
        self.statement_ids = set()
        self.current_statement_ids = set()
        self.count_ownership_or_control_statement_by_year = defaultdict(int)
        self.subject_statement_ids_by_year = defaultdict(set)
        self.count_ownership_or_control_statement_interested_party_with_entity_by_year = defaultdict(
            int
        )
        self.count_ownership_or_control_statement_interested_party_with_person_by_year = defaultdict(
            int
        )
        self.count_ownership_or_control_statement_interested_party_with_unspecified_by_year = defaultdict(
            int
        )
        # Others
        self.count_addresses = 0
        self.count_addresses_with_postcode = 0
        self.count_addresses_with_country = 0
        self.count_addresses_with_postcode_duplicated_in_address = 0

    def check_statement_first_pass(self, statement):
        if isinstance(statement.get("replacesStatements"), list):
            for replaces_statement_id in statement.get("replacesStatements"):
                if replaces_statement_id not in self.statement_ids:
                    self.count_replaces_statements_missing += 1
                if replaces_statement_id in self.current_statement_ids:
                    self.current_statement_ids.remove(replaces_statement_id)
        if "statementID" in statement and isinstance(statement["statementID"], str):
            self.statement_ids.add(statement["statementID"])

    def check_entity_statement_first_pass(self, statement):
        self.count_entity_statements += 1
        if (
            "entityType" in statement
            and isinstance(statement["entityType"], str)
            and statement["entityType"] in self.count_entity_statements_types
        ):
            self.count_entity_statements_types[statement["entityType"]] += 1
            if "identifiers" in statement and isinstance(
                statement["identifiers"], list
            ):
                has_ids = False
                has_ids_with_id_and_scheme = False
                for identifier in statement["identifiers"]:
                    if isinstance(identifier, dict):
                        has_ids = True
                        if (
                            "scheme" in identifier
                            and isinstance(identifier["scheme"], str)
                            and identifier["scheme"]
                            and "id" in identifier
                            and isinstance(identifier["id"], str)
                            and identifier["id"]
                        ):
                            has_ids_with_id_and_scheme = True

                if has_ids:
                    self.count_entity_statements_types_with_any_identifier[
                        statement["entityType"]
                    ] += 1
                    if has_ids_with_id_and_scheme:
                        self.count_entity_statements_types_with_any_identifier_with_id_and_scheme[
                            statement["entityType"]
                        ] += 1
        if "addresses" in statement and isinstance(statement["addresses"], list):
            for address in statement["addresses"]:
                self._process_address(address)

    def check_person_statement_first_pass(self, statement):
        self.count_person_statements += 1
        if (
            "personType" in statement
            and isinstance(statement["personType"], str)
            and statement["personType"] in self.count_person_statements_types
        ):
            self.count_person_statements_types[statement["personType"]] += 1
        if "addresses" in statement and isinstance(statement["addresses"], list):
            for address in statement["addresses"]:
                self._process_address(address)
        if "placeOfBirth" in statement and isinstance(statement["placeOfBirth"], dict):
            self._process_address(statement["placeOfBirth"])
        if "placeOfResidence" in statement and isinstance(
            statement["placeOfResidence"], dict
        ):
            self._process_address(statement["placeOfResidence"])

    def check_ownership_or_control_statement_first_pass(self, statement):
        try:
            year = int(statement.get("statementDate", "").split("-")[0])
        except (ValueError, AttributeError):
            year = None
        self.count_ownership_or_control_statement += 1
        interested_party = statement.get("interestedParty")
        if isinstance(interested_party, dict):
            if interested_party.get("describedByEntityStatement"):
                self.count_ownership_or_control_statement_interested_party_with_entity += (
                    1
                )
                self.count_ownership_or_control_statement_interested_party_with_entity_by_year[
                    year
                ] += 1
            if interested_party.get("describedByPersonStatement"):
                self.count_ownership_or_control_statement_interested_party_with_person += (
                    1
                )
                self.count_ownership_or_control_statement_interested_party_with_person_by_year[
                    year
                ] += 1
            if (
                interested_party.get("unspecified")
                and isinstance(interested_party.get("unspecified"), dict)
                and interested_party["unspecified"].get("reason")
            ):
                self.count_ownership_or_control_statement_interested_party_with_unspecified += (
                    1
                )
                self.count_ownership_or_control_statement_interested_party_with_unspecified_by_year[
                    year
                ] += 1
        if "interests" in statement and isinstance(statement["interests"], list):
            for interest in statement["interests"]:
                if isinstance(interest, dict):
                    if (
                        "type" in interest
                        and isinstance(interest["type"], str)
                        and interest["type"]
                        in self.count_ownership_or_control_statement_interest_statement_types
                    ):
                        self.count_ownership_or_control_statement_interest_statement_types[
                            interest["type"]
                        ] += 1
                    if is_interest_current(interest) and "statementID" in statement:
                        self.current_statement_ids.add(statement["statementID"])

        if "statementDate" in statement:
            self.count_ownership_or_control_statement_by_year[year] += 1
        if (
            "subject" in statement
            and isinstance(statement["subject"], dict)
            and "describedByEntityStatement" in statement["subject"]
        ):
            self.subject_statement_ids_by_year[year].add(
                statement["subject"]["describedByEntityStatement"]
            )
        if "addresses" in statement and isinstance(statement["addresses"], list):
            for address in statement["addresses"]:
                self._process_address(address)

    def _process_address(self, address):
        self.count_addresses += 1
        if address.get("postCode"):
            self.count_addresses_with_postcode += 1
        if address.get("country"):
            self.count_addresses_with_country += 1
        if (
            address.get("postCode")
            and address.get("address")
            and isinstance(address.get("postCode"), str)
            and isinstance(address.get("address"), str)
            and address.get("postCode").lower() in address.get("address").lower()
        ):
            self.count_addresses_with_postcode_duplicated_in_address += 1

    def get_statistics(self):
        data = {
            "count_entity_statements": self.count_entity_statements,
            "count_entity_statements_types": self.count_entity_statements_types,
            "count_entity_statements_types_with_any_identifier": self.count_entity_statements_types_with_any_identifier,
            "count_entity_statements_types_with_any_identifier_with_id_and_scheme": self.count_entity_statements_types_with_any_identifier_with_id_and_scheme,
            "count_person_statements": self.count_person_statements,
            "count_person_statements_types": self.count_person_statements_types,
            "count_ownership_or_control_statement": self.count_ownership_or_control_statement,
            "count_ownership_or_control_statement_current": len(
                self.current_statement_ids
            ),
            "count_ownership_or_control_statement_interested_party_with_person": self.count_ownership_or_control_statement_interested_party_with_person,
            "count_ownership_or_control_statement_interested_party_with_entity": self.count_ownership_or_control_statement_interested_party_with_entity,
            "count_ownership_or_control_statement_interested_party_with_unspecified": self.count_ownership_or_control_statement_interested_party_with_unspecified,
            "count_ownership_or_control_statement_interest_statement_types": self.count_ownership_or_control_statement_interest_statement_types,
            "count_ownership_or_control_statement_by_year": self.count_ownership_or_control_statement_by_year,
            "count_ownership_or_control_statement_subject_by_year": {
                year: len(year_set)
                for year, year_set in self.subject_statement_ids_by_year.items()
            },
            "count_ownership_or_control_statement_interested_party_with_entity_by_year": self.count_ownership_or_control_statement_interested_party_with_entity_by_year,
            "count_ownership_or_control_statement_interested_party_with_person_by_year": self.count_ownership_or_control_statement_interested_party_with_person_by_year,
            "count_ownership_or_control_statement_interested_party_with_unspecified_by_year": self.count_ownership_or_control_statement_interested_party_with_unspecified_by_year,
            "count_replaces_statements_missing": self.count_replaces_statements_missing,
            "count_addresses": self.count_addresses,
            "count_addresses_with_postcode": self.count_addresses_with_postcode,
            "count_addresses_with_country": self.count_addresses_with_country,
            "count_addresses_with_postcode_duplicated_in_address": self.count_addresses_with_postcode_duplicated_in_address,
        }
        return data


class StatisticOwnershipOrControlInterestDirectOrIndirect(AdditionalCheck):
    def does_apply_to_schema(self):
        return self._schema_object.is_schema_version_equal_to_or_greater_than("0.3")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_ownership_or_control_statement_interest_direct_or_indirect = {}
        for (
            value
        ) in (
            schema_object.get_ownership_or_control_statement_interest_direct_or_indirect_list()
        ):
            self.count_ownership_or_control_statement_interest_direct_or_indirect[
                value
            ] = 0

    def check_ownership_or_control_statement_first_pass(self, statement):
        if "interests" in statement and isinstance(statement["interests"], list):
            for interest in statement["interests"]:
                if isinstance(interest, dict):
                    if (
                        "directOrIndirect" in interest
                        and isinstance(interest["directOrIndirect"], str)
                        and interest["directOrIndirect"]
                        in self.count_ownership_or_control_statement_interest_direct_or_indirect
                    ):
                        self.count_ownership_or_control_statement_interest_direct_or_indirect[
                            interest["directOrIndirect"]
                        ] += 1

    def get_statistics(self):
        return {
            "count_ownership_or_control_statement_interest_direct_or_indirect": self.count_ownership_or_control_statement_interest_direct_or_indirect,
        }


class StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.stat = 0

    def check_ownership_or_control_statement_first_pass(self, statement):
        if "interests" in statement and isinstance(statement["interests"], list):
            interests_with_beneficialOwnershipOrControl = [
                i
                for i in statement["interests"]
                if isinstance(i, dict) and i.get("beneficialOwnershipOrControl")
            ]
            if interests_with_beneficialOwnershipOrControl:
                self.stat += 1

    def get_statistics(self):
        return {
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial": self.stat,
        }


class LegacyChecks(AdditionalCheck):
    """Before the AdditionalCheck system was implemented, all this code was together in one class.
    As we work on checks in this class, we should move them to seperate classes if possible."""

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.person_statements_seen = []
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.ownership_or_control_statements_seen = []
        self.statement_ids_seen_in_component_statement_ids = []
        self.possible_out_of_order_statements = []
        self.orgids_prefixes = get_orgids_prefixes()
        self.statement_ids_counted = {}

    def check_entity_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        self.entity_statements_seen.append(statement.get("statementID"))
        identifiers = statement.get("identifiers")
        if isinstance(identifiers, list):
            for identifier in identifiers:
                if isinstance(identifier, dict):
                    if (
                        "scheme" in identifier
                        and identifier["scheme"]
                        and not identifier["scheme"] in self.orgids_prefixes
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "entity_identifier_scheme_not_known",
                                "scheme": identifier.get("scheme"),
                                "entity_statement": statement.get("statementID"),
                            }
                        )
        (
            inconsistent_schema_version_error,
            inconsistent_schema_version_used,
        ) = self._schema_object.get_inconsistent_schema_version_used_for_statement(
            statement
        )
        if inconsistent_schema_version_error:
            self._additional_check_results.append(
                {
                    "type": "inconsistent_schema_version_used",
                    "schema_version": inconsistent_schema_version_used,
                    "statement_type": "entity",
                    "statement": statement.get("statementID"),
                }
            )
        if self._schema_object.schema_version != "0.1":
            if "addresses" in statement and isinstance(statement["addresses"], list):
                self._check_addresses_list_for_alternatives(statement)
                for address in statement["addresses"]:
                    if (
                        "type" in address
                        and address["type"]
                        not in self._schema_object.get_address_types_allowed_in_entity_statement()
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "wrong_address_type_used",
                                "address_type": address["type"],
                                "statement_type": "entity",
                                "statement": statement.get("statementID"),
                            }
                        )
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_is_after_use_in_component_statement_id",
                        "statement_type": "entity",
                        "statement": statement.get("statementID"),
                    }
                )

    def check_person_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        self.person_statements_seen.append(statement.get("statementID"))
        if "birthDate" in statement:
            birth_year = get_year_from_bods_birthdate_or_deathdate(
                statement["birthDate"]
            )
            if birth_year:
                if (
                    birth_year
                    < self._lib_cove_bods_config.config[
                        "bods_additional_checks_person_birthdate_min_year"
                    ]
                ):
                    self._additional_check_results.append(
                        {
                            "type": "person_birth_year_too_early",
                            "year": birth_year,
                            "person_statement": statement.get("statementID"),
                        }
                    )
                elif (
                    birth_year
                    > self._lib_cove_bods_config.config[
                        "bods_additional_checks_person_birthdate_max_year"
                    ]
                ):
                    self._additional_check_results.append(
                        {
                            "type": "person_birth_year_too_late",
                            "year": birth_year,
                            "person_statement": statement.get("statementID"),
                        }
                    )
        (
            inconsistent_schema_version_error,
            inconsistent_schema_version_used,
        ) = self._schema_object.get_inconsistent_schema_version_used_for_statement(
            statement
        )
        if inconsistent_schema_version_error:
            self._additional_check_results.append(
                {
                    "type": "inconsistent_schema_version_used",
                    "schema_version": inconsistent_schema_version_used,
                    "statement_type": "person",
                    "statement": statement.get("statementID"),
                }
            )
        if self._schema_object.schema_version != "0.1":
            if "addresses" in statement and isinstance(statement["addresses"], list):
                self._check_addresses_list_for_alternatives(statement)
                for address in statement["addresses"]:
                    if (
                        "type" in address
                        and address["type"]
                        not in self._schema_object.get_address_types_allowed_in_person_statement()
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "wrong_address_type_used",
                                "address_type": address["type"],
                                "statement_type": "person",
                                "statement": statement.get("statementID"),
                            }
                        )
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_is_after_use_in_component_statement_id",
                        "statement_type": "person",
                        "statement": statement.get("statementID"),
                    }
                )

    def check_ownership_or_control_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        self.ownership_or_control_statements_seen.append(statement.get("statementID"))
        interested_party = statement.get("interestedParty")
        if isinstance(interested_party, dict):
            interested_party_described_by_entity_statement = interested_party.get(
                "describedByEntityStatement"
            )
            interested_party_described_by_person_statement = interested_party.get(
                "describedByPersonStatement"
            )
            if interested_party_described_by_entity_statement:
                self.entity_statements_seen_in_ownership_or_control_statement.append(
                    interested_party_described_by_entity_statement
                )
                if (
                    interested_party_described_by_entity_statement
                    not in self.entity_statements_seen
                ):
                    self.possible_out_of_order_statements.append(
                        {
                            "type": "entity_statement_out_of_order",
                            "referenced_from": "interestedParty",
                            "entity_statement_out_of_order": interested_party_described_by_entity_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
            if interested_party_described_by_person_statement:
                self.person_statements_seen_in_ownership_or_control_statement.append(
                    interested_party_described_by_person_statement
                )
                if (
                    interested_party_described_by_person_statement
                    not in self.person_statements_seen
                ):
                    self.possible_out_of_order_statements.append(
                        {
                            "type": "person_statement_out_of_order",
                            "referenced_from": "interestedParty",
                            "person_statement_out_of_order": interested_party_described_by_person_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
        subject = statement.get("subject")
        if isinstance(subject, dict):
            subject_described_by_entity_statement = subject.get(
                "describedByEntityStatement"
            )
            if subject_described_by_entity_statement:
                self.entity_statements_seen_in_ownership_or_control_statement.append(
                    subject_described_by_entity_statement
                )
                if (
                    subject_described_by_entity_statement
                    not in self.entity_statements_seen
                ):
                    self.possible_out_of_order_statements.append(
                        {
                            "type": "entity_statement_out_of_order",
                            "referenced_from": "subject",
                            "entity_statement_out_of_order": subject_described_by_entity_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
        (
            inconsistent_schema_version_error,
            inconsistent_schema_version_used,
        ) = self._schema_object.get_inconsistent_schema_version_used_for_statement(
            statement
        )
        if inconsistent_schema_version_error:
            self._additional_check_results.append(
                {
                    "type": "inconsistent_schema_version_used",
                    "schema_version": inconsistent_schema_version_used,
                    "statement_type": "ownership_or_control",
                    "statement": statement.get("statementID"),
                }
            )
        if self._schema_object.schema_version != "0.1":
            if (
                "isComponent" in statement
                and statement["isComponent"]
                and "componentStatementIDs" in statement
                and statement["componentStatementIDs"]
            ):
                self._additional_check_results.append(
                    {
                        "type": "ownership_or_control_statement_has_is_compontent_and_component_statement_ids",
                        "statement": statement.get("statementID"),
                    }
                )
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_is_after_use_in_component_statement_id",
                        "statement_type": "ownership_or_control",
                        "statement": statement.get("statementID"),
                    }
                )
            if (
                "componentStatementIDs" in statement
                and not statement.get("isComponent")
                and isinstance(statement["componentStatementIDs"], list)
            ):
                self.statement_ids_seen_in_component_statement_ids.extend(
                    statement["componentStatementIDs"]
                )
        # If any interest has beneficialOwnershipOrControl then a person statement ID must be specified.
        interests = statement.get("interests", [])
        if isinstance(interests, list):
            interests_with_beneficialOwnershipOrControl = [
                i
                for i in interests
                if isinstance(i, dict) and i.get("beneficialOwnershipOrControl")
            ]
            if (
                len(interests_with_beneficialOwnershipOrControl) > 0
                and isinstance(statement.get("interestedParty", {}), dict)
                and not statement.get("interestedParty").get(
                    "describedByPersonStatement"
                )
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_beneficialOwnershipOrControl_but_no_person_specified",
                        "statement_type": "ownership_or_control",
                        "statement": statement.get("statementID"),
                    }
                )

    def check_entity_statement_second_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        if (
            statement.get("statementID")
            not in self.entity_statements_seen_in_ownership_or_control_statement
        ):
            self._additional_check_results.append(
                {
                    "type": "entity_statement_not_used_in_ownership_or_control_statement",
                    "entity_statement": statement.get("statementID"),
                }
            )
        if self._schema_object.schema_version != "0.1":
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                not in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_not_used_in_component_statement_ids",
                        "statement_type": "entity",
                        "statement": statement.get("statementID"),
                    }
                )

    def check_person_statement_second_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        if (
            statement.get("statementID")
            not in self.person_statements_seen_in_ownership_or_control_statement
        ):
            self._additional_check_results.append(
                {
                    "type": "person_statement_not_used_in_ownership_or_control_statement",
                    "person_statement": statement.get("statementID"),
                }
            )
        if self._schema_object.schema_version != "0.1":
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                not in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_not_used_in_component_statement_ids",
                        "statement_type": "person",
                        "statement": statement.get("statementID"),
                    }
                )

    def check_ownership_or_control_statement_second_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code, but this should be evaluated.
        if not statement.get("statementID"):
            return
        interested_party = statement.get("interestedParty")
        if isinstance(interested_party, dict):
            interested_party_described_by_entity_statement = interested_party.get(
                "describedByEntityStatement"
            )
            interested_party_described_by_person_statement = interested_party.get(
                "describedByPersonStatement"
            )
            if interested_party_described_by_entity_statement:
                if (
                    interested_party_described_by_entity_statement
                    not in self.entity_statements_seen
                ):
                    self._additional_check_results.append(
                        {
                            "type": "entity_statement_missing",
                            "missing_from": "interestedParty",
                            "entity_statement_missing": interested_party_described_by_entity_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
            if interested_party_described_by_person_statement:
                if (
                    interested_party_described_by_person_statement
                    not in self.person_statements_seen
                ):
                    self._additional_check_results.append(
                        {
                            "type": "person_statement_missing",
                            "missing_from": "interestedParty",
                            "person_statement_missing": interested_party_described_by_person_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
        subject = statement.get("subject")
        if isinstance(subject, dict):
            subject_described_by_entity_statement = subject.get(
                "describedByEntityStatement"
            )
            if subject_described_by_entity_statement:
                if (
                    subject_described_by_entity_statement
                    not in self.entity_statements_seen
                ):
                    self._additional_check_results.append(
                        {
                            "type": "entity_statement_missing",
                            "missing_from": "subject",
                            "entity_statement_missing": subject_described_by_entity_statement,
                            "seen_in_ownership_or_control_statement": statement.get(
                                "statementID"
                            ),
                        }
                    )
        if self._schema_object.schema_version != "0.1":
            if "componentStatementIDs" in statement and isinstance(
                statement["componentStatementIDs"], list
            ):
                for component_statement_id in statement["componentStatementIDs"]:
                    if (
                        component_statement_id not in self.person_statements_seen
                        and component_statement_id not in self.entity_statements_seen
                        and component_statement_id
                        not in self.ownership_or_control_statements_seen
                    ):
                        self._additional_check_results.append(
                            {
                                "type": "component_statement_id_not_in_package",
                                "component_statement_id": component_statement_id,
                                "seen_in_ownership_or_control_statement": statement.get(
                                    "statementID"
                                ),
                            }
                        )
            if (
                statement.get("isComponent")
                and statement.get("statementID")
                and statement.get("statementID")
                not in self.statement_ids_seen_in_component_statement_ids
            ):
                self._additional_check_results.append(
                    {
                        "type": "statement_is_component_but_not_used_in_component_statement_ids",
                        "statement_type": "ownership_or_control",
                        "statement": statement.get("statementID"),
                    }
                )

    def final_checks(self):
        # We have seen some possible out of order statements;
        # but earlier we weren't sure if they were "out of order" or "missing"!
        # Now we have other info, we can check and see which one they are.
        for possible_out_of_order_statement in self.possible_out_of_order_statements:
            if (
                possible_out_of_order_statement["type"]
                == "entity_statement_out_of_order"
            ):
                if (
                    possible_out_of_order_statement["entity_statement_out_of_order"]
                    in self.entity_statements_seen
                ):
                    self._additional_check_results.append(
                        possible_out_of_order_statement
                    )
            else:
                if (
                    possible_out_of_order_statement["person_statement_out_of_order"]
                    in self.person_statements_seen
                ):
                    self._additional_check_results.append(
                        possible_out_of_order_statement
                    )

        # We can now look for duplicate IDs!
        self.statement_ids_counted = {}
        self._add_statement_ids_to_statement_ids_counted(self.person_statements_seen)
        self._add_statement_ids_to_statement_ids_counted(self.entity_statements_seen)
        self._add_statement_ids_to_statement_ids_counted(
            self.ownership_or_control_statements_seen
        )
        for k, v in self.statement_ids_counted.items():
            if v > 1:
                self._additional_check_results.append(
                    {
                        "type": "duplicate_statement_id",
                        "id": k,
                        "count": v,
                    }
                )

    def _add_statement_ids_to_statement_ids_counted(self, statement_ids):
        for statement_id in statement_ids:
            if statement_id in self.statement_ids_counted:
                self.statement_ids_counted[statement_id] += 1
            else:
                self.statement_ids_counted[statement_id] = 1

    def _check_addresses_list_for_alternatives(self, statement):
        # Does this addresses list have any alternative?
        found_alternative = False
        for address in statement["addresses"]:
            if "type" in address and address["type"] == "alternative":
                found_alternative = True

        if not found_alternative:
            return

        # It does! Well, if it has an alternative it must have another address that is not an alternative
        found_non_alternative = False
        for address in statement["addresses"]:
            if "type" in address and address["type"] != "alternative":
                found_non_alternative = True

        if not found_non_alternative:
            self._additional_check_results.append(
                {
                    "type": "alternative_address_with_no_other_address_types",
                    "statement_type": (
                        "person"
                        if statement.get("statementType") == "personStatement"
                        else "entity"
                    ),
                    "statement": statement.get("statementID"),
                }
            )


class CheckHasPublicListing(AdditionalCheck):
    def does_apply_to_schema(self):
        return self._schema_object.is_schema_version_equal_to_or_greater_than("0.3")

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
    def does_apply_to_schema(self):
        return self._schema_object.is_schema_version_equal_to_or_greater_than("0.3")

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
        self.mics_data = None

    def does_apply_to_schema(self):
        return self._schema_object.is_schema_version_equal_to_or_greater_than("0.3")

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


class PEPForSchema02Only(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_person_statements_have_pep_status = 0
        # Schema 0.2 only has a boolean, but we are going to map them to these 2 values taken from schema 0.3
        self.count_person_statements_have_pep_status_statuses = {
            "isPep": 0,
            "isNotPep": 0,
        }

        self.count_person_statements_have_pep_status_and_reason_missing_info = 0

    def does_apply_to_schema(self):
        return self._schema_object.schema_version == "0.2"

    def check_person_statement_first_pass(self, statement):
        if "hasPepStatus" in statement:
            self.count_person_statements_have_pep_status += 1
            if statement["hasPepStatus"]:
                self.count_person_statements_have_pep_status_statuses["isPep"] += 1
            else:
                self.count_person_statements_have_pep_status_statuses["isNotPep"] += 1
        if isinstance(statement.get("pepStatusDetails"), list):
            details_no_missing_info = [
                x
                for x in statement.get("pepStatusDetails")
                if not x.get("missingInfoReason")
            ]
            if details_no_missing_info and not statement["hasPepStatus"]:
                self._additional_check_results.append(
                    {
                        "type": "has_pep_details_without_missing_info_but_incorrect_pep_status",
                        "statement_type": "person",
                        "statement": statement.get("statementID"),
                    }
                )
            details_with_missing_info = [
                x
                for x in statement.get("pepStatusDetails")
                if x.get("missingInfoReason")
            ]
            if details_with_missing_info and statement["hasPepStatus"]:
                self._additional_check_results.append(
                    {
                        "type": "has_pep_details_with_missing_info_but_incorrect_pep_status",
                        "statement_type": "person",
                        "statement": statement.get("statementID"),
                    }
                )

    def get_statistics(self):
        return {
            "count_person_statements_have_pep_status": self.count_person_statements_have_pep_status,
            "count_person_statements_have_pep_status_statuses": self.count_person_statements_have_pep_status_statuses,
        }


class PEPForSchema03AndAbove(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_person_statements_have_pep_status = 0
        self.count_person_statements_have_pep_status_statuses = {}
        for (
            value
        ) in schema_object.get_person_statement_political_exposure_status_list():
            self.count_person_statements_have_pep_status_statuses[value] = 0

    def does_apply_to_schema(self):
        return self._schema_object.is_schema_version_equal_to_or_greater_than("0.3")

    def check_person_statement_first_pass(self, statement):
        if isinstance(statement.get("politicalExposure"), dict):
            status = statement["politicalExposure"].get("status")
            if status in self.count_person_statements_have_pep_status_statuses.keys():
                self.count_person_statements_have_pep_status += 1
                self.count_person_statements_have_pep_status_statuses[status] += 1
            has_pep_details_with_missing_info_but_incorrect_pep_status = False
            details = statement["politicalExposure"].get("details")
            if isinstance(details, list):
                details_with_missing_info = [
                    x for x in details if x.get("missingInfoReason")
                ]
                if details_with_missing_info and status != "unknown":
                    has_pep_details_with_missing_info_but_incorrect_pep_status = True
                    self._additional_check_results.append(
                        {
                            "type": "has_pep_details_with_missing_info_but_incorrect_pep_status",
                            "statement_type": "person",
                            "statement": statement.get("statementID"),
                        }
                    )
            if (
                details
                and (not status or status == "isNotPep")
                and not has_pep_details_with_missing_info_but_incorrect_pep_status
            ):
                # This check is a less specific version of has_pep_details_with_missing_info_but_incorrect_pep_status
                # so if that one has already been issued then we want to skip this one.
                self._additional_check_results.append(
                    {
                        "type": "has_pep_details_but_incorrect_pep_status",
                        "statement_type": "person",
                        "statement": statement.get("statementID"),
                    }
                )

    def get_statistics(self):
        return {
            "count_person_statements_have_pep_status": self.count_person_statements_have_pep_status,
            "count_person_statements_have_pep_status_statuses": self.count_person_statements_have_pep_status_statuses,
        }


ADDITIONAL_CHECK_CLASSES = [
    LegacyChecks,
    CheckHasPublicListing,
    CheckEntityTypeAndEntitySubtypeAlign,
    CheckEntitySecurityListingsMICSCodes,
    LegacyStatistics,
    StatisticOwnershipOrControlInterestDirectOrIndirect,
    StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    PEPForSchema02Only,
    PEPForSchema03AndAbove,
]


def process_additional_checks(json_data, lib_cove_bods_config, schema_object):
    additional_check_instances = [
        x(lib_cove_bods_config, schema_object) for x in ADDITIONAL_CHECK_CLASSES
    ]
    additional_check_instances = [
        x for x in additional_check_instances if x.does_apply_to_schema()
    ]

    # First pass
    for statement in json_data:
        statement_type = statement.get("statementType")
        for additional_check_instance in additional_check_instances:
            additional_check_instance.check_statement_first_pass(statement)
        if statement_type == "entityStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_entity_statement_first_pass(statement)
        elif statement_type == "personStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_person_statement_first_pass(statement)
        elif statement_type == "ownershipOrControlStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_ownership_or_control_statement_first_pass(
                    statement
                )

    # Second Pass
    for statement in json_data:
        statement_type = statement.get("statementType")
        if statement_type == "entityStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_entity_statement_second_pass(statement)
        elif statement_type == "personStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_person_statement_second_pass(statement)
        elif statement_type == "ownershipOrControlStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_ownership_or_control_statement_second_pass(
                    statement
                )

    # Final checks
    for additional_check_instance in additional_check_instances:
        additional_check_instance.final_checks()

    # Get results
    additional_checks = []
    statistics = {}
    if schema_object.schema_error:
        additional_checks.append(schema_object.schema_error)
    for additional_check_instance in additional_check_instances:
        additional_checks.extend(
            additional_check_instance.get_additional_check_results()
        )
        statistics.update(additional_check_instance.get_statistics())
    return {"additional_checks": additional_checks, "statistics": statistics}
