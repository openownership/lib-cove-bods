import libcovebods.data_reader
import libcovebods.tasks.checks
import libcovebods.tasks.peps
import libcovebods.tasks.statistics

TASK_CLASSES = [
    libcovebods.tasks.checks.LegacyChecks,
    libcovebods.tasks.checks.LegacyChecksNeedingHistory,
    libcovebods.tasks.checks.CheckHasPublicListing,
    libcovebods.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
    libcovebods.tasks.checks.CheckEntitySecurityListingsMICSCodes,
    libcovebods.tasks.statistics.LegacyStatistics,
    libcovebods.tasks.statistics.StatisticsCurrentOwnershipOrControlStatementsAndReplacesStatementsMissing,
    libcovebods.tasks.statistics.StatisticAddress,
    libcovebods.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    libcovebods.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    libcovebods.tasks.peps.PEPForSchema02Only,
    libcovebods.tasks.peps.PEPForSchema03AndAbove,
]

TASK_CLASSES_IN_SAMPLE_MODE = [
    libcovebods.tasks.checks.LegacyChecks,
    libcovebods.tasks.checks.CheckHasPublicListing,
    libcovebods.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
    libcovebods.tasks.checks.CheckEntitySecurityListingsMICSCodes,
    libcovebods.tasks.statistics.LegacyStatistics,
    libcovebods.tasks.statistics.StatisticAddress,
    libcovebods.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    libcovebods.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    libcovebods.tasks.peps.PEPForSchema02Only,
    libcovebods.tasks.peps.PEPForSchema03AndAbove,
]


def process_additional_checks(
    data_reader: libcovebods.data_reader.DataReader,
    lib_cove_bods_config,
    schema_object,
    task_classes=TASK_CLASSES,
):
    additional_check_instances = [
        x(lib_cove_bods_config, schema_object)
        for x in task_classes
        if x.does_apply_to_schema(lib_cove_bods_config, schema_object)
    ]
    all_data = data_reader.get_all_data()

    # First pass
    for statement in all_data:
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
    for statement in all_data:
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
