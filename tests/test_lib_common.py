from libcovebods.lib.common import get_year_from_bods_birthdate_or_deathdate


def test_get_year_from_bods_birthdate_or_deathdate_1():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate('1961')


def test_get_year_from_bods_birthdate_or_deathdate_2():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate('1961-10')


def test_get_year_from_bods_birthdate_or_deathdate_3():
    assert 1961 == get_year_from_bods_birthdate_or_deathdate('1961-10-01')


def test_get_year_from_bods_birthdate_or_deathdate_bad_1():
    assert None == get_year_from_bods_birthdate_or_deathdate('') # noqa


def test_get_year_from_bods_birthdate_or_deathdate_bad_2():
    assert None == get_year_from_bods_birthdate_or_deathdate('61') # noqa