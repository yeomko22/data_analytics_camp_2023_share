from datetime import datetime, timedelta


def get_dates_between(start_datetime: datetime, end_datetime):
    datestr_list = []
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        datestr_list.append(current_datetime.strftime("%Y%m%d"))
        current_datetime += timedelta(days=1)
    return datestr_list


if __name__ == '__main__':
    start = datetime(2022, 1, 1)
    end = datetime(2022, 12, 31)
    datestr_list = get_dates_between(start, end)
    print(datestr_list)
