from typing import Dict, Any

from .internal.caller import Caller


class Stats(Caller):
    def __init__(self, api_key=None):
        super().__init__(api_key=api_key)

    def stats(self) -> Dict[str, Any]:
        """
         Returns information about the site.

        :return: A dictionary containing the site's statistics.
        :rtype: dict
        """
        url = "https://www.geni.com/api/stats"

        response = self._call(url)
        return response.json()

    def world_family_tree(self):
        """
         Returns info about the world family tree.
        """
        url = "https://www.geni.com/api/stats/world-family-tree"

        response = self._call(url)
        return response.json()