import calendar, datetime


def utc_date_to_timestamp(year: int|str, month: int|str, day: int|str):
    date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    ts = calendar.timegm(date.timetuple())
    return ts