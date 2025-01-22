from dataclasses import dataclass, asdict
import json
import os
import re
import time

API_KEY_FILE = "geni_api.key"  # File to store API key
TOKEN_FILE = "geni_token.tmp"  # File to store tokens


class AuthError(Exception):
    pass


@dataclass(frozen=True)
class AccessToken:
    token: str
    expires_at: float


class Auth:
    def __init__(self,
                 api_key: str | None = None,
                 api_file: str = API_KEY_FILE,
                 token_file: str = TOKEN_FILE,
                 save_token: bool = True
                 ) -> None:
        """
        Constructor for Auth.
        
        :param api_key: the API key
        :type api_key: str
        :param token_file: the file to store the access token
        :type token_file: str
        :param save_token: whether to cache the access token in a file
        :type save_token: bool

        :raises AuthError: if the API key cannot be obtained
        """
        self._token_file: str = token_file
        self._save_token: bool = save_token

        self._access_token: AccessToken | None = None

        self._api_key: str = api_key or self._load_secrets(api_file) or ""
        if not self._api_key:
            raise AuthError(f"Pass the API key or store it in {api_file}")

    @property
    def access_token(self) -> str:
        """
        Get the access token.

        :return: the access token
        :rtype: str       

         .. note::
            Lazy loading the access token and refreshing it if needed.
        """
        if not self._access_token:
            self._load()

        if not self._access_token or not self._access_token.token or self._access_token.expires_at <= time.time():
            self._generate()
            if self._save_token:
                self._save()

        if not self._access_token:
            raise AuthError("Failed to obtain access token")

        return self._access_token.token

    @staticmethod
    def _load_secrets(api_file: str) -> str | None:
        """
        Load API key from a file. 

        :param api_file: the file to load the API key from
        :type api_file: str
        :return: the API key
        :rtype: str | None
        """
        if os.path.exists(api_file):
            with open(api_file, "r") as f:
                return f.read().strip()

        return None

    def _save(self) -> bool:
        """
        Save access token time to a file.

        :return: True if the access token was saved, False otherwise
        :rtype: bool
        """
        if self._access_token is None:
            return False

        with open(self._token_file, "w") as f:
            json.dump(asdict(self._access_token), f)
        return True

    def _load(self) -> None:
        """
        Load access token time from a file.

        :raises AuthError: if the access token file is corrupt or the file does not exist.
        """
        if not os.path.exists(self._token_file):
            raise AuthError(f"The access token file {self._token_file} does not exist")

        with open(self._token_file, "r") as f:
            try:
                data = json.load(f)
                self._access_token = AccessToken(**data)
            except (json.decoder.JSONDecodeError, TypeError):
                raise AuthError(f"The access token file {self._token_file} is corrupt. Was it edited manually?")

    def _generate(self) -> None:
        """
        Generate a new access token.

        :raise AuthError: if authentication fails
        """
        auth_url = (
            "https://www.geni.com/platform/oauth/authorize"
            f"?client_id={self._api_key}"
            "&response_type=token&display=desktop"
        )

        # TODO: Make it more visible?
        print("Visit this URL to authorize the application:")
        print(auth_url)
        redirect_url = input("Paste the redirect URL (from the address bar): ")

        if "oauth/auth_success" not in redirect_url:
            raise AuthError("Auth failed, possibly rejected by user")

        match = re.search(r"access_token%3D(.*)%26expires_in%3D(.*)", redirect_url)
        if not match or not match.group(1) or not match.group(2) or not match.group(2).isdigit():
            raise AuthError("Invalid redirect URL. Did you copy one from the address bar?")

        self._access_token = AccessToken(
            token=match.group(1),
            expires_at=time.time() + int(match.group(2))
        )
