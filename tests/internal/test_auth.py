import json
from unittest.mock import patch, mock_open

import pytest

from geni.internal.auth import Auth, AuthError


DUMMY_TIME = 1609459200  # Mocked time (Jan 1, 2021)
DUMMY_FUTURE_TIME = DUMMY_TIME + 3600
DUMMY_PAST_TIME = DUMMY_TIME - 600
DUMMY_API_KEY = "dummy_api_key"
DUMMY_TOKEN = "dummy_token"


@pytest.mark.parametrize(
    "kwargs, load_return, expect_exception",
    [
        # pass all kwargs => no load, no exception
        ({"api_key": DUMMY_API_KEY, "api_file": "mock_api_file", "token_file": "mock_token_file", "save_token": False}, None, None),
        # pass only api_key => no load, no exception
        ({"api_key": DUMMY_API_KEY}, None, None),
        # pass only api_file => load, no exception
        ({"api_file": "mock_api_file"}, DUMMY_API_KEY, None),
        # use default api_file => load, no exception
        ({}, DUMMY_API_KEY, None),
        # don't pass api_key and fail loading key => raise exception
        ({}, None, AuthError),
        # pass empty string as api_key and fail loading key => raise exception
        ({"api_key": ""}, None, AuthError),
        # don't pass api_key and load empty string => raise exception
        ({}, "", AuthError),
    ]
)
def test___init__(kwargs, load_return, expect_exception):
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
            assert auth._expires_at is None

            if load_return:
                mock_load_secrets.assert_called_once_with(kwargs.get("api_file", "geni_api.key"))


@pytest.mark.parametrize(
    "initial, load, generate, save, expect",
    [
         # unexpired token already exists => pass
        ((DUMMY_TOKEN, DUMMY_FUTURE_TIME), (None, None), (None, None), False, (DUMMY_TOKEN, DUMMY_FUTURE_TIME)),
        # no previous token exists => load
        ((None, None), (DUMMY_TOKEN, DUMMY_FUTURE_TIME), (None, None), False, (DUMMY_TOKEN, DUMMY_FUTURE_TIME)),
        # no previous token exists and load fails => generate and don't save
        ((None, None), (None, None), (DUMMY_TOKEN, DUMMY_FUTURE_TIME), False, (DUMMY_TOKEN, DUMMY_FUTURE_TIME)),
        # expired token => generate and don't save
        ((DUMMY_TOKEN, DUMMY_PAST_TIME), (None, None), (DUMMY_TOKEN, DUMMY_FUTURE_TIME), False, (DUMMY_TOKEN, DUMMY_FUTURE_TIME)),
        # expired token => generate and save
        ((DUMMY_TOKEN, DUMMY_PAST_TIME), (None, None), (DUMMY_TOKEN, DUMMY_FUTURE_TIME), True, (DUMMY_TOKEN, DUMMY_FUTURE_TIME)),
    ],
)
def test_access_token(initial, load, generate, save, expect):
    with patch.object(Auth, "_load") as mock_load, \
         patch.object(Auth, "_generate") as mock_generate, \
         patch.object(Auth, "_save") as mock_save, \
         patch("time.time", return_value=DUMMY_TIME):

        auth = Auth(api_key=DUMMY_API_KEY, save_token=save)

        if load[0] is not None:
            mock_load.side_effect = lambda: (
                setattr(auth, "_access_token", load[0]),
                setattr(auth, "_expires_at", load[1])
            )

        if generate[0] is not None:
            mock_generate.side_effect = lambda: (
                setattr(auth, "_access_token", generate[0]),
                setattr(auth, "_expires_at", generate[1])
            )

        auth._access_token = initial[0]
        auth._expires_at = initial[1]
        token = auth.access_token

        assert token == expect[0]
        assert auth._access_token == expect[0]
        assert auth._expires_at == expect[1]
        if load[0] is not None:
            mock_load.assert_called_once()
        if generate[0] is not None:
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
def test_load_secrets(file_content, path_exists, expected_api_key):
    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_file, \
         patch("os.path.exists", return_value=path_exists):
            api_key = Auth._load_secrets("dummy_api_file.cfg")

            assert api_key == expected_api_key
            if path_exists:
                mocked_file.assert_called_once_with("dummy_api_file.cfg", "r")
            else:
                mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "access_token, expires_at",
    [
        ("access-token-123", 1672531199),
        (None, None),
    ]
)
def test_save(access_token, expires_at):
    auth = Auth(api_key="dummy-api-key")
    auth._access_token = access_token
    auth._expires_at = expires_at

    with patch("builtins.open", mock_open()) as mocked_file:
        auth._save("dummy_token_file.tmp")
        mocked_file.assert_called_once_with("dummy_token_file.tmp", "w")

        expected_data = {
            "access_token": access_token,
            "expires_at": expires_at
        }
        calls = [call[0][0] for call in mocked_file().write.call_args_list]
        assert ''.join(calls) == json.dumps(expected_data)

@pytest.mark.parametrize(
    "file_content, path_exists, expect_access_token, expect_expires_at, expect_exception",
    [
        # correct file => set access_token and expires_at
        ('{"access_token": "token", "expires_at": 123}', True, "token", 123, None),
        # missing token key => raise exception
        ('{"expires_at": 123}', True, None, None, AuthError),
        # missing expires_at key => raise exception
        ('{"access_token": "token"}', True, None, None, AuthError),
        # bad json => raise exception
        ("}", True, None, None, AuthError),
        # no file => don't change access_token and expires_at
        (None, False, None, None, None),
    ]
)
def test_load(file_content, path_exists, expect_access_token, expect_expires_at, expect_exception):
    auth = Auth(api_key="dummy-api-key")

    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_file:
        with patch("os.path.exists", return_value=path_exists):
            if expect_exception is not None:
                with pytest.raises(expect_exception):
                    auth._load()
            else:
                auth._load()
            assert auth._access_token == expect_access_token
            assert auth._expires_at == expect_expires_at
            if path_exists:
                mocked_file.assert_called_once_with(auth._token_file, "r")
            else:
                mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "redirect_url, expect_access_token, expect_expires_at, expect_exception",
    [
        # correct url => set access_token and expires_at
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D3600", "token123", 3600, None),
        # missing access_token value => raise exception
        ("https://example.com/oauth/auth_success#access_token%3D%26expires_in%3D3600", None, None, AuthError),
        # missing expires_in value => raise exception
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D", None, None, AuthError),
        # expires_in is not an int => raise exception
        ("https://example.com/oauth/auth_success#access_token%3Dtoken123%26expires_in%3D123f56", None, None, AuthError),
        # missing search template => raise exception
        ("https://example.com/oauth/auth_success", None, None, AuthError),
        # bad url => raise exception
        ("not an url", None, None, AuthError),
        # failed auth => raise exception
        ("https://example.com/oauth/failure", None, None, True),
    ]
)
def test_generate(redirect_url, expect_access_token, expect_expires_at, expect_exception):
    auth = Auth(api_key="dummy-api-key")

    with patch("builtins.input", return_value=redirect_url), \
         patch("time.time", return_value=1000):
        if expect_exception is not None:
            with pytest.raises(AuthError):
                auth._generate()
        else:
            auth._generate()
            assert auth._access_token == expect_access_token
            assert auth._expires_at == 1000 + expect_expires_at
