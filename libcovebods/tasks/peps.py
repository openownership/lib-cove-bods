from libcovebods.base_task import AdditionalCheck


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

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.schema_version == "0.2"

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return (
            [
                "has_pep_details_without_missing_info_but_incorrect_pep_status",
                "has_pep_details_with_missing_info_but_incorrect_pep_status",
            ]
            if schema_object.schema_version == "0.2"
            else []
        )

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

    @staticmethod
    def does_apply_to_schema(lib_cove_bods_config, schema_object) -> bool:
        return schema_object.is_schema_version_equal_to_or_greater_than("0.3")

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_bods_config, schema_object
    ) -> list:
        return (
            [
                "has_pep_details_with_missing_info_but_incorrect_pep_status",
                "has_pep_details_but_incorrect_pep_status",
            ]
            if schema_object.is_schema_version_equal_to_or_greater_than("0.3")
            else []
        )

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
