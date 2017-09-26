ISO_8601_DATE_FORMAT = "%Y-%m-%d"
ISO_8601_TIME_FORMAT = "%H:%M:%S"
ISO_8601_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def to_iso_datetime_string(value):
    """
    Format datetime value to ISO datetime format without timezone

    :type value: datetime.datetime
    :rtype: str
    """

    if value is None:
        return None

    return value.strftime(ISO_8601_DATETIME_FORMAT)


def to_iso_date_string(value):
    """
    Format datetime value to ISO date format without timezone

    :type value: datetime.datetime
    :rtype: str
    """

    if value is None:
        return None

    return value.strftime(ISO_8601_DATE_FORMAT)


def to_iso_time_string(value):
    """
    Format datetime value to ISO time format without timezone

    :type value: datetime.datetime
    :rtype: str
    """

    if value is None:
        return None

    return value.strftime(ISO_8601_TIME_FORMAT)


def from_iso(str_date):
    """:rtype: datetime.datetime"""

    if str_date is None:
        return None

    from dateutil import parser

    return parser.parse(str_date)
