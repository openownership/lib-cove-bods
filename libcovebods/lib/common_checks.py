from libcove.lib.common import get_orgids_prefixes
from libcovebods.lib.common import get_year_from_bods_birthdate_or_deathdate, is_interest_current
from collections import defaultdict


class GetStatistics:

    def __init__(self, json_data, lib_cove_bods_config, schema_object):
        self.json_data = json_data
        self.lib_cove_bods_config = lib_cove_bods_config
        self.schema_object = schema_object
        # These are variables used during the run - we need to init them here so the class works
        # We should also reset them at the start of the run function, incase the run function is called more than once
        self.count_addresses = 0
        self.count_addresses_with_postcode = 0
        self.count_addresses_with_country = 0
        self.count_addresses_with_postcode_duplicated_in_address = 0

    def run(self):
        # Initialise Variables to hold results
        # .... entities
        count_entity_statements = 0
        count_entity_statements_types = {}
        for value in self.schema_object.get_entity_statement_types_list():
            count_entity_statements_types[value] = 0
        count_entity_statements_types_with_any_identifier = count_entity_statements_types.copy()
        count_entity_statements_types_with_any_identifier_with_id_and_scheme = count_entity_statements_types.copy()
        # .... people
        count_person_statements = 0
        count_person_statements_types = {}
        for value in self.schema_object.get_person_statement_types_list():
            count_person_statements_types[value] = 0
        count_person_statements_have_pep_status = 0
        count_person_statements_have_pep_status_and_reason_missing_info = 0
        # .... ownership or control
        count_ownership_or_control_statement = 0
        count_ownership_or_control_statement_interested_party_with_person = 0
        count_ownership_or_control_statement_interested_party_with_entity = 0
        count_ownership_or_control_statement_interested_party_with_unspecified = 0
        count_ownership_or_control_statement_interest_statement_types = {}
        for value in self.schema_object.get_ownership_or_control_statement_interest_statement_types_list():
            count_ownership_or_control_statement_interest_statement_types[value] = 0
        count_replaces_statements_missing = 0
        statement_ids = set()
        current_statement_ids = set()
        count_ownership_or_control_statement_by_year = defaultdict(int)
        subject_statement_ids_by_year = defaultdict(set)
        count_ownership_or_control_statement_interested_party_with_entity_by_year = defaultdict(int)
        count_ownership_or_control_statement_interested_party_with_person_by_year = defaultdict(int)
        count_ownership_or_control_statement_interested_party_with_unspecified_by_year = defaultdict(int)
        # .... Others
        self.count_addresses = 0
        self.count_addresses_with_postcode = 0
        self.count_addresses_with_country = 0
        self.count_addresses_with_postcode_duplicated_in_address = 0

        # Process data one statement at a time
        for statement in self.json_data:
            statement_type = statement.get('statementType')
            if statement_type == 'entityStatement':
                count_entity_statements += 1
                if ('entityType' in statement and isinstance(statement['entityType'], str)
                        and statement['entityType'] in count_entity_statements_types):
                    count_entity_statements_types[statement['entityType']] += 1
                    if 'identifiers' in statement and isinstance(statement['identifiers'], list):
                        has_ids = False
                        has_ids_with_id_and_scheme = False
                        for identifier in statement['identifiers']:
                            if isinstance(identifier, dict):
                                has_ids = True
                                if ('scheme' in identifier and isinstance(identifier['scheme'], str)
                                        and identifier['scheme']
                                        and 'id' in identifier and isinstance(identifier['id'], str)
                                        and identifier['id']):
                                    has_ids_with_id_and_scheme = True

                        if has_ids:
                            count_entity_statements_types_with_any_identifier[statement['entityType']] += 1
                            if has_ids_with_id_and_scheme:
                                count_entity_statements_types_with_any_identifier_with_id_and_scheme[statement['entityType']] += 1 # noqa
                if 'addresses' in statement and isinstance(statement['addresses'], list):
                    for address in statement['addresses']:
                        self._process_address(address)
            elif statement_type == 'personStatement':
                count_person_statements += 1
                if ('personType' in statement and isinstance(statement['personType'], str)
                        and statement['personType'] in count_person_statements_types):
                    count_person_statements_types[statement['personType']] += 1
                if self.schema_object.schema_version != '0.1':
                    if 'hasPepStatus' in statement and statement['hasPepStatus']:
                        count_person_statements_have_pep_status += 1
                        if 'pepStatusDetails' in statement and isinstance(statement['pepStatusDetails'], list):
                            if [x for x in statement['pepStatusDetails'] if x.get('missingInfoReason')]:
                                count_person_statements_have_pep_status_and_reason_missing_info += 1
                if 'addresses' in statement and isinstance(statement['addresses'], list):
                    for address in statement['addresses']:
                        self._process_address(address)
                if 'placeOfBirth' in statement and isinstance(statement['placeOfBirth'], dict):
                    self._process_address(statement['placeOfBirth'])
                if 'placeOfResidence' in statement and isinstance(statement['placeOfResidence'], dict):
                    self._process_address(statement['placeOfResidence'])
            elif statement_type == 'ownershipOrControlStatement':
                try:
                    year = int(statement.get('statementDate', '').split('-')[0])
                except (ValueError, AttributeError):
                    year = None
                count_ownership_or_control_statement += 1
                interested_party = statement.get('interestedParty')
                if isinstance(interested_party, dict):
                    if interested_party.get('describedByEntityStatement'):
                        count_ownership_or_control_statement_interested_party_with_entity += 1
                        count_ownership_or_control_statement_interested_party_with_entity_by_year[year] += 1
                    if interested_party.get('describedByPersonStatement'):
                        count_ownership_or_control_statement_interested_party_with_person += 1
                        count_ownership_or_control_statement_interested_party_with_person_by_year[year] += 1
                    if (interested_party.get('unspecified') and isinstance(interested_party.get('unspecified'), dict)
                            and interested_party['unspecified'].get('reason')):
                        count_ownership_or_control_statement_interested_party_with_unspecified += 1
                        count_ownership_or_control_statement_interested_party_with_unspecified_by_year[year] += 1
                if 'interests' in statement and isinstance(statement['interests'], list):
                    for interest in statement['interests']:
                        if isinstance(interest, dict):
                            if ('type' in interest and isinstance(interest['type'], str)
                                    and interest['type'] in count_ownership_or_control_statement_interest_statement_types):  # noqa
                                count_ownership_or_control_statement_interest_statement_types[interest['type']] += 1
                            if is_interest_current(interest) and 'statementID' in statement:
                                current_statement_ids.add(statement['statementID'])

                if 'statementDate' in statement:
                    count_ownership_or_control_statement_by_year[year] += 1
                if ('subject' in statement and isinstance(statement['subject'], dict)
                        and 'describedByEntityStatement' in statement['subject']):
                    subject_statement_ids_by_year[year].add(statement['subject']['describedByEntityStatement'])
                if 'addresses' in statement and isinstance(statement['addresses'], list):
                    for address in statement['addresses']:
                        self._process_address(address)
            if isinstance(statement.get('replacesStatements'), list):
                for replaces_statement_id in statement.get('replacesStatements'):
                    if replaces_statement_id not in statement_ids:
                        count_replaces_statements_missing += 1
                    if replaces_statement_id in current_statement_ids:
                        current_statement_ids.remove(replaces_statement_id)
            if 'statementID' in statement:
                statement_ids.add(statement['statementID'])

        # Return Results
        data = {
            'count_entity_statements': count_entity_statements,
            'count_entity_statements_types': count_entity_statements_types,
            'count_entity_statements_types_with_any_identifier': count_entity_statements_types_with_any_identifier,
            'count_entity_statements_types_with_any_identifier_with_id_and_scheme': count_entity_statements_types_with_any_identifier_with_id_and_scheme,  # noqa
            'count_person_statements': count_person_statements,
            'count_person_statements_types': count_person_statements_types,
            'count_ownership_or_control_statement': count_ownership_or_control_statement,
            'count_ownership_or_control_statement_current': len(current_statement_ids),
            'count_ownership_or_control_statement_interested_party_with_person': count_ownership_or_control_statement_interested_party_with_person, # noqa
            'count_ownership_or_control_statement_interested_party_with_entity': count_ownership_or_control_statement_interested_party_with_entity, # noqa
            'count_ownership_or_control_statement_interested_party_with_unspecified': count_ownership_or_control_statement_interested_party_with_unspecified, # noqa
            'count_ownership_or_control_statement_interest_statement_types': count_ownership_or_control_statement_interest_statement_types,  # noqa
            'count_ownership_or_control_statement_by_year': count_ownership_or_control_statement_by_year,
            'count_ownership_or_control_statement_subject_by_year': {
                year: len(year_set) for year, year_set in subject_statement_ids_by_year.items()},
            'count_ownership_or_control_statement_interested_party_with_entity_by_year': count_ownership_or_control_statement_interested_party_with_entity_by_year, # noqa
            'count_ownership_or_control_statement_interested_party_with_person_by_year': count_ownership_or_control_statement_interested_party_with_person_by_year, # noqa
            'count_ownership_or_control_statement_interested_party_with_unspecified_by_year': count_ownership_or_control_statement_interested_party_with_unspecified_by_year, # noqa
            'count_replaces_statements_missing': count_replaces_statements_missing,  # noqa
            'count_addresses': self.count_addresses,
            'count_addresses_with_postcode': self.count_addresses_with_postcode,
            'count_addresses_with_country': self.count_addresses_with_country,
            'count_addresses_with_postcode_duplicated_in_address': self.count_addresses_with_postcode_duplicated_in_address,  # noqa
        }
        if self.schema_object.schema_version != '0.1':
            data['count_person_statements_have_pep_status'] = count_person_statements_have_pep_status
            data['count_person_statements_have_pep_status_and_reason_missing_info'] = \
                count_person_statements_have_pep_status_and_reason_missing_info
        return data

    def _process_address(self, address):
        self.count_addresses += 1
        if address.get('postCode'):
            self.count_addresses_with_postcode += 1
        if address.get('country'):
            self.count_addresses_with_country += 1
        if address.get('postCode') and address.get('address') \
                and isinstance(address.get('postCode'), str) and isinstance(address.get('address'), str) \
                and address.get('postCode').lower() in address.get('address').lower():
            self.count_addresses_with_postcode_duplicated_in_address += 1


