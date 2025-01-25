from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from requests.structures import CaseInsensitiveDict

from geni.internal.auth import Auth
from geni.internal.caller import Caller, flatten_dict, remove_none
from geni.internal.ratelimiter import RateLimiter
from tests.internal.fixtures.response import dummyResponse
from tests.internal.fixtures.profile import sampleParamsUpdateBasics


@pytest.mark.parametrize(
    "d, expect",
    [
        ({}, {}),
        ({"a": None, "b": "c", "d": None}, {"b": "c"}),
    ]
)
def test_remove_none(d: dict[Any, Any], expect: dict[Any, Any]) -> None:
    assert remove_none(d) == expect


def test_remove_none_returns_a_dict_copy() -> None:
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

        pytest.param(sampleParamsUpdateBasics["names"], "", {
            "en[first_name]": sampleParamsUpdateBasics["names"]["en"]["first_name"],
            "en[last_name]": sampleParamsUpdateBasics["names"]["en"]["last_name"],
            "es[first_name]": sampleParamsUpdateBasics["names"]["es"]["first_name"],
            "es[last_name]": sampleParamsUpdateBasics["names"]["es"]["last_name"],
        }, id="names dict with no parent key => flattened dict"),

        pytest.param(sampleParamsUpdateBasics["names"], "names", {
            "names[en][first_name]": sampleParamsUpdateBasics["names"]["en"]["first_name"],
            "names[en][last_name]": sampleParamsUpdateBasics["names"]["en"]["last_name"],
            "names[es][first_name]": sampleParamsUpdateBasics["names"]["es"]["first_name"],
            "names[es][last_name]": sampleParamsUpdateBasics["names"]["es"]["last_name"],
        }, id="names dict with 'names' as a parent key => flattened dict with 'names' as a parent key"),
    ],
)
def test_flatten_dict(d: dict[Any, Any], parent_key: str, expect: dict[Any, Any]) -> None:
    assert flatten_dict(d, parent_key) == expect


def test_flatten_dict_returns_a_dict_copy() -> None:
    d = {"key": "value"}
    result = flatten_dict(d)
    d.pop("key")
    assert result == {"key": "value"}
    assert d != result


def test___init__() -> None:
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
def test__call(url: str, kwargs: dict[str, Any],
               expect_method: str, expect_headers: dict[str, str], expect_params: dict[str, Any]) -> None:
    with patch.object(Caller, "_raw_call", return_value=dummyResponse) as mock___call:
        caller = Caller(api_key="test_key")
        response = caller._call(url, **dict(kwargs))

        assert response == dummyResponse
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
def test__raw_call(url: str, kwargs: dict[str, Any],
                   access_token: str,
                   expect_method: str, expect_headers: dict[str, str], expect_params: dict[str, Any]) -> None:
    mock_response = requests.Response()
    mock_response.headers = CaseInsensitiveDict({
        "X-API-Rate-Limit": "100",
        "X-API-Rate-Remaining": "1",
        "X-API-Rate-Window": "60",
    })

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
