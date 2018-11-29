

def get_statistics(json_data):
    count_entity_statements = 0
    count_person_statements = 0
    count_ownership_or_control_statement = 0
    count_ownership_or_control_statement_interested_party_with_person = 0
    count_ownership_or_control_statement_interested_party_with_entity = 0

    for statement in json_data:
        statement_type = statement.get('statementType')
        if statement_type == 'entityStatement':
            count_entity_statements += 1
        elif statement_type == 'personStatement':
            count_person_statements += 1
        elif statement_type == 'ownershipOrControlStatement':
            count_ownership_or_control_statement += 1
            interested_party = statement.get('interestedParty')
            if isinstance(interested_party, dict):
                if interested_party.get('describedByEntityStatement'):
                    count_ownership_or_control_statement_interested_party_with_entity += 1
                if interested_party.get('describedByPersonStatement'):
                    count_ownership_or_control_statement_interested_party_with_person += 1

    return {
        'count_entity_statements': count_entity_statements,
        'count_person_statements': count_person_statements,
        'count_ownership_or_control_statement': count_ownership_or_control_statement,
        'count_ownership_or_control_statement_interested_party_with_person': count_ownership_or_control_statement_interested_party_with_person, # noqa
        'count_ownership_or_control_statement_interested_party_with_entity': count_ownership_or_control_statement_interested_party_with_entity, # noqa
    }


class RunAdditionalChecks:

    def __init__(self, json_data):
        self.json_data = json_data
        self.person_statements_seen = []
        self.entity_statements_seen = []
        self.output = []

    def run(self):
        self.person_statements_seen = []
        self.entity_statements_seen = []
        self.output = []

        for statement in self.json_data:
            statement_type = statement.get('statementType')
            statement_id = statement.get('statementID')

            # TODO here check statement_id is a valid Id and raise alert if not!

            if statement_id:
                if statement_type == 'entityStatement':
                    self._check_entity_statement(statement)
                elif statement_type == 'personStatement':
                    self._check_person_statement(statement)
                elif statement_type == 'ownershipOrControlStatement':
                    self._check_ownership_or_control_statement(statement)

        return self.output

    def _check_entity_statement(self, statement):
        self.entity_statements_seen.append(statement.get('statementID'))

    def _check_person_statement(self, statement):
        self.person_statements_seen.append(statement.get('statementID'))

    def _check_ownership_or_control_statement(self, statement):
        interested_party = statement.get('interestedParty')
        if isinstance(interested_party, dict):
            interested_party_described_by_entity_statement = interested_party.get('describedByEntityStatement')
            interested_party_described_by_person_statement = interested_party.get('describedByPersonStatement')
            if interested_party_described_by_entity_statement:
                if interested_party_described_by_entity_statement not in self.entity_statements_seen:
                    self.output.append({
                        'type': 'entity_statement_missing',
                        'missing_from': 'interestedParty',
                        'entity_statement_missing': interested_party_described_by_entity_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })
            if interested_party_described_by_person_statement:
                if interested_party_described_by_person_statement not in self.person_statements_seen:
                    self.output.append({
                        'type': 'person_statement_missing',
                        'missing_from': 'interestedParty',
                        'person_statement_missing': interested_party_described_by_person_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })
        subject = statement.get('subject')
        if isinstance(subject, dict):
            subject_described_by_entity_statement = subject.get('describedByEntityStatement')
            if subject_described_by_entity_statement:
                if subject_described_by_entity_statement not in self.entity_statements_seen:
                    self.output.append({
                        'type': 'entity_statement_missing',
                        'missing_from': 'subject',
                        'entity_statement_missing': subject_described_by_entity_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })
