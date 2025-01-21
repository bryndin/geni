from typing import Any

from .internal.caller import Caller


class Stats(Caller):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key=api_key)

    def stats(self) -> dict[str, dict[str, Any]]:
        """
         Returns information about the site.

        :return: A dictionary containing the site's statistics.
        :rtype: dict
        **Dictionary Keys:**
            * **stats**: List of available statistics (list[dict])
        """
        url = "https://www.geni.com/api/stats"

        response = self._call(url)
        return response.json()

    def world_family_tree(self) -> dict[str, Any]:
        """
         Returns info about the world family tree.

        :return: A dictionary containing information about the World Family Tree.
        :rtype: dict
        **Dictionary Keys:**
            * **formatted_size**: Formatted number of profiles in the World Family Tree (str)
            * **size**: Number of profiles in the World Family Tree (int)
        """
        url = "https://www.geni.com/api/stats/world-family-tree"

        response = self._call(url)
        return response.json()
