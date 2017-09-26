def is_none_or_empty(value):
    """
    Check if value is None or empty
    :param value: string value
    :type value: str
    """

    if value is None:
        return True

    if type(value) is str:
        return len(value.strip()) == 0

    return False


def to_string(value, default_value=None):
    """
    Convert value to string or None
    :rtype: str
    """

    if is_none_or_empty(value):
        return default_value

    if type(value) is not str:
        return str(value)

    return value


def to_int(value, default_value=None):
    """
    Convert value to int or None
    :rtype: int or None
    """

    if is_none_or_empty(value):
        return default_value

    if type(value) is int:
        return value

    if type(value) is float:
        return int(value)

    if type(value) is not str:
        value = str(value)

    if not value.isnumeric():
        try:
            return int(float(value))
        except ValueError:
            return default_value

    try:
        return int(value)
    except ValueError or TypeError:
        return default_value


def to_float(value, default_value=None):
    """
    Convert value to float or None
    :rtype: float
    """

    if is_none_or_empty(value):
        return default_value

    if type(value) is float:
        return value

    if type(value) is not str:
        value = str(value)

    try:
        value = float(value)
    except ValueError:
        return default_value

    return value


def to_bool(value, default_value=False):
    """
    Convert value to boolean. True values: 1, True, 'true', 'yes' (case insensitive)
    :rtype: bool
    """

    if is_none_or_empty(value):
        return default_value

    if type(value) is bool:
        return value

    if type(value) is not str:
        value = str(value)

    true_values = ['yes', 'true', '1']

    if value.lower() in true_values:
        return True

    return default_value
