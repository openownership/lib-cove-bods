from libcove2.common import get_orgids_prefixes  # type: ignore

from libcovebods.base_task import AdditionalCheck
from libcovebods.utils import get_year_from_bods_birthdate_or_deathdate


class LegacyChecks(AdditionalCheck):
    """Before the AdditionalCheck system was implemented, all this code was together in one class.
    As we work on checks in this class, we should move them to seperate classes if possible.
    This now only has legacy checks that don't need to store a history.
    Ones that need to store history are in LegacyChecksNeedingHistory."""

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_less_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return [
            "entity_identifier_scheme_not_known",
            "inconsistent_schema_version_used",
            "wrong_address_type_used",
            "person_birth_year_too_early",
            "person_birth_year_too_late",
            "ownership_or_control_statement_has_is_compontent_and_component_statement_ids",
            "statement_is_beneficialOwnershipOrControl_but_no_person_specified",
            "alternative_address_with_no_other_address_types",
        ]

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.orgids_prefixes = get_orgids_prefixes()

    def check_entity_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
        if not statement.get("statementID"):
            return
        identifiers = statement.get("identifiers")
        if isinstance(identifiers, list):
            for identifier in identifiers:
                if isinstance(identifier, dict):
                    if (
                        "scheme" in identifier
                        and identifier["scheme"]
                        and identifier["scheme"] not in self.orgids_prefixes
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

    def check_person_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
        if not statement.get("statementID"):
            return
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

    def check_ownership_or_control_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
        if not statement.get("statementID"):
            return
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


class LegacyChecksNeedingHistory(AdditionalCheck):
    """Before the AdditionalCheck system was implemented, all this code was together in one class.
    As we work on checks in this class, we should move them to seperate classes if possible.
    This now only has legacy checks that need to store a history.
    Ones that don't need to store history are in LegacyChecks."""

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_less_than("0.4")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return [
            "statement_is_component_but_is_after_use_in_component_statement_id",
            "entity_statement_out_of_order",
            "person_statement_out_of_order",
            "entity_statement_not_used_in_ownership_or_control_statement",
            "statement_is_component_but_not_used_in_component_statement_ids",
            "person_statement_not_used_in_ownership_or_control_statement",
            "entity_statement_missing",
            "person_statement_missing",
            "component_statement_id_not_in_package",
            "duplicate_statement_id",
        ]

    def __init__(self, lib_cove_bods_config, schema_object):
        super().__init__(lib_cove_bods_config, schema_object)
        self.person_statements_seen = []
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.ownership_or_control_statements_seen = []
        self.statement_ids_seen_in_component_statement_ids = []
        self.possible_out_of_order_statements = []
        self.statement_ids_counted = {}

    def check_entity_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
        if not statement.get("statementID"):
            return
        self.entity_statements_seen.append(statement.get("statementID"))
        if self._schema_object.schema_version != "0.1":
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
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
        if not statement.get("statementID"):
            return
        self.person_statements_seen.append(statement.get("statementID"))

    def check_ownership_or_control_statement_first_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
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
        if self._schema_object.schema_version != "0.1":
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

    def check_entity_statement_second_pass(self, statement):
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
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
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
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
        # Not doing any work if no statementID preserves the old behaviour of the code,
        # but this should be evaluated.
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
