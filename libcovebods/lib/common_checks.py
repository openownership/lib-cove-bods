

def get_statistics(json_data):
    count_entity_statements = 0
    count_person_statements = 0
    count_ownership_or_control_statement = 0

    for statement in json_data:
        statement_type = statement.get('statementType')
        if statement_type == 'entityStatement':
            count_entity_statements += 1
        elif statement_type == 'personStatement':
            count_person_statements += 1
        elif statement_type == 'ownershipOrControlStatement':
            count_ownership_or_control_statement += 1

    return {
        'count_entity_statements': count_entity_statements,
        'count_person_statements': count_person_statements,
        'count_ownership_or_control_statement': count_ownership_or_control_statement,
    }
