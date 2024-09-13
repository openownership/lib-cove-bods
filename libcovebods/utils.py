import datetime
import re

from dateutil import parser
from pytz import UTC


def get_year_from_bods_birthdate_or_deathdate(data):
    if len(data) == 4:
        return int(data)
    if len(data) > 4 and data[4] == "-":
        return int(data[0:4])


def is_interest_current(interest):
    if "endDate" in interest:
        try:
            nowUTC = datetime.datetime.now(UTC)
            endDate = parser.parse(interest["endDate"], default=nowUTC)
            if not endDate.tzinfo:
                endDate = endDate.replace(tzinfo=UTC)
            return endDate >= nowUTC
        except ValueError:
            return False
    else:
        return True

def get_statement_type(statement, schema_object):
    if schema_object.is_schema_version_equal_to_or_greater_than("0.4"):
        record_type = statement.get("recordType")
        if record_type:
            if record_type == "relationship":
                return "ownershipOrControlStatement"
            else:
                return f"{record_type}Statement"
        else:
            return None
    else:
        return statement.get("statementType")

def parse_date_field(date_str):
    print(date_str)
    if "-" in date_str or len(date_str) == 4:
        if "T" in date_str:
            if "Z" in date_str:
                return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            else:
                return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        else:
            if re.match(r"^[0-9]{4}$", date_str):
                return datetime.datetime.strptime(date_str, "%Y")
            elif re.match(r"^[0-9]{4}-[0-9]{2}$", date_str):
                return datetime.datetime.strptime(date_str, "%Y-%m")
            else:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    else:
        return None
