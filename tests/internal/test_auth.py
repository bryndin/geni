from typing import Any
from unittest.mock import patch, mock_open

import pytest

from geni.internal.auth import Auth, AuthError, AccessToken

DUMMY_TIME = 1609459200  # Mocked time (Jan 1, 2021)
DUMMY_FUTURE_TIME = DUMMY_TIME + 3600
DUMMY_PAST_TIME = DUMMY_TIME - 600
DUMMY_API_KEY = "dummy_api_key"
DUMMY_TOKEN = "dummy_token"


@pytest.mark.parametrize(
    "kwargs, load_return, expect_exception",
    [
        pytest.param(
            {
                "api_key": DUMMY_API_KEY,
                "api_file": "mock_api_file",
                "token_file": "mock_token_file",
                "save_token": False
            }, None, None,
            id="pass all kwargs => no load, no exception"),
        pytest.param({"api_key": DUMMY_API_KEY}, None, None,
                     id="pass only api_key => no load, no exception"),
        pytest.param({"api_file": "mock_api_file"}, DUMMY_API_KEY, None,
                     id="pass only api_file => load, no exception"),
        pytest.param({}, DUMMY_API_KEY, None,
                     id="use default api_file => load, no exception"),
        pytest.param({}, None, AuthError,
                     id="don't pass api_key and fail loading key => raise exception"),
        # pass empty string as api_key and fail loading key => raise exception
        pytest.param({"api_key": ""}, None, AuthError,
                     id="pass empty string as api_key and fail loading key => raise exception"),
        pytest.param({}, "", AuthError,
                     id="don't pass api_key and load empty string => raise exception"),
    ]
)
def test___init__(kwargs: dict[str, Any], load_return: str | None, expect_exception: type[Exception] | None) -> None:
    with patch.object(Auth, "_load_secrets") as mock_load_secrets:
        mock_load_secrets.return_value = load_return

        if expect_exception is not None:
            with pytest.raises(expect_exception):
                Auth(**kwargs)
        else:
            auth = Auth(**kwargs)

            assert auth._api_key == load_return if load_return is not None else kwargs.get("api_key", None)
            assert auth._token_file == kwargs.get("token_file", "geni_token.tmp")
            assert auth._save_token == kwargs.get("save_token", True)
            assert auth._access_token is None

            if load_return:
                mock_load_secrets.assert_called_once_with(kwargs.get("api_file", "geni_api.key"))


@pytest.mark.parametrize(
    "initial, load, generate, save, expect, expect_exception",
    [
        pytest.param(AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     None,
                     False,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     id="unexpired token already exists => pass"),
        pytest.param(None,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     False,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     id="no previous token exists => load"),
        pytest.param(None,
                     None,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     False,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     id="no previous token exists and load fails => generate and don't save"),
        pytest.param(AccessToken(DUMMY_TOKEN, DUMMY_PAST_TIME),
                     None,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     False,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     id="expired token => generate and don't save"),
        pytest.param(AccessToken(DUMMY_TOKEN, DUMMY_PAST_TIME),
                     None,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     True,
                     AccessToken(DUMMY_TOKEN, DUMMY_FUTURE_TIME),
                     None,
                     id="expired token => generate and save"),
        pytest.param(None,
                     None,
                     None,
                     False,
                     None,
                     AuthError,
                     id="no token and both load and generate fail => raise exception"),
    ],
)
def test_access_token(
        initial: AccessToken | None,
        load: AccessToken | None,
        generate: AccessToken | None,
        save: bool,
        expect: AccessToken,
        expect_exception: type[Exception] | None) -> None:
    with (patch.object(Auth, "_load") as mock_load, \
          patch.object(Auth, "_generate") as mock_generate, \
          patch.object(Auth, "_save") as mock_save, \
          patch("time.time", return_value=DUMMY_TIME)):

        auth = Auth(api_key=DUMMY_API_KEY, save_token=save)

        if load is not None:
            mock_load.side_effect = lambda: setattr(auth, "_access_token", load)

        if generate is not None:
            mock_generate.side_effect = lambda: setattr(auth, "_access_token", generate)

        auth._access_token = initial

        if expect_exception is not None:
            with pytest.raises(expect_exception):
                auth.access_token
        else:
            token = auth.access_token

            assert token == expect.token
            assert auth._access_token == expect
            if load is not None:
                mock_load.assert_called_once()
            if generate is not None:
                mock_generate.assert_called_once()
            if save:
                mock_save.assert_called_once()
            else:
                mock_save.assert_not_called()


