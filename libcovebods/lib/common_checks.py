from libcove.lib.common import get_orgids_prefixes


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
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.output = []
        self.possible_out_of_order_statements = []
        self.orgids_prefixes = []

    def run(self):
        self.person_statements_seen = []
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.output = []
        self.possible_out_of_order_statements = []
        self.orgids_prefixes = get_orgids_prefixes()

        # First Pass
        for statement in self.json_data:
            statement_type = statement.get('statementType')
            statement_id = statement.get('statementID')

            # TODO here check statement_id is a valid Id and raise alert if not!

            if statement_id:
                if statement_type == 'entityStatement':
                    self._check_entity_statement_first_pass(statement)
                elif statement_type == 'personStatement':
                    self._check_person_statement_first_pass(statement)
                elif statement_type == 'ownershipOrControlStatement':
                    self._check_ownership_or_control_statement_first_pass(statement)

        # Second Pass
        for statement in self.json_data:
            statement_type = statement.get('statementType')
            statement_id = statement.get('statementID')

            # TODO here check statement_id is a valid Id

            if statement_id:
                if statement_type == 'entityStatement':
                    self._check_entity_statement_second_pass(statement)
                elif statement_type == 'personStatement':
                    self._check_person_statement_second_pass(statement)
                elif statement_type == 'ownershipOrControlStatement':
                    self._check_ownership_or_control_statement_second_pass(statement)

        # Turn checks into output
        for possible_out_of_order_statement in self.possible_out_of_order_statements:
            if possible_out_of_order_statement['type'] == 'entity_statement_out_of_order':
                if possible_out_of_order_statement['entity_statement_out_of_order'] in self.entity_statements_seen:
                    self.output.append(possible_out_of_order_statement)
            else:
                if possible_out_of_order_statement['person_statement_out_of_order'] in self.person_statements_seen:
                    self.output.append(possible_out_of_order_statement)

        return self.output

    def _check_entity_statement_first_pass(self, statement):
        self.entity_statements_seen.append(statement.get('statementID'))
        identifiers = statement.get('identifiers')
        if isinstance(identifiers, list):
            for identifier in identifiers:
                if isinstance(identifier, dict):
                    if not identifier.get('scheme') in self.orgids_prefixes:
                        self.output.append({
                            'type': 'entity_identifier_scheme_not_known',
                            'scheme': identifier.get('scheme'),
                            'entity_statement': statement.get('statementID'),
                        })

    def _check_person_statement_first_pass(self, statement):
        self.person_statements_seen.append(statement.get('statementID'))

    def _check_ownership_or_control_statement_first_pass(self, statement):
        interested_party = statement.get('interestedParty')
        if isinstance(interested_party, dict):
            interested_party_described_by_entity_statement = interested_party.get('describedByEntityStatement')
            interested_party_described_by_person_statement = interested_party.get('describedByPersonStatement')
            if interested_party_described_by_entity_statement:
                self.entity_statements_seen_in_ownership_or_control_statement.append(interested_party_described_by_entity_statement) # noqa
                if interested_party_described_by_entity_statement not in self.entity_statements_seen:
                    self.possible_out_of_order_statements.append({
                        'type': 'entity_statement_out_of_order',
                        'referenced_from': 'interestedParty',
                        'entity_statement_out_of_order': interested_party_described_by_entity_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })
            if interested_party_described_by_person_statement:
                self.person_statements_seen_in_ownership_or_control_statement.append(interested_party_described_by_person_statement) # noqa
                if interested_party_described_by_person_statement not in self.person_statements_seen:
                    self.possible_out_of_order_statements.append({
                        'type': 'person_statement_out_of_order',
                        'referenced_from': 'interestedParty',
                        'person_statement_out_of_order': interested_party_described_by_person_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })
        subject = statement.get('subject')
        if isinstance(subject, dict):
            subject_described_by_entity_statement = subject.get('describedByEntityStatement')
            if subject_described_by_entity_statement:
                self.entity_statements_seen_in_ownership_or_control_statement.append(subject_described_by_entity_statement) # noqa
                if subject_described_by_entity_statement not in self.entity_statements_seen:
                    self.possible_out_of_order_statements.append({
                        'type': 'entity_statement_out_of_order',
                        'referenced_from': 'subject',
                        'entity_statement_out_of_order': subject_described_by_entity_statement,
                        'seen_in_ownership_or_control_statement': statement.get('statementID'),
                    })

    def _check_entity_statement_second_pass(self, statement):
        if statement.get('statementID') not in self.entity_statements_seen_in_ownership_or_control_statement:
            self.output.append({
                'type': 'entity_statement_not_used_in_ownership_or_control_statement',
                'entity_statement': statement.get('statementID'),
            })

    def _check_person_statement_second_pass(self, statement):
        if statement.get('statementID') not in self.person_statements_seen_in_ownership_or_control_statement:
            self.output.append({
                'type': 'person_statement_not_used_in_ownership_or_control_statement',
                'person_statement': statement.get('statementID'),
            })

    def _check_ownership_or_control_statement_second_pass(self, statement):
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