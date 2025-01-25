from typing import Any

from geni.stats import Stats
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
            dummyResponse.json(), {}, None,
            id="no params => success",
        ),
        pytest.param(
            [], {},
            None, Exception("test"),
            dummyResponse.json(), {}, Exception,
            id="exception from call => raised exception",
        ),
    ],
)
def test_stats(args: list[Any], kwargs: dict[str, Any],
               mock_returns: Any, mock_raises: type[Exception] | None,
               expect_response: Any, expect_kwargs: dict[str, Any], expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Stats, "stats", "https://www.geni.com/api/stats",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [], {},
            dummyResponse, None,
            dummyResponse.json(), {}, None,
            id="no params => success",
        ),
        pytest.param(
            [], {},
            None, Exception("test"),
            dummyResponse.json(), {}, Exception,
            id="exception from call => raised exception",
        ),
    ],
)
def test_world_family_tree(args: list[Any], kwargs: dict[str, Any],
               mock_returns: Any, mock_raises: type[Exception] | None,
               expect_response: Any, expect_kwargs: dict[str, Any], expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Stats, "world_family_tree", "https://www.geni.com/api/stats/world-family-tree",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )
