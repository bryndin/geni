import json
import os
import re
import time

API_KEY_FILE = "geni_api.key"  # File to store API key
TOKEN_FILE = "geni_token.tmp"  # File to store tokens


class AuthError(Exception):
    pass


class Auth:
    _SERIALIZE_ACCESS_TOKEN = "access_token"
    _SERIALIZE_EXPIRES_AT = "expires_at"

    def __init__(self, api_key=None, api_file=API_KEY_FILE, token_file=TOKEN_FILE, save_token=True):
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
        self._api_key = api_key
        self._token_file = token_file
        self._save_token = save_token

        self._access_token = None
        self._expires_at = None

        if not self._api_key:
            self._api_key = self._load_secrets(api_file)

        if not self._api_key:
            raise AuthError(f"Pass the API key or store it in {api_file}")

    @property
    def access_token(self):
        """
        Get the access token.

        :return: the access token
        :rtype: str       

         .. note::
            Lazy loading the access token and refreshing it if needed.
        """
        if not self._access_token:
            self._load()

        if not self._access_token or not self._expires_at or self._expires_at <= time.time():
            self._generate()
            if self._save_token:
                self._save()

        return self._access_token

    @staticmethod
    def _load_secrets(api_file):
        """
        Load API key from a file. 

        :param api_file: the file to load the API key from
        :type api_file: str
        :return: the API key
        :rtype: str
        """
        if os.path.exists(api_file):
            with open(api_file, "r") as f:
                return f.read().strip()

    def _save(self, filename=TOKEN_FILE):
        """
        Save access token time to a file.
        """
        with open(filename, "w") as f:
            json.dump({
                self._SERIALIZE_ACCESS_TOKEN: self._access_token,
                self._SERIALIZE_EXPIRES_AT: self._expires_at
            }, f)

    def _load(self):
        """
        Load access token time from a file.
        """
        if os.path.exists(self._token_file):
            with open(self._token_file, "r") as f:
                try:
                    data = json.load(f)
                    self._access_token = data["access_token"]
                    self._expires_at = data["expires_at"]
                except (json.decoder.JSONDecodeError, KeyError):
                    self._access_token = self._expires_at = None
                    raise AuthError(f"The access token file {self._token_file} is corrupt. Was it edited manually?")

    def _generate(self):
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

        if "oauth/auth_success" in redirect_url:
            match = re.search(r"access_token%3D(.*)%26expires_in%3D(.*)", redirect_url)
            if not match or not match.group(1) or not match.group(2) or not match.group(2).isdigit():
                raise AuthError("Invalid redirect URL. Did you copy one from the address bar?")

            self._access_token = match.group(1)
            self._expires_at = time.time() + int(match.group(2))
        else:
            raise AuthError("Auth failed, possibly rejected by user")
