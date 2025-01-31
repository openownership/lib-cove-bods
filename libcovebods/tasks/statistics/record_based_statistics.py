from collections import defaultdict

from libcovebods.base_task import AdditionalCheck


class StatisticsCountEntityRecordStatements(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
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

    def check_entity_statement_first_pass(self, statement):
        self.count_entity_statements += 1
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "entityType" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["entityType"], dict)
            and "type" in statement["recordDetails"]["entityType"]
            and isinstance(statement["recordDetails"]["entityType"]["type"], str)
            and statement["recordDetails"]["entityType"]["type"]
            in self.count_entity_statements_types
        ):
            self.count_entity_statements_types[
                statement["recordDetails"]["entityType"]["type"]
            ] += 1
            if "identifiers" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["identifiers"], list
            ):
                has_ids = False
                has_ids_with_id_and_scheme = False
                for identifier in statement["recordDetails"]["identifiers"]:
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
                        statement["recordDetails"]["entityType"]["type"]
                    ] += 1
                    if has_ids_with_id_and_scheme:
                        self.count_entity_statements_types_with_any_identifier_with_id_and_scheme[
                            statement["recordDetails"]["entityType"]["type"]
                        ] += 1

    def get_statistics(self):
        data = {
            "count_entity_statements": self.count_entity_statements,
            "count_entity_statements_types": self.count_entity_statements_types,
            "count_entity_statements_types_with_any_identifier": self.count_entity_statements_types_with_any_identifier,
            "count_entity_statements_types_with_any_identifier_with_id_and_scheme": self.count_entity_statements_types_with_any_identifier_with_id_and_scheme,
        }
        return data


class StatisticsCountPersonRecordStatements(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_person_statements = 0
        self.count_person_statements_types = {}
        for value in schema_object.get_person_statement_types_list():
            self.count_person_statements_types[value] = 0

    def check_person_statement_first_pass(self, statement):
        self.count_person_statements += 1
        if (
            "recordDetails" in statement
            and isinstance(statement["recordDetails"], dict)
            and "personType" in statement["recordDetails"]
            and isinstance(statement["recordDetails"]["personType"], str)
            and statement["recordDetails"]["personType"]
            in self.count_person_statements_types
        ):
            self.count_person_statements_types[
                statement["recordDetails"]["personType"]
            ] += 1

    def get_statistics(self):
        data = {
            "count_person_statements": self.count_person_statements,
            "count_person_statements_types": self.count_person_statements_types,
        }
        return data


class StatisticsCountOwnershipOrControlRecordStatements(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.entity_record_ids = []
        self.person_record_ids = []
        self.count_ownership_or_control_statement = 0
        self.count_ownership_or_control_statement_interested_party_with_person = 0
        self.count_ownership_or_control_statement_interested_party_with_entity = 0
        self.count_ownership_or_control_statement_interested_party_with_unspecified = 0
        self.count_ownership_or_control_statement_interested_party = 0
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
        self.count_ownership_or_control_statement_interested_party_by_year = (
            defaultdict(int)
        )

    def check_entity_statement_first_pass(self, statement):
        if "recordId" in statement:
            self.entity_record_ids.append(statement["recordId"])

    def check_person_statement_first_pass(self, statement):
        if "recordId" in statement:
            self.person_record_ids.append(statement["recordId"])

    def check_ownership_or_control_statement_first_pass(self, statement):
        try:
            year = int(statement.get("statementDate", "").split("-")[0])
        except (ValueError, AttributeError):
            year = None
        self.count_ownership_or_control_statement += 1
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            interested_party = statement["recordDetails"].get("interestedParty")
            if interested_party:
                self.count_ownership_or_control_statement_interested_party += 1
                self.count_ownership_or_control_statement_interested_party_by_year[
                    year
                ] += 1
            if "interests" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interests"], list
            ):
                for interest in statement["recordDetails"]["interests"]:
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
            if "subject" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["subject"], str
            ):
                self.subject_statement_ids_by_year[year].add(
                    statement["recordDetails"]["subject"]
                )
        if "statementDate" in statement:
            self.count_ownership_or_control_statement_by_year[year] += 1

    def check_ownership_or_control_statement_second_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            interested_party = statement["recordDetails"].get("interestedParty")
            if interested_party:
                if interested_party in self.entity_record_ids:
                    self.count_ownership_or_control_statement_interested_party_with_entity += (
                        1
                    )
                if interested_party in self.person_record_ids:
                    self.count_ownership_or_control_statement_interested_party_with_person += (
                        1
                    )
                if isinstance(interested_party, dict):
                    self.count_ownership_or_control_statement_interested_party_with_unspecified += (
                        1
                    )

    def get_statistics(self):
        data = {
            "count_ownership_or_control_statement": self.count_ownership_or_control_statement,
            "count_ownership_or_control_statement_interested_party_with_person": self.count_ownership_or_control_statement_interested_party_with_person,
            "count_ownership_or_control_statement_interested_party_with_entity": self.count_ownership_or_control_statement_interested_party_with_entity,
            "count_ownership_or_control_statement_interested_party_with_unspecified": self.count_ownership_or_control_statement_interested_party_with_unspecified,
            "count_ownership_or_control_statement_interested_party": self.count_ownership_or_control_statement_interested_party,
            "count_ownership_or_control_statement_interest_statement_types": self.count_ownership_or_control_statement_interest_statement_types,
            "count_ownership_or_control_statement_by_year": self.count_ownership_or_control_statement_by_year,
            "count_ownership_or_control_statement_subject_by_year": {
                year: len(year_set)
                for year, year_set in self.subject_statement_ids_by_year.items()
            },
            "count_ownership_or_control_statement_interested_party_by_year": self.count_ownership_or_control_statement_interested_party_by_year,
        }
        return data


