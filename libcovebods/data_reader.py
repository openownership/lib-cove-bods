import json

class DataReader:

    def __init__(self, filename, sample_mode=False, sample_mode_max_row_count=50):
        self._filename = filename
        self._sample_mode = sample_mode
        self._sample_mode_max_row_count = sample_mode_max_row_count

    def get_all_data(self):
        # Load data
        with open(self._filename) as fp:
            data = json.load(fp)

        # Which mode?
        if self._sample_mode:

            # Sample Mode
            sample_data = []
            count_statement_types = {
                "entityStatement": 0,
                "personStatement": 0,
                "ownershipOrControlStatement": 0
            }
            for statement in data:
                if statement.get("statementType") in count_statement_types and count_statement_types[statement["statementType"]] < self._sample_mode_max_row_count:
                    sample_data.append(statement)
                    count_statement_types[statement["statementType"]] += 1

            return sample_data

        else:

            # Full Mode
            return data
