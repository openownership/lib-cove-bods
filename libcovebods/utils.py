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
    if not isinstance(date_str, str):
        return None
    elif "-" in date_str or len(date_str) == 4:
        if date_str.count("-") < 2:
            if re.match(r"^[0-9]{4}$", date_str):
                return datetime.datetime.strptime(date_str, "%Y").date()
            elif re.match(r"^[0-9]{4}-[0-9]{1,2}$", date_str):
                return datetime.datetime.strptime(date_str, "%Y-%m").date()
        else:
            return datetime.datetime.fromisoformat(
                date_str.replace("Z", "+00:00")
            ).date()
    else:
        return None


def numeric_value(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def sort_by_date(list_with_date, index):
    out = []
    for item in list_with_date:
        date = parse_date_field(item[index])
        if date:
            new_item = item.copy()
            new_item[index] = date
            out.append(new_item)
    return sorted(out, key=lambda x: x[index])
