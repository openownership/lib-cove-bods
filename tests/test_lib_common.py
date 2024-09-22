import datetime

import dateutil.utils
from pytz import UTC

from libcovebods.utils import (
    get_year_from_bods_birthdate_or_deathdate,
    is_interest_current,
)


def test_get_year_from_bods_birthdate_or_deathdate_1():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate("1961")


def test_get_year_from_bods_birthdate_or_deathdate_2():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate("1961-10")


def test_get_year_from_bods_birthdate_or_deathdate_3():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate("1961-10-01")


def test_get_year_from_bods_birthdate_or_deathdate_bad_1():
    assert None == get_year_from_bods_birthdate_or_deathdate("")  # noqa


def test_get_year_from_bods_birthdate_or_deathdate_bad_2():
    assert None == get_year_from_bods_birthdate_or_deathdate("61")  # noqa


class TestIsInterestCurrent:
    def test_empty_dict(self):
        assert is_interest_current({}) is True

    def test_bad_endDate_value(self):
        assert is_interest_current({"endDate": "bad"}) is False

    def test_past_YYYY(self):
        assert is_interest_current({"endDate": "2018"}) is False

    def test_past_YYYY_MM(self):
        assert is_interest_current({"endDate": "2018-05"}) is False

    def test_past_date(self):
        assert is_interest_current({"endDate": "2018-05-07"}) is False

    def test_future_YYYY(self):
        assert is_interest_current({"endDate": "2112"}) is True

    def test_future_YYYY_MM(self):
        assert is_interest_current({"endDate": "2112-05"}) is True

    def test_future_date(self):
        assert is_interest_current({"endDate": "2112-05-07"}) is True

    def test_future_datetime(self):
        assert is_interest_current({"endDate": "2112-05-07T01:02:03.0004"}) is True

    def test_future_datetime_tz(self):
        assert is_interest_current({"endDate": "2112-05-07T01:02:03.0004+0900"}) is True

    def test_future_datetime_tzz(self):
        assert is_interest_current({"endDate": "2112-05-07T01:02:03.0004Z"}) is True

    def test_this_YYYY(self):
        assert (
            is_interest_current({"endDate": str(dateutil.utils.today(UTC).year)})
            is True
        )

    def test_this_YYYY_MM(self):
        today = dateutil.utils.today(UTC)
        assert is_interest_current({"endDate": f"{today.year}-{today.month}"}) is True

    def test_this_date(self):
        assert (
            is_interest_current({"endDate": str(dateutil.utils.today(UTC).date())})
            is True
        )

    def test_yesterday(self):
        assert (
            is_interest_current({"endDate": str(dateutil.utils.today(UTC).year - 1)})
            is False
        )

    def test_now(self):
        now = datetime.datetime.now(UTC)
        # Add a second because comparison is now instaneous
        now += datetime.timedelta(seconds=1)
        assert is_interest_current({"endDate": now.isoformat()}) is True

    def test_last_second(self):
        now = datetime.datetime.now(UTC)
        now -= datetime.timedelta(seconds=1)
        assert is_interest_current({"endDate": now.isoformat()}) is False

    def test_now_no_tz(self):
        now = datetime.datetime.now(UTC)
        now.replace(tzinfo=None)
        # Add a second because comparison is now instaneous
        now += datetime.timedelta(seconds=1)
        assert is_interest_current({"endDate": now.isoformat()}) is True

    def test_last_second_no_tz(self):
        now = datetime.datetime.now(UTC)
        now.replace(tzinfo=None)
        now -= datetime.timedelta(seconds=1)
        assert is_interest_current({"endDate": now.isoformat()}) is False
