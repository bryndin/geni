from geni.profile import Profile
from geni.stats import Stats
from geni.user import User


class Geni:
    def __init__(self, api_key: str | None = None) -> None:
        """
        Initialize the Geni client.

        :param str api_key: a Geni API key. If provided, this key parameter takes precedence over the one listed in the key file.

        .. note:: This class is not more than an aggregator for the Geni API classes.
        """
        self.profile: Profile = Profile(api_key=api_key)
        self.stats: Stats = Stats(api_key=api_key)
        self.user: User = User(api_key=api_key)
