from .internal.caller import Caller


class User(Caller):
    def __init__(self, api_key=None):
        super().__init__(api_key=api_key)

    def managed_profiles(self, fields=None, page=None, per_page=None):
        """
        Returns a list of profiles the user manages.

        :param fields: Optional; A list of fields to include in the response.
        :type fields: list or None
        :param page: Optional; The page number for paginated results.
        :type page: int or None
        :param per_page: Optional; The number of results per page.
        :type per_page: int or None
        :return: A list of profiles managed by the user.
        :rtype: dict
        """
        url = "https://www.geni.com/api/user/managed-profiles"
        params = {
            "fields": fields,
            "page": page,
            "per_page": per_page,
        }

        response = self._call(url, params=params)
        return response.json()
