from typing import Any

from .internal.caller import Caller


class Profile(Caller):
    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key=api_key)

    def profile(self,
                fields: list[str] | None = None,
                guids: list[str] | None = None,
                only_ids: bool | None = None
                ) -> dict[str, Any]:
        """
        Returns information about a profile.
        """
        url = "https://www.geni.com/api/profile"
        params = {
            "fields": fields,
            "guids": guids,
            "only_ids": only_ids
        }

        response = self._call(url, params=params)
        return response.json()

    def delete(self, guids: list[str]) -> dict[str, str]:
        """
        Deletes a profile.
        """
        url = "https://www.geni.com/api/profile/delete"
        params = {"guids": guids}

        response = self._call(url, params=params, method="post")
        return response.json()

    def update_basics(self, guid: str,
                      about_me: str | None = None,
                      baptism: dict[str, Any] | None = None,
                      birth: dict[str, Any] | None = None,
                      burial: dict[str, Any] | None = None,
                      cause_of_death: str | None = None,
                      death: dict[str, Any] | None = None,
                      display_name: str | None = None,
                      first_name: str | None = None,
                      gender: str | None = None,
                      is_alive: bool | None = None,
                      last_name: str | None = None,
                      maiden_name: str | None = None,
                      middle_name: str | None = None,
                      names: dict[str, Any] | None = None,
                      nicknames: list[str] | None = None,
                      suffix: str | None = None,
                      title: str | None = None,
                      ) -> dict[str, Any]:
        """
        Updates basic profile information for a specific profile on Geni.

        :param guid: str
            The GUID of the profile to update (required).
        :param first_name: str, optional
            The new first name of the profile.
        :param middle_name: str, optional
            The new middle name of the profile.
        :param last_name: str, optional
            The new last name of the profile.
        :param maiden_name: str, optional
            The new maiden name of the profile.
        :param suffix: str, optional
            The new suffix of the profile.
        :param display_name: str, optional
            The new display name of the profile.
        :param title: str, optional
            The new title of the profile.
        :param nicknames: str, optional
            Comma-delimited list of nicknames for the profile.
        :param about_me: str, optional
            The "About Me" section of the profile.
        :param gender: str, optional
            The gender of the profile.
        :param is_alive: bool, optional
            True if the profile is living, False otherwise.
        :param birth: Event, optional
            Information about the birth event (e.g., date, place).
        :param baptism: Event, optional
            Information about the baptism event (e.g., date, place).
        :param death: Event, optional
            Information about the death event (e.g., date, place).
        :param burial: Event, optional
            Information about the burial event (e.g., date, place).
        :param cause_of_death: str, optional
            The cause of death of the profile.
        :param names: Hash, optional
            Nested maps of locales to name fields to values.

        :return: dict
            The response from the API.
        """
        url = "https://www.geni.com/api/profile/update-basics"
        params = {
            "guid": guid,
            "about_me": about_me,
            "baptism": baptism,
            "birth": birth,
            "burial": burial,
            "cause_of_death": cause_of_death,
            "death": death,
            "display_name": display_name,
            "first_name": first_name,
            "gender": gender,
            "is_alive": is_alive,
            "last_name": last_name,
            "maiden_name": maiden_name,
            "middle_name": middle_name,
            "names": names,
            "nicknames": nicknames,
            "suffix": suffix,
            "title": title,
        }

        response = self._call(url, params=params, method="post")
        return response.json()
