import datetime


def get_date_today() -> str:
    today = datetime.datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)

    date_today = f'{year}-{month}'

    return date_today


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
