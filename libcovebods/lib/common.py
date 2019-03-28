

def get_year_from_bods_birthdate_or_deathdate(data):
    if len(data) == 4:
        return int(data)
    if len(data) > 4 and data[4] == '-':
        return int(data[0:4])
