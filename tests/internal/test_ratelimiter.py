from collections import deque
from unittest.mock import Mock, call, patch

import pytest
from requests.structures import CaseInsensitiveDict

from geni.internal.ratelimiter import RateLimiter


def test_initialization() -> None:
    rate_limiter = RateLimiter(limit=5, window=60)

    assert rate_limiter.limit == 5
    assert rate_limiter.window == 60
    assert rate_limiter.remaining == -1
    assert rate_limiter.queue == deque()


@pytest.mark.parametrize(
    "limit, remaining, queue, mock_time, expect_sleep_calls",
    [
        # queue is full, but we were told we have one remaining call left
        (2, 1, [10, 20], Mock(), None),
        # queue has one call, but limit allows one extra
        (2, 0, [7], Mock(), None),
        # sleep 10-1=9s, expire 10; sleep 15-10=5s, expire 20
        (2, 0, [10, 20, 30], Mock(side_effect=[1, 15, 23]), [9, 5]),
    ],
)
def test_wait(limit: int, remaining: int, queue: list[int], mock_time: Mock,
              expect_sleep_calls: list[int] | None) -> None:
    rate_limiter = RateLimiter(limit=limit, window=60)
    rate_limiter.remaining = remaining
    rate_limiter.queue = deque(queue)

    with patch("time.time", new=mock_time), \
            patch("time.sleep") as mock_sleep:
        rate_limiter.wait()
        if expect_sleep_calls is not None:
            mock_sleep.assert_has_calls([call(x) for x in expect_sleep_calls])
        else:
            mock_sleep.assert_not_called()


@pytest.mark.parametrize(
    "headers, "
    "limit, window, queue, current_time, "
    "expect_limit, expect_remaining, expect_queue",
    [
        pytest.param(
            {"X-API-Rate-Limit": "100", "X-API-Rate-Remaining": "50", "X-API-Rate-Window": "60"},
            1, 2, [600], 1000,
            100, 50, [600, 1000 + 60],
            id="correct headers => update",
        ),
        pytest.param(
            {},
            10, 20, [], 10000,
            10, 0, [10000 + 20],
            id="missing headers => keep defaults",
        ),
    ]
)
def test_update(headers: CaseInsensitiveDict[str],
                limit: int, window: int, queue: list[int], current_time: float,
                expect_limit: int, expect_remaining: int, expect_queue: list[int]) -> None:
    with patch("time.time", return_value=current_time) as mock_time, \
            patch("time.sleep"):
        rate_limiter = RateLimiter()
        rate_limiter.limit = limit
        rate_limiter.window = window
        rate_limiter.queue = deque(queue)

        rate_limiter.update(headers)

        assert rate_limiter.limit == expect_limit
        assert rate_limiter.remaining == expect_remaining
        assert rate_limiter.queue == deque(expect_queue)
        mock_time.assert_called_once()
