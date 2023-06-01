import datetime


def get_month_today() -> str:
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)

    month_today = f'{year}-{month}'

    return month_today


def get_date_today() -> str:
    now = datetime.datetime.now()
    day_today = str(now).split()[0]

    return day_today


def months_spent(start_date: str, end_date: str):
    start_year = start_date[:4]
    end_year = end_date[:4]
    start_month = start_date[5:]
    end_month = end_date[5:]
    if end_year > start_year:
        months = [start_year + '-' + str(i).zfill(2) for i in range(int(start_month), 13)] + [
            end_year + '-' + str(i).zfill(2) for i in range(1, int(end_month) + 1)]
    else:
        months = [start_year + '-' + str(i).zfill(2) for i in range(int(start_month), int(end_month) + 1)]
    return months
