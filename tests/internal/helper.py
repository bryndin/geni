from unittest.mock import patch

import pytest

_DUMMY_API_KEY = "dummy_api_key"
_CALLER_FN = "geni.internal.caller.Caller._call"

def check_api_method(api_cls, api_method, api_url,
          args, kwargs, mock_returns, mock_raises, expect_response, expect_kwargs, expect_exception):
    with patch(_CALLER_FN) as mock_call:
        if mock_raises:
            mock_call.side_effect = mock_raises
        else:
            mock_call.return_value = mock_returns

        f = getattr(api_cls(api_key=_DUMMY_API_KEY), api_method, None)
        assert f is not None, f"class {api_cls} has no method {api_method}, typo in your test?"

        if expect_exception:
            with pytest.raises(expect_exception):
                f(*args, **kwargs)
        else:
            assert f(*args, **kwargs) == expect_response

        mock_call.assert_called_once_with(api_url, **expect_kwargs)