@pytest.mark.parametrize(
    "file_content, path_exists, expected_api_key",
    [
        # key string => return key
        ("api-key", True, "api-key"),
        # extra spacing in key => return key
        ("   my-secret-api-key\n", True, "my-secret-api-key"),
        # empty file => return ""
        ("", True, ""),
        # no file => return None
        ("api-key", False, None),
    ]
)
def test_load_secrets(file_content: str, path_exists: bool, expected_api_key: str | None) -> None:
    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_file, \
            patch("os.path.exists", return_value=path_exists):
        api_key = Auth._load_secrets("dummy_api_file.cfg")

        assert api_key == expected_api_key
        if path_exists:
            mocked_file.assert_called_once_with("dummy_api_file.cfg", "r")
        else:
            mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "token, expect_arg, expect_return",
    [
        pytest.param(
            AccessToken("access-token-123", 1672531199), "geni_token.tmp", True,
            id="save token to default filename => return True"),
        pytest.param(
            None, "geni_token.tmp", False,
            id="there is no token => return False"),
    ]
)
def test_save(token: AccessToken | None, expect_arg: str, expect_return: bool) -> None:
    auth = Auth(api_key="dummy-api-key")
    auth._access_token = token

    with patch("builtins.open", mock_open()) as mocked_file:
        res = auth._save()

        assert res == expect_return
        if token is not None:
            mocked_file.assert_called_once_with(expect_arg, "w")
            calls = [call[0][0] for call in mocked_file().write.call_args_list]
            assert ''.join(calls) == f'{{"token": "{token.token}", "expires_at": {token.expires_at}}}'
        else:
            mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "file_content, path_exists, expect, expect_exception",
    [
        pytest.param('{"token": "token", "expires_at": 123}', True, AccessToken("token", 123), None,
                     id="correct file => expect the access token"),
        pytest.param('{"not-token": "token"}', True, None, AuthError,
                     id="corrupt file => raise exception"),
        pytest.param("}", True, None, AuthError,
                     id="bad json => raise exception"),
        pytest.param(None, False, None, AuthError,
                     id="missing file => raise exception"),
    ]
)
def test_load(file_content: str, path_exists: bool, expect: AccessToken | None,
              expect_exception: type[Exception] | None) -> None:
    auth = Auth(api_key="dummy-api-key")
    auth._access_token = None

    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_file:
        with patch("os.path.exists", return_value=path_exists):
            if expect_exception is not None:
                with pytest.raises(expect_exception):
                    auth._load()
            else:
                auth._load()
            assert auth._access_token == expect
            if path_exists:
                mocked_file.assert_called_once_with(auth._token_file, "r")
            else:
                mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "redirect_url, expect, expect_exception",
    [
        # correct url => set access_token and expires_at
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D3600",
         AccessToken("token123", 3600 + 1000), None),
        # missing access_token value => raise exception
        ("https://example.com/oauth/auth_success#access_token%3D%26expires_in%3D3600", None, AuthError),
        # missing expires_in value => raise exception
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D", None, AuthError),
        # expires_in is not an int => raise exception
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D123f56", None, AuthError),
        # missing search template => raise exception
        ("https://example.com/oauth/auth_success", None, AuthError),
        # bad url => raise exception
        ("not an url", None, AuthError),
        # failed auth => raise exception
        ("https://example.com/oauth/failure", None, True),
    ]
)
def test_generate(redirect_url: str, expect: AccessToken | None, expect_exception: type[Exception] | None) -> None:
    auth = Auth(api_key="dummy-api-key")

    with patch("builtins.input", return_value=redirect_url), \
            patch("time.time", return_value=1000):
        if expect_exception is not None:
            with pytest.raises(AuthError):
                auth._generate()
        else:
            auth._generate()
            assert auth._access_token == expect