class RunAdditionalChecks:

    def __init__(self, json_data, lib_cove_bods_config, schema_object):
        self.json_data = json_data
        self.lib_cove_bods_config = lib_cove_bods_config
        self.schema_object = schema_object
        self.person_statements_seen = []
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.ownership_or_control_statements_seen = []
        self.statement_ids_seen_in_component_statement_ids = []
        self.output = []
        self.possible_out_of_order_statements = []
        self.orgids_prefixes = []
        self.statement_ids_counted = {}

    def run(self):
        self.person_statements_seen = []
        self.person_statements_seen_in_ownership_or_control_statement = []
        self.entity_statements_seen = []
        self.entity_statements_seen_in_ownership_or_control_statement = []
        self.ownership_or_control_statements_seen = []
        self.statement_ids_seen_in_component_statement_ids = []
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

        # We have seen some possible out of order statements;
        # but earlier we weren't sure if they were "out of order" or "missing"!
        # Now we have other info, we can check and see which one they are.
        for possible_out_of_order_statement in self.possible_out_of_order_statements:
            if possible_out_of_order_statement['type'] == 'entity_statement_out_of_order':
                if possible_out_of_order_statement['entity_statement_out_of_order'] in self.entity_statements_seen:
                    self.output.append(possible_out_of_order_statement)
            else:
                if possible_out_of_order_statement['person_statement_out_of_order'] in self.person_statements_seen:
                    self.output.append(possible_out_of_order_statement)

        # We can now look for duplicate IDs!
        self.statement_ids_counted = {}
        self._add_statement_ids_to_statement_ids_counted(self.person_statements_seen)
        self._add_statement_ids_to_statement_ids_counted(self.entity_statements_seen)
        self._add_statement_ids_to_statement_ids_counted(self.ownership_or_control_statements_seen)
        for k, v in self.statement_ids_counted.items():
            if v > 1:
                self.output.append({
                    'type': 'duplicate_statement_id',
                    'id': k,
                    'count': v,
                })

        return self.output

    def _check_entity_statement_first_pass(self, statement):
        self.entity_statements_seen.append(statement.get('statementID'))
        identifiers = statement.get('identifiers')
        if isinstance(identifiers, list):
            for identifier in identifiers:
                if isinstance(identifier, dict):
                    if ('scheme' in identifier and identifier['scheme']
                            and not identifier['scheme'] in self.orgids_prefixes):
                        self.output.append({
                            'type': 'entity_identifier_scheme_not_known',
                            'scheme': identifier.get('scheme'),
                            'entity_statement': statement.get('statementID'),
                        })
        schema_version, throw_away_1, throw_away_2 = self.schema_object.get_schema_version_of_statement(statement)
        if self.schema_object.schema_version != schema_version:
            self.output.append({
                'type': 'inconsistent_schema_version_used',
                'schema_version': schema_version,
                'statement_type': 'entity',
                'statement': statement.get('statementID'),
            })
        if self.schema_object.schema_version != '0.1':
            if 'addresses' in statement and isinstance(statement['addresses'], list):
                self._check_addresses_list_for_alternatives(statement)
                for address in statement['addresses']:
                    if 'type' in address and address['type'] not in \
                            self.schema_object.get_address_types_allowed_in_entity_statement():
                        self.output.append({
                            'type': 'wrong_address_type_used',
                            'address_type': address['type'],
                            'statement_type': 'entity',
                            'statement': statement.get('statementID'),
                        })
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_is_after_use_in_component_statement_id',
                    'statement_type': 'entity',
                    'statement': statement.get('statementID'),
                })

    def _check_person_statement_first_pass(self, statement):
        self.person_statements_seen.append(statement.get('statementID'))
        if 'birthDate' in statement:
            birth_year = get_year_from_bods_birthdate_or_deathdate(statement['birthDate'])
            if birth_year:
                if birth_year < self.lib_cove_bods_config.config['bods_additional_checks_person_birthdate_min_year']:
                    self.output.append({
                        'type': 'person_birth_year_too_early',
                        'year': birth_year,
                        'person_statement': statement.get('statementID'),
                    })
                elif birth_year > self.lib_cove_bods_config.config['bods_additional_checks_person_birthdate_max_year']:
                    self.output.append({
                        'type': 'person_birth_year_too_late',
                        'year': birth_year,
                        'person_statement': statement.get('statementID'),
                    })
        schema_version, throw_away_1, throw_away_2 = self.schema_object.get_schema_version_of_statement(statement)
        if self.schema_object.schema_version != schema_version:
            self.output.append({
                'type': 'inconsistent_schema_version_used',
                'schema_version': schema_version,
                'statement_type': 'person',
                'statement': statement.get('statementID'),
            })
        if self.schema_object.schema_version != '0.1':
            if 'addresses' in statement and isinstance(statement['addresses'], list):
                self._check_addresses_list_for_alternatives(statement)
                for address in statement['addresses']:
                    if 'type' in address and address['type'] not in \
                            self.schema_object.get_address_types_allowed_in_person_statement():
                        self.output.append({
                            'type': 'wrong_address_type_used',
                            'address_type': address['type'],
                            'statement_type': 'person',
                            'statement': statement.get('statementID'),
                        })
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_is_after_use_in_component_statement_id',
                    'statement_type': 'person',
                    'statement': statement.get('statementID'),
                })

    def _check_ownership_or_control_statement_first_pass(self, statement):
        self.ownership_or_control_statements_seen.append(statement.get('statementID'))
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
        schema_version, throw_away_1, throw_away_2 = self.schema_object.get_schema_version_of_statement(statement)
        if self.schema_object.schema_version != schema_version:
            self.output.append({
                'type': 'inconsistent_schema_version_used',
                'schema_version': schema_version,
                'statement_type': 'ownership_or_control',
                'statement': statement.get('statementID'),
            })
        if self.schema_object.schema_version != '0.1':
            if 'isComponent' in statement and statement['isComponent'] \
                    and 'componentStatementIDs' in statement and statement['componentStatementIDs']:
                self.output.append({
                    'type': 'ownership_or_control_statement_has_is_compontent_and_component_statement_ids',
                    'statement': statement.get('statementID'),
                })
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_is_after_use_in_component_statement_id',
                    'statement_type': 'ownership_or_control',
                    'statement': statement.get('statementID'),
                })
            if 'componentStatementIDs' in statement and not statement.get('isComponent') \
                    and isinstance(statement['componentStatementIDs'], list):
                self.statement_ids_seen_in_component_statement_ids.extend(statement['componentStatementIDs'])

    def _check_entity_statement_second_pass(self, statement):
        if statement.get('statementID') not in self.entity_statements_seen_in_ownership_or_control_statement:
            self.output.append({
                'type': 'entity_statement_not_used_in_ownership_or_control_statement',
                'entity_statement': statement.get('statementID'),
            })
        if self.schema_object.schema_version != '0.1':
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') not in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_not_used_in_component_statement_ids',
                    'statement_type': 'entity',
                    'statement': statement.get('statementID'),
                })

    def _check_person_statement_second_pass(self, statement):
        if statement.get('statementID') not in self.person_statements_seen_in_ownership_or_control_statement:
            self.output.append({
                'type': 'person_statement_not_used_in_ownership_or_control_statement',
                'person_statement': statement.get('statementID'),
            })
        if self.schema_object.schema_version != '0.1':
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') not in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_not_used_in_component_statement_ids',
                    'statement_type': 'person',
                    'statement': statement.get('statementID'),
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
        if self.schema_object.schema_version != '0.1':
            if 'componentStatementIDs' in statement and isinstance(statement['componentStatementIDs'], list):
                for component_statement_id in statement['componentStatementIDs']:
                    if component_statement_id not in self.person_statements_seen and \
                            component_statement_id not in self.entity_statements_seen and \
                            component_statement_id not in self.ownership_or_control_statements_seen:
                        self.output.append({
                            'type': 'component_statement_id_not_in_package',
                            'component_statement_id': component_statement_id,
                            'seen_in_ownership_or_control_statement': statement.get('statementID'),
                        })
            if statement.get('isComponent') and statement.get('statementID') \
                    and statement.get('statementID') not in self.statement_ids_seen_in_component_statement_ids:
                self.output.append({
                    'type': 'statement_is_component_but_not_used_in_component_statement_ids',
                    'statement_type': 'ownership_or_control',
                    'statement': statement.get('statementID'),
                })

    def _add_statement_ids_to_statement_ids_counted(self, statement_ids):
        for statement_id in statement_ids:
            if statement_id in self.statement_ids_counted:
                self.statement_ids_counted[statement_id] += 1
            else:
                self.statement_ids_counted[statement_id] = 1

    def _check_addresses_list_for_alternatives(self, statement):
        # Does this addresses list have any alternative?
        found_alternative = False
        for address in statement['addresses']:
            if 'type' in address and address['type'] == 'alternative':
                found_alternative = True

        if not found_alternative:
            return

        # It does! Well, if it has an alternative it must have another address that is not an alternative
        found_non_alternative = False
        for address in statement['addresses']:
            if 'type' in address and address['type'] != 'alternative':
                found_non_alternative = True

        if not found_non_alternative:
            self.output.append({
                'type': 'alternative_address_with_no_other_address_types',
                'statement_type': ('person' if statement.get('statementType') == 'personStatement' else 'entity'),
                'statement': statement.get('statementID'),
            })
