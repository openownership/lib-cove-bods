from collections import defaultdict

from libcovebods.base_task import AdditionalCheck
from libcovebods.utils import is_interest_current


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

    def check_person_statement_first_pass(self, statement):
        self.count_person_statements += 1
        if (
            "personType" in statement
            and isinstance(statement["personType"], str)
            and statement["personType"] in self.count_person_statements_types
        ):
            self.count_person_statements_types[statement["personType"]] += 1

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

    def get_statistics(self):
        data = {
            "count_entity_statements": self.count_entity_statements,
            "count_entity_statements_types": self.count_entity_statements_types,
            "count_entity_statements_types_with_any_identifier": self.count_entity_statements_types_with_any_identifier,
            "count_entity_statements_types_with_any_identifier_with_id_and_scheme": self.count_entity_statements_types_with_any_identifier_with_id_and_scheme,
            "count_person_statements": self.count_person_statements,
            "count_person_statements_types": self.count_person_statements_types,
            "count_ownership_or_control_statement": self.count_ownership_or_control_statement,
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
        }
        return data


class StatisticsCurrentOwnershipOrControlStatementsAndReplacesStatementsMissing(
    AdditionalCheck
):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_replaces_statements_missing = 0
        self.statement_ids = set()
        self.current_statement_ids = set()

    def check_statement_first_pass(self, statement):
        if isinstance(statement.get("replacesStatements"), list):
            for replaces_statement_id in statement.get("replacesStatements"):
                if replaces_statement_id not in self.statement_ids:
                    self.count_replaces_statements_missing += 1
                if replaces_statement_id in self.current_statement_ids:
                    self.current_statement_ids.remove(replaces_statement_id)
        if "statementID" in statement and isinstance(statement["statementID"], str):
            self.statement_ids.add(statement["statementID"])

    def check_ownership_or_control_statement_first_pass(self, statement):
        if (
            "interests" in statement
            and isinstance(statement["interests"], list)
            and "statementID" in statement
        ):
            for interest in statement["interests"]:
                if isinstance(interest, dict) and is_interest_current(interest):
                    self.current_statement_ids.add(statement["statementID"])

    def get_statistics(self):
        data = {
            "count_ownership_or_control_statement_current": len(
                self.current_statement_ids
            ),
            "count_replaces_statements_missing": self.count_replaces_statements_missing,
        }
        return data


class StatisticAddress(AdditionalCheck):
    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_addresses = 0
        self.count_addresses_with_postcode = 0
        self.count_addresses_with_country = 0
        self.count_addresses_with_postcode_duplicated_in_address = 0

    def check_entity_statement_first_pass(self, statement):
        if "addresses" in statement and isinstance(statement["addresses"], list):
            for address in statement["addresses"]:
                self._process_address(address)

    def check_person_statement_first_pass(self, statement):
        if "addresses" in statement and isinstance(statement["addresses"], list):
            for address in statement["addresses"]:
                self._process_address(address)
        if "placeOfBirth" in statement and isinstance(statement["placeOfBirth"], dict):
            self._process_address(statement["placeOfBirth"])
        if "placeOfResidence" in statement and isinstance(
            statement["placeOfResidence"], dict
        ):
            self._process_address(statement["placeOfResidence"])

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
            "count_addresses": self.count_addresses,
            "count_addresses_with_postcode": self.count_addresses_with_postcode,
            "count_addresses_with_country": self.count_addresses_with_country,
            "count_addresses_with_postcode_duplicated_in_address": self.count_addresses_with_postcode_duplicated_in_address,
        }
        return data


class StatisticOwnershipOrControlInterestDirectOrIndirect(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.3")

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
