import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from geni.internal.auth import Auth
from geni.internal.caller import Caller, flatten_dict, remove_none
from geni.internal.ratelimiter import RateLimiter
from tests.internal.fixtures import sampleProfile


@pytest.mark.parametrize(
    "d, expect",
    [
        ({}, {}),
        ({"a": None, "b": "c", "d": None}, {"b": "c"}),
    ]
)
def test_remove_none(d, expect):
    assert remove_none(d) == expect


def test_remove_none_returns_a_dict_copy():
    d = {"a": 1, "b": 2}
    result = remove_none(d)
    d.pop("b")
    assert result == {"a": 1, "b": 2}
    assert d != result


@pytest.mark.parametrize(
    "d, parent_key, expect",
    [
        pytest.param({}, "", {},
                     id="empty dict => empty dict"),

        pytest.param({}, "key", {},
                     id="empty dict with a parent key => empty dict"),

        pytest.param(sampleProfile["names"], "", {
            "en[first_name]": sampleProfile["names"]["en"]["first_name"],
            "en[last_name]": sampleProfile["names"]["en"]["last_name"],
            "es[first_name]": sampleProfile["names"]["es"]["first_name"],
            "es[last_name]": sampleProfile["names"]["es"]["last_name"],
        }, id="names dict with no parent key => flattened dict"),

        pytest.param(sampleProfile["names"], "names", {
            "names[en][first_name]": sampleProfile["names"]["en"]["first_name"],
            "names[en][last_name]": sampleProfile["names"]["en"]["last_name"],
            "names[es][first_name]": sampleProfile["names"]["es"]["first_name"],
            "names[es][last_name]": sampleProfile["names"]["es"]["last_name"],
        }, id="names dict with 'names' as a parent key => flattened dict with 'names' as a parent key"),
    ],
)
def test_flatten_dict(d, parent_key, expect):
    assert flatten_dict(d, parent_key) == expect


def test_flatten_dict_returns_a_dict_copy():
    d = {"key": "value"}
    result = flatten_dict(d)
    d.pop("key")
    assert result == {"key": "value"}
    assert d != result


def test___init__():
    caller = Caller(api_key="test_key")

    assert isinstance(caller._auth, Auth)
    assert isinstance(caller._ratelimiter, RateLimiter)
    assert caller._auth._api_key == "test_key"


@pytest.mark.parametrize(
    "url, kwargs, "
    "expect_method, expect_headers, expect_params",
    [
        pytest.param("https://api.com/a", {},
                     "get", None, None,
                     id="url only => all optional arguments are None"),
        pytest.param("https://api.com/b",
                     {"headers": {"Custom-Header": "value"}, "params": {"k": "v"}, "method": "post"},
                     "post", {"Custom-Header": "value"}, {"k": "v"},
                     id="post with headers and params => optional arguments are passed as is"),
        pytest.param("https://api.com/b", {"params": {"root": {"k": "v"}}},
                     "get", None, {"root[k]": "v"},
                     id="post with a dict that needs flattening => flattened dict in params"),
    ]
)
def test__call(url, kwargs, expect_method, expect_headers, expect_params):
    expected_response = json.dumps("test_response")

    with patch.object(Caller, "_raw_call", return_value=expected_response) as mock___call:
        caller = Caller(api_key="test_key")

        # url = "test_url"
        # headers = {"test_header": "test_value"}
        # params = {"p": "v", "none": None, "dict": {"key": "val"}}
        # method = "test_method"
        response = caller._call(url, **dict(kwargs))

        assert response == expected_response
        mock___call.assert_called_once_with(url, headers=expect_headers, params=expect_params, method=expect_method)


@pytest.mark.parametrize(
    "url, kwargs, "
    "access_token,"
    "expect_method, expect_headers, expect_params",
    [
        pytest.param("https://api.com/a", {},
                     "TOKEN_A",
                     "get", {"Authorization": "Bearer TOKEN_A"}, None,
                     id="url only => success"),
        pytest.param("https://api.com/a", {"headers": {"Authorization": "Bearer EXISTING_HEADER"}},
                     "TOKEN_A",
                     "get", {"Authorization": "Bearer EXISTING_HEADER"}, None,
                     id="pre-existing auth header => original auth header is kept"),
        pytest.param("https://api.com/b",
                     {"headers": {"Custom-Header": "value"}, "params": {"k": "v"}, "method": "post"},
                     "TOKEN_B",
                     "post", {"Custom-Header": "value", "Authorization": "Bearer TOKEN_B"}, {"k": "v"},
                     id="post with headers and params => success"),
    ]
)
def test__raw_call(url, kwargs, access_token, expect_method, expect_headers, expect_params):
    mock_response = requests.Response()
    mock_response.headers = {"X-API-Rate-Limit": "100"}

    mock_access_token = MagicMock(return_value=access_token)

    with patch("requests.request", return_value=mock_response) as mock_request, \
            patch.object(RateLimiter, "wait") as mock_wait, \
            patch.object(RateLimiter, "update") as mock_update, \
            patch.object(Auth, "access_token", new_callable=mock_access_token):
        caller = Caller(api_key="dummy-api-key")
        response = caller._raw_call(url, **dict(kwargs))

        assert response == mock_response
        mock_access_token.assert_called_once()
        mock_wait.assert_called_once()
        mock_request.assert_called_once_with(expect_method, url, headers=expect_headers, params=expect_params)
        mock_update.assert_called_once_with(mock_response.headers)
