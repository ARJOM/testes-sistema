from datetime import datetime


def get_age(date):
    now = datetime.now()
    birthday = datetime.strptime(date, "%Y-%m-%d")
    return abs((now.year - birthday.year) - ((now.month, now.day) < (birthday.month, birthday.day)))
