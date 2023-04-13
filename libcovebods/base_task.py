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
