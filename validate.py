

def validate_date(date: str) -> bool:
    """check if date is a valid date"""
    if date == 'total' or date == 'today':
        return True
    if len(date) != 10:
        return False
    if date[4] not in '-/' or date[7] not in '-/':
        return False
    if not all({char in '1234567890-/' for char in date}):
        return False
    return True
