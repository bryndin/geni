from typing import Any

from geni.profile import Profile
import pytest

from tests.internal.fixtures.response import dummyResponse
from tests.internal.helper import check_api_method

from tests.internal.fixtures.profile import (
    noneParamsAddChild,
    sampleParamsAddChild,
    noneParamsAddParent,
    sampleParamsAddParent,
    noneParamsAddPartner,
    sampleParamsAddPartner,
    noneParamsAddSibling,
    sampleParamsAddSibling,
    noneParamsUpdateBasics,
    sampleParamsUpdateBasics,
)


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": None, "guids": None, "only_ids": None}}, None,
            id="no params => success",
        ),
        pytest.param(
            [], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {"fields": None, "guids": None, "only_ids": None}}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [["name", "last_name"], 123, False], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": ["name", "last_name"], "guids": 123, "only_ids": False}}, None,
            id="pass sample params as args => success",
        ),
        pytest.param(
            [], {"fields": ["name", "email"], "guids": 321, "only_ids": True},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"fields": ["name", "email"], "guids": 321, "only_ids": True}}, None,
            id="pass sample params as kwargs => success",
        ),
    ],
)
def test_profile(args: list[Any], kwargs: dict[str, Any],
                 mock_returns: Any, mock_raises: type[Exception] | None,
                 expect_response: Any, expect_kwargs: dict[str, Any], expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "profile", "https://www.geni.com/api/profile",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**noneParamsAddChild, "guid": 1}, "method": "post"}, None,
            id="no params => success",
        ),
        pytest.param(
            [2], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {**noneParamsAddChild, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], {**sampleParamsAddChild},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**sampleParamsAddChild, "guid": 3}, "method": "post"}, None,
            id="params from a sample profile => success",
        ),
    ],
)
def test_add_child(args: list[Any], kwargs: dict[str, Any],
                   mock_returns: Any, mock_raises: type[Exception] | None,
                   expect_response: Any, expect_kwargs: dict[str, Any],
                   expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "add_child", "https://www.geni.com/api/profile/add-child",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**noneParamsAddParent, "guid": 1}, "method": "post"}, None,
            id="no params => success",
        ),
        pytest.param(
            [2], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {**noneParamsAddParent, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], {**sampleParamsAddChild},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**sampleParamsAddParent, "guid": 3}, "method": "post"}, None,
            id="params from a sample profile => success",
        ),
    ],
)
def test_add_parent(args: list[Any], kwargs: dict[str, Any],
                    mock_returns: Any, mock_raises: type[Exception] | None,
                    expect_response: Any, expect_kwargs: dict[str, Any],
                    expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "add_parent", "https://www.geni.com/api/profile/add-parent",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**noneParamsAddPartner, "guid": 1}, "method": "post"}, None,
            id="no params => success",
        ),
        pytest.param(
            [2], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {**noneParamsAddPartner, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], {**sampleParamsAddChild},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**sampleParamsAddPartner, "guid": 3}, "method": "post"}, None,
            id="params from a sample profile => success",
        ),
    ],
)
def test_add_partner(args: list[Any], kwargs: dict[str, Any],
                     mock_returns: Any, mock_raises: type[Exception] | None,
                     expect_response: Any, expect_kwargs: dict[str, Any],
                     expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "add_partner", "https://www.geni.com/api/profile/add-partner",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**noneParamsAddSibling, "guid": 1}, "method": "post"}, None,
            id="no params => success",
        ),
        pytest.param(
            [2], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {**noneParamsAddSibling, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], {**sampleParamsAddChild},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**sampleParamsAddSibling, "guid": 3}, "method": "post"}, None,
            id="params from a sample profile => success",
        ),
    ],
)
def test_add_sibling(args: list[Any], kwargs: dict[str, Any],
                     mock_returns: Any, mock_raises: type[Exception] | None,
                     expect_response: Any, expect_kwargs: dict[str, Any],
                     expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "add_sibling", "https://www.geni.com/api/profile/add-sibling",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {"guids": 1}, "method": "post"}, None,
            id="no params => success",
        ),
        pytest.param(
            [2], {},
            None, Exception("test"),
            dummyResponse.json(), {"params": {"guids": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
    ],
)
def test_delete(args: list[Any], kwargs: dict[str, Any],
                mock_returns: Any, mock_raises: type[Exception] | None,
                expect_response: Any, expect_kwargs: dict[str, Any], expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "delete", "https://www.geni.com/api/profile/delete",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception,
    )


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [1], {},
            dummyResponse, None,
            dummyResponse.json(), {"params": {**noneParamsUpdateBasics, "guid": 1}, "method": "post"}, None,
            id="no params => success expecting default None values",
        ),
        pytest.param(
            [2], {},
            None, Exception("boom"),
            None, {"params": {**noneParamsUpdateBasics, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], sampleParamsUpdateBasics,
            dummyResponse, None,
            dummyResponse.json(), {"params": {**sampleParamsUpdateBasics, "guid": 3}, "method": "post"}, None,
            id="pass all params from a sample profile => success expecting all passed values",
        ),
    ],
)
def test_update_basics(args: list[Any], kwargs: dict[str, Any],
                       mock_returns: Any, mock_raises: type[Exception] | None,
                       expect_response: Any, expect_kwargs: dict[str, Any],
                       expect_exception: type[Exception] | None) -> None:
    check_api_method(
        Profile, "update_basics", "https://www.geni.com/api/profile/update-basics",
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )
