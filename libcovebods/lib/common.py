from dateutil import parser
from pytz import UTC
import datetime


def get_year_from_bods_birthdate_or_deathdate(data):
    if len(data) == 4:
        return int(data)
    if len(data) > 4 and data[4] == '-':
        return int(data[0:4])


def is_interest_current(interest):
    if 'endDate' in interest:
        try:
            nowUTC = datetime.datetime.now(UTC)
            endDate = parser.parse(interest['endDate'], default=nowUTC)
            if not endDate.tzinfo:
                endDate = endDate.replace(tzinfo=UTC)
            return endDate >= nowUTC
        except ValueError:
            return False
    else:
        return True
