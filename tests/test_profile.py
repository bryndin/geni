import pytest

from geni.profile import Profile

from tests.fixtures import dummyResponse, noneProfile, sampleProfile
from tests.internal.helper import check_api_method


@pytest.mark.parametrize(
    "args, kwargs,"
    "mock_returns, mock_raises,"
    "expect_response, expect_kwargs, expect_exception",
    [
        pytest.param(
            [], {}, 
            dummyResponse, None, 
            dummyResponse.json(), {"params": {"fields": None, "guids": None,  "only_ids": None}}, None,
            id="no params => success",
        ),
        pytest.param(
            [], {}, 
            None, Exception("test"), 
            dummyResponse.json(), {"params": {"fields": None, "guids": None,  "only_ids": None}}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [["name", "last_name"], 123, False], {},
            dummyResponse, None, 
            dummyResponse.json(), {"params": {"fields": ["name", "last_name"], "guids": 123,  "only_ids": False}}, None,
            id="pass sample params as args => success",
        ),
        pytest.param(
            [], {"fields":["name", "email"], "guids": 321,  "only_ids": True},
            dummyResponse, None, 
            dummyResponse.json(), {"params": {"fields": ["name", "email"], "guids": 321,  "only_ids": True}}, None,
            id="pass sample params as kwargs => success",
        ),
    ],
)
def test_profile(args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception):
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
def test_delete(args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception):
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
            dummyResponse.json(), {"params": {**noneProfile, "guid": 1}, "method": "post"}, None,
            id="no params => success expecting default None values",
        ),
        pytest.param(
            [2], {},
            None, Exception("boom"), 
            None, {"params": {**noneProfile, "guid": 2}, "method": "post"}, Exception,
            id="exception from call => raised exception",
        ),
        pytest.param(
            [3], sampleProfile,
            dummyResponse, None, 
            dummyResponse.json(), {"params": {**sampleProfile, "guid": 3}, "method": "post"}, None,
            id="pass all params from a sample profile => success expecting all passed values",
        ),
    ],
)
def test_update_basics(args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception):
    check_api_method(
        Profile, "update_basics", "https://www.geni.com/api/profile/update-basics", 
        args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception
    )
