import libcovebods.data_reader
import libcovebods.tasks.peps
from libcovebods.tasks.checks import (
    legacy_checks,
    pre_record_checks,
    record_based_checks,
)
from libcovebods.tasks.statistics import pre_record_statistics, record_based_statistics
from libcovebods.utils import get_statement_type

TASK_CLASSES = [
    legacy_checks.LegacyChecks,
    legacy_checks.LegacyChecksNeedingHistory,
    pre_record_checks.CheckHasPublicListing,
    record_based_checks.CheckHasPublicListingRecord,
    pre_record_checks.CheckEntityTypeAndEntitySubtypeAlign,
    pre_record_checks.CheckEntitySecurityListingsMICSCodes,
    record_based_checks.CheckEntitySecurityListingsMICSCodesRecord,
    record_based_checks.CheckSourceRetrievedAtFutureDate,
    record_based_checks.CheckStatementDateFutureDate,
    record_based_checks.CheckAnnotationCreationDateFutureDate,
    record_based_checks.CheckStatementPublicationDateFutureDate,
    record_based_checks.CheckStatementPersonDateOfDeathSane,
    record_based_checks.CheckStatementEntityFoundationDissolutionDates,
    record_based_checks.CheckStatementPersonBirthDateSensible,
    record_based_checks.CheckStatementRelationshipInterestsStartEndDates,
    record_based_checks.CheckStatementRelationshipInterestsShareValues,
    record_based_checks.CheckStatementDeclarationSubject,
    record_based_checks.CheckStatementIsComponent,
    record_based_checks.CheckStatementDuplicateStatementId,
    record_based_checks.CheckStatementSeries,
    record_based_checks.CheckStatementRelationshipParties,
    record_based_checks.CheckAnnotationStatementPointerTarget,
    record_based_checks.CheckStatementRelationshipInterests,
    record_based_checks.CheckStatementSerialisation,
    record_based_checks.CheckStatementPersonIdentifiersHaveCorrectScheme,
    record_based_checks.CheckStatementEntityIdentifiersHaveKnownScheme,
    pre_record_statistics.StatisticsCountEntityStatements,
    record_based_statistics.StatisticsCountEntityRecordStatements,
    pre_record_statistics.StatisticsCountPersonStatements,
    record_based_statistics.StatisticsCountPersonRecordStatements,
    pre_record_statistics.StatisticsCountOwnershipOrControlStatements,
    record_based_statistics.StatisticsCountOwnershipOrControlRecordStatements,
    pre_record_statistics.StatisticsCurrentOwnershipOrControlStatementsAndReplacesStatementsMissing,
    pre_record_statistics.StatisticAddress,
    record_based_statistics.StatisticRecordAddress,
    pre_record_statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    record_based_statistics.StatisticOwnershipOrControlRecordInterestDirectOrIndirect,
    pre_record_statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    record_based_statistics.StatisticOwnershipOrControlRecordWithAtLeastOneInterestBeneficial,
    record_based_statistics.StatisticDeclarationSubjects,
    record_based_statistics.StatisticsStatementsRecordStatus,
    libcovebods.tasks.peps.PEPForSchema02Only,
    libcovebods.tasks.peps.PEPForSchema03AndAbove,
    libcovebods.tasks.peps.PEPForSchema04AndAbove,
]

TASK_CLASSES_IN_SAMPLE_MODE = [
    legacy_checks.LegacyChecks,
    pre_record_checks.CheckHasPublicListing,
    record_based_checks.CheckHasPublicListingRecord,
    pre_record_checks.CheckEntityTypeAndEntitySubtypeAlign,
    pre_record_checks.CheckEntitySecurityListingsMICSCodes,
    record_based_checks.CheckEntitySecurityListingsMICSCodesRecord,
    record_based_checks.CheckSourceRetrievedAtFutureDate,
    record_based_checks.CheckStatementDateFutureDate,
    record_based_checks.CheckAnnotationCreationDateFutureDate,
    record_based_checks.CheckStatementPublicationDateFutureDate,
    record_based_checks.CheckStatementPersonDateOfDeathSane,
    record_based_checks.CheckStatementEntityFoundationDissolutionDates,
    record_based_checks.CheckStatementPersonBirthDateSensible,
    record_based_checks.CheckStatementRelationshipInterestsStartEndDates,
    record_based_checks.CheckStatementRelationshipInterestsShareValues,
    record_based_checks.CheckStatementDuplicateStatementId,
    record_based_checks.CheckAnnotationStatementPointerTarget,
    record_based_checks.CheckStatementRelationshipInterests,
    record_based_checks.CheckStatementPersonIdentifiersHaveCorrectScheme,
    record_based_checks.CheckStatementEntityIdentifiersHaveKnownScheme,
    pre_record_statistics.StatisticsCountEntityStatements,
    record_based_statistics.StatisticsCountEntityRecordStatements,
    pre_record_statistics.StatisticsCountPersonStatements,
    record_based_statistics.StatisticsCountPersonRecordStatements,
    pre_record_statistics.StatisticsCountOwnershipOrControlStatements,
    record_based_statistics.StatisticsCountOwnershipOrControlRecordStatements,
    pre_record_statistics.StatisticAddress,
    record_based_statistics.StatisticRecordAddress,
    pre_record_statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    record_based_statistics.StatisticOwnershipOrControlRecordInterestDirectOrIndirect,
    pre_record_statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    record_based_statistics.StatisticOwnershipOrControlRecordWithAtLeastOneInterestBeneficial,
    record_based_statistics.StatisticDeclarationSubjects,
    record_based_statistics.StatisticsStatementsRecordStatus,
    libcovebods.tasks.peps.PEPForSchema02Only,
    libcovebods.tasks.peps.PEPForSchema03AndAbove,
    libcovebods.tasks.peps.PEPForSchema04AndAbove,
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

    # If not list of statements put in list so that additional checks
    # can be run (jsonschema validation will handle reporting error)
    if not isinstance(all_data, list):
        all_data = [all_data]

    # First pass
    for statement in all_data:
        statement_type = get_statement_type(statement, schema_object)
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
        # statement_type = statement.get("statementType")
        statement_type = get_statement_type(statement, schema_object)
        for additional_check_instance in additional_check_instances:
            additional_check_instance.check_statement_second_pass(statement)
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
