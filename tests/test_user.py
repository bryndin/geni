from typing import Any

from geni.user import User
import requests
import pytest

from tests.internal.fixtures.response import dummyResponse
from tests.internal.helper import check_api_method


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": None, "page": None, "per_page": None}}, None,
            id="no params => success",
        ),
        pytest.param(
            [], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {"fields": None, "page": None, "per_page": None}}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [["name", "last_name"], 3, 10], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": ["name", "last_name"], "page": 3, "per_page": 10}}, None,
            id="pass sample params as args => success",
        ),
        pytest.param(
            [], {"fields": ["name", "email"], "page": 2, "per_page": 50},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": ["name", "email"], "page": 2, "per_page": 50}}, None,
            id="pass sample params as kwargs => success",
        ),
    ],
)
def test_managed_profiles(args: list[Any], kwargs: dict[str, Any],
                          mock_returns: requests.Response | None, mock_raises: type[Exception] | None,
                          expect_response: Any, expect_kwargs: dict[str, Any],
                          expect_exception: type[Exception] | None) -> None:
    check_api_method(
        User, "managed_profiles", "https://www.geni.com/api/user/managed-profiles",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )
