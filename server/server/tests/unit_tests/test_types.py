import pytest
from server.tools import types


def test_not_none_and_not_empty():
    correct_values = ['7', 7, 7.0, True, False]
    for value in correct_values:
        assert types.is_none_or_empty(value) == False


def test_none_or_empty():
    correct_values = [None, '', ' ']

    for value in correct_values:
        assert types.is_none_or_empty(value) == True


def test_to_string(mocked_is_none_or_empty):
    parameters = ['1', 1, 3.14, True]
    responses = ['1', '1', '3.14', 'True']
    values = zip(parameters, responses)

    for i, (param, resp) in enumerate(values):
        assert types.to_string(param) == resp
        assert mocked_is_none_or_empty.call_count == i + 1


def test_to_int(mocked_is_none_or_empty):
    parameters = ['1', '3.14', 'abc', True, False]
    responses = [1, 3, None, None, None]
    values = zip(parameters, responses)

    for i, (param, resp) in enumerate(values):
        assert types.to_int(param) == resp
        assert mocked_is_none_or_empty.call_count == i + 1


def test_to_float(mocked_is_none_or_empty):
    parameters = ['1', '3.14', '1', 'abc', True, False]
    responses = [1.0, 3.14, 1.0, None, None, None]
    values = zip(parameters, responses)

    for i, (param, resp) in enumerate(values):
        assert types.to_float(param) == resp
        assert mocked_is_none_or_empty.call_count == i + 1


def test_to_bool(mocked_is_none_or_empty):
    parameters = ['true', 'false', '1', '0', 'abc', True, False, 1, 314]
    responses = [True, False, True, False, False, True, False, True, False]
    values = zip(parameters, responses)

    for i, (param, resp) in enumerate(values):
        assert types.to_bool(param) == resp
        assert mocked_is_none_or_empty.call_count == i + 1


@pytest.fixture
def mocked_is_none_or_empty(mocker):
    mocked = mocker.patch('server.tools.types.is_none_or_empty')
    mocked.return_value = False

    return mocked
