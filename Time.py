import datetime as _dt
import time as _time
from dateutil import parser as _time_parser
import pytz as _pytz
from logger import logger


logger = logger.loggers()


class time_difference:
    def __init__(self, timedelta):
        self.timedelta = timedelta
        self._minutes = self.timedelta.total_seconds() / 60.0
        self._hours = self._minutes / 60.0

    def __call__(self):
        return self.timedelta

    @property
    def minutes(self):
        return int(self._minutes)

    @property
    def hours(self):
        return int(self._hours)

    @property
    def days(self):
        return self.timedelta.days

    @property
    def microseconds(self):
        return self.timedelta.microseconds

    @property
    def seconds(self):
        return self.timedelta.seconds

    @property
    def min(self):
        return self.timedelta.min

    @property
    def max(self):
        return self.timedelta.max

    @property
    def resolution(self):
        return self.timedelta.resolution

    def total_seconds(self):
        return self.timedelta.total_seconds()


class time_class:
    def __init__(self, unsorted_time):
        self.unsorted_time = unsorted_time
        time_sort = self.unsorted_time.split()
        self.weekday = time_sort[0]
        self.month = time_sort[1]
        self.day = time_sort[2]
        self.time = time_sort[3]
        self.year = time_sort[4]
        self.date = self.day + "-" + self.month + "-" + self.year

    # def elapsed(self, past):
    #    """Provides elapsed time since <past>."""
    #    t_split = past.time.split(":")
    #    result = (t_split[0] * 60 * 60 + t_split[1] * 60 + t_split[2])
    #    return None


def get_date(_date=None, timezone=None, format_="HR", just_result=False):
    """For timezone list please get the supported list from <pytz> python library.!!
    <format_>: "HR" (Human Readable) / "ISO"!!"""
    if not _date:
        if not timezone:
            req_date = _time_parser.parse(_time.asctime(_time.localtime())).astimezone()
        else:
            req_date = _time_parser.parse(_time.asctime(_time.localtime())).astimezone(
                _pytz.timezone(timezone)
            )
    else:
        if isinstance(_date, _dt.datetime):
            _date = _date.strftime("%m/%d/%Y")
        if not timezone:
            req_date = _time_parser.parse(_date).astimezone()
        else:
            req_date = _time_parser.parse(_date).astimezone(_pytz.timezone(timezone))

    result = time_class(req_date.ctime())

    if not just_result:
        if "hr" in format_.lower():
            return result.date + "/" + result.time
        if "iso" in format_.lower():
            return _time_parser.parse(result.date + "/" + result.time).isoformat()
        if "epoch" in format_.lower():
            return req_date.timestamp()
    else:
        return result


def database_column_name(**kwargs):
    date = get_date(
        _date=kwargs.get("_date", None),
        timezone=kwargs.get("timezone", None),
        format_=kwargs.get("format_", "HR"),
        just_result=True,
    )

    return str(date.time)


def current_hour_range():
    start_time = get_date()
    start_hour = start_time.split("/")[1].split(":")[0]
    if start_hour == "23":
        end_hour = "00"
    else:
        end_hour = str(int(start_hour) + 1)

    return start_hour + ":00:00--" + end_hour + ":00:00"


def get_time_diff(_date1=None, _date2=None, verbose=False):
    """Provides <datetime.timedelta> object. If timezone information is present then it doesn't matter if the timezones are different because the difference will be taken between there 'UTC' equivalents. If timezone info is not present then system local timezone is taken for 'UTC' conversion."""

    if not _date1:
        _date1 = _time.asctime(_time.localtime())

    if not _date2:
        _date2 = _time.asctime(_time.localtime())

    if isinstance(_date1, str):
        _date1 = _time_parser.parse(_date1)
        if verbose:
            logger["WARNING"].logger.warning(
                "1st Date '{}' is of '{}' timezone given in 'str' format. Converting to 'UTC'.".format(
                    _date1.ctime(), _date1.tzname()
                )
            )
        _date1 = _date1.astimezone(_pytz.timezone("UTC"))
        if verbose:
            logger["WARNING"].logger.warning(
                "Converted 1st Date: {}".format(_date1.ctime())
            )

    elif "datetime" in str(type(_date1)):
        _date1 = _time_parser.parse(_date1.ctime())
        if verbose:
            logger["WARNING"].logger.warning(
                "1st Date '{}' is of '{}' timezone given in 'datetime' format. Converting to 'UTC'.".format(
                    _date1.ctime(), _date1.tzname()
                )
            )
        _date1 = _date1.astimezone(_pytz.timezone("UTC"))
        if verbose:
            logger["WARNING"].logger.warning(
                "Converted 1st Date: {}".format(_date1.ctime())
            )

    else:
        logger["ERROR"].logger.error(
            "Date should either be a <str> or <datetime> object. Please recheck!!"
        )

    if isinstance(_date2, str):
        _date2 = _time_parser.parse(_date2)
        if verbose:
            logger["WARNING"].logger.warning(
                "2nd Date '{}' is of '{}' timezone given in 'str' format. Converting to 'UTC'.".format(
                    _date2.ctime(), _date2.tzname()
                )
            )
        _date2 = _date2.astimezone(_pytz.timezone("UTC"))
        if verbose:
            logger["WARNING"].logger.warning(
                "Converted 2nd Date: {}".format(_date2.ctime())
            )

    elif "datetime" in str(type(_date2)):
        _date2 = _time_parser.parse(_date2.ctime())
        if verbose:
            logger["WARNING"].logger.warning(
                "2nd Date '{}' is of '{}' timezone given in 'datetime' format. Converting to 'UTC'.".format(
                    _date2.ctime(), _date2.tzname()
                )
            )
        _date2 = _date2.astimezone(_pytz.timezone("UTC"))
        if verbose:
            logger["WARNING"].logger.warning(
                "Converted 2nd Date: {}".format(_date2.ctime())
            )

    else:
        logger["ERROR"].logger.error(
            "Date should either be a <str> or <datetime> object. Please recheck!!"
        )

    if _date1 < _date2:
        diff = _date2 - _date1
    else:
        diff = _date1 - _date2

    return diff
    # return time_difference(diff)


def isdate(date):
    try:
        if isinstance(date, _dt.datetime):
            date = get_date(date)
        _time_parser.parse(date)
        return True
    except ValueError:
        return False


def track_pro(day_pro, today=get_date(), profit=0.0):
    if today not in day_pro.keys():
        day_pro = {today: 0}
    else:
        pass
    day_pro[today] = day_pro[today] + profit

    return day_pro