class StatisticsStatementsRecordStatus(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.records = {}
        self.missing_new_records = {}
        self.current_records_count = 0
        self.missing_new_records_count = 0

    def check_statement_first_pass(self, statement):
        if (
            isinstance(statement.get("recordStatus"), str)
            and isinstance(statement.get("recordId"), str)
            and statement.get("recordStatus") in ("new", "updated", "closed")
        ):
            if not statement.get("recordId") in self.records:
                if not statement.get("recordStatus") == "new":
                    self.missing_new_records[statement.get("recordId")] = statement.get(
                        "statementId"
                    )
            self.records[statement.get("recordId")] = statement.get("recordStatus")

    def final_checks(self):
        for record_id in self.records:
            if not self.records[record_id] == "closed":
                self.current_records_count += 1
        for record_id in self.missing_new_records:
            self.missing_new_records_count += 1

    def get_statistics(self):
        data = {
            "count_records_current": self.current_records_count,
            "count_new_records_missing": self.missing_new_records_count,
        }
        return data


class StatisticRecordAddress(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.count_addresses = 0
        self.count_addresses_with_postcode = 0
        self.count_addresses_with_country = 0
        self.count_addresses_with_postcode_duplicated_in_address = 0

    def check_entity_statement_first_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "addresses" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["addresses"], list
            ):
                for address in statement["recordDetails"]["addresses"]:
                    self._process_address(address)

    def check_person_statement_first_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "addresses" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["addresses"], list
            ):
                for address in statement["recordDetails"]["addresses"]:
                    self._process_address(address)
        if "placeOfBirth" in statement["recordDetails"] and isinstance(
            statement["recordDetails"]["placeOfBirth"], dict
        ):
            self._process_address(statement["recordDetails"]["placeOfBirth"])

    def _process_address(self, address):
        self.count_addresses += 1
        if isinstance(address, dict):
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


class StatisticOwnershipOrControlRecordInterestDirectOrIndirect(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

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
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "interests" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interests"], list
            ):
                for interest in statement["recordDetails"]["interests"]:
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


class StatisticOwnershipOrControlRecordWithAtLeastOneInterestBeneficial(
    AdditionalCheck
):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.stat = 0

    def check_ownership_or_control_statement_first_pass(self, statement):
        if "recordDetails" in statement and isinstance(
            statement["recordDetails"], dict
        ):
            if "interests" in statement["recordDetails"] and isinstance(
                statement["recordDetails"]["interests"], list
            ):
                interests_with_beneficialOwnershipOrControl = [
                    i
                    for i in statement["recordDetails"]["interests"]
                    if isinstance(i, dict) and i.get("beneficialOwnershipOrControl")
                ]
                if interests_with_beneficialOwnershipOrControl:
                    self.stat += 1

    def get_statistics(self):
        return {
            "count_ownership_or_control_statement_with_at_least_one_interest_beneficial": self.stat,
        }


class StatisticDeclarationSubjects(AdditionalCheck):
    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.4")

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self._declaration_subjects = {}

    def check_statement_first_pass(self, statement):
        if (
            "recordId" in statement
            and "declarationSubject" in statement
            and statement["recordId"] == statement["declarationSubject"]
        ):
            self._declaration_subjects[statement["recordId"]] = 1

    def get_statistics(self):
        return {
            "count_declaration_subjects": len(self._declaration_subjects),
        }
