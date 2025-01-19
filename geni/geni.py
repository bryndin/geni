from geni.profile import Profile
from geni.user import User


class Geni:
    def __init__(self, api_key=None):
        """
        Initialize the Geni object, with an optional api_key.

        :param str api_key: a Geni API key. If provided, this key parameter takes precedence over the one listed in the key file.

        .. note:: This class is not more than an aggregator for the Geni API classes.
        """
        self.profile = Profile(api_key=api_key)
        self.user = User(api_key=api_key)
