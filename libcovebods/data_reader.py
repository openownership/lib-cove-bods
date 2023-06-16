import json

import ijson  # type: ignore


class DataReader:
    """Class to hold information on where to get data and provides methods to access it.

    This is then passed around to any code that wants access to data.

    This is done so that later we can add a get_iterator() function here
    that returns statements in a memory efficient way and code that can use
    an iterator (like Python Checks) can call get_iterator() and not get_all_data()
    """

    def __init__(
        self,
        filename,
        sample_mode=False,
        sample_mode_max_row_count_per_statement_type=50,
    ):
        self._filename = filename
        self._sample_mode = sample_mode
        self._sample_mode_max_row_count_per_statement_type = (
            sample_mode_max_row_count_per_statement_type
        )

    def get_all_data(self):
        # Which mode?
        if self._sample_mode:

            # Sample Mode
            sample_data = []
            count_statement_types = {
                "entityStatement": 0,
                "personStatement": 0,
                "ownershipOrControlStatement": 0,
            }
            count_unknown_statement_types = 0

            with open(self._filename, "rb") as fp:
                for statement in ijson.items(fp, "item"):
                    statementType = (
                        statement.get("statementType")
                        if isinstance(statement, dict)
                        and isinstance(statement.get("statementType"), str)
                        else "unknown"
                    )
                    if statementType in count_statement_types:
                        if (
                            count_statement_types[statementType]
                            < self._sample_mode_max_row_count_per_statement_type
                        ):
                            sample_data.append(statement)
                            count_statement_types[statementType] += 1
                    else:
                        if (
                            count_unknown_statement_types
                            < self._sample_mode_max_row_count_per_statement_type
                        ):
                            sample_data.append(statement)
                            count_unknown_statement_types += 1
                    if (
                        not count_unknown_statement_types
                        < self._sample_mode_max_row_count_per_statement_type
                        and not [
                            True
                            for k, v in count_statement_types.items()
                            if v < self._sample_mode_max_row_count_per_statement_type
                        ]
                    ):
                        break

            return sample_data

        else:

            # Full Mode
            with open(self._filename) as fp:
                return json.load(fp)
