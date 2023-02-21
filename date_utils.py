import datetime


def get_date_today() -> str:
    today = datetime.datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)

    date_today = f'{year}-{month}'

    return date_today
