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

    def add_child(self, guid: str,
                  about_me: str | None = None,
                  baptism: dict[str, Any] | None = None,
                  birth: dict[str, Any] | None = None,
                  burial: dict[str, Any] | None = None,
                  death: dict[str, Any] | None = None,
                  display_name: str | None = None,
                  divorce: dict[str, Any] | None = None,
                  email: str | None = None,
                  first_name: str | None = None,
                  gender: str | None = None,
                  is_alive: bool | None = None,
                  last_name: str | None = None,
                  maiden_name: str | None = None,
                  marriage: dict[str, Any] | None = None,
                  middle_name: str | None = None,
                  names: dict[str, dict[str, str]] | None = None,
                  nicknames: list[str] | None = None,
                  public: bool | None = None,
                  relationship_modifier: str | None = None,
                  suffix: str | None = None,
                  title: str | None = None,
                  ) -> dict[str, Any]:
        """
        Adds a child to a profile and returns the added profile.

        :param guid: str
            The GUID of the profile (required).
        :param about_me: str, optional
            The "About Me" section of the profile (must be requested).
        :param baptism: dict, optional
            Information about the baptism event (e.g., date, place).
        :param birth: dict, optional
            Information about the birth event (e.g., date, place).
        :param burial: dict, optional
            Information about the burial event (e.g., date, place).
        :param death: dict, optional
            Information about the death event (e.g., date, place).
        :param display_name: str, optional
            The profile's display name.
        :param divorce: dict, optional
            Divorce event (e.g., date, place).
        :param email: str, optional
            Profile's email address.
        :param first_name: str, optional
            Profile's first name.
        :param gender: str, optional
            Profile's gender.
        :param is_alive: bool, optional
            True if the profile is living.
        :param last_name: str, optional
            Profile's last name.
        :param maiden_name: str, optional
            Profile's maiden name.
        :param marriage: dict, optional
            Information about the marriage event (e.g., date, place).
        :param middle_name: str, optional
            Profile's middle name.
        :param names: dict, optional
            Nested maps of locales to name fields to values.
        :param nicknames: list of str, optional
            Also known as. Returned as an array, but can be set as a comma-delimited list.
        :param public: bool, optional
            True if the profile is public.
        :param relationship_modifier: str, optional
            Set to 'adopt' or 'foster' when adding children or siblings to the profile.
        :param suffix: str, optional
            Profile suffix.
        :param title: str, optional
            Profile name title.

        :return: dict
            The response from the API containing the added child's profile information.
        """
        url = "https://www.geni.com/api/profile/add-child"
        params = self._shared_params(
            about_me=about_me, baptism=baptism, birth=birth, burial=burial, death=death, display_name=display_name,
            divorce=divorce, email=email, first_name=first_name, gender=gender, is_alive=is_alive,
            last_name=last_name, maiden_name=maiden_name, middle_name=middle_name, marriage=marriage, names=names,
            nicknames=nicknames, public=public, relationship_modifier=relationship_modifier, suffix=suffix,
            title=title, )
        params["guid"] = guid

        response = self._call(url, params=params, method="post")
        return response.json()

    def add_parent(self, guid: str,
                   about_me: str | None = None,
                   baptism: dict[str, Any] | None = None,
                   birth: dict[str, Any] | None = None,
                   burial: dict[str, Any] | None = None,
                   death: dict[str, Any] | None = None,
                   display_name: str | None = None,
                   divorce: dict[str, Any] | None = None,
                   email: str | None = None,
                   first_name: str | None = None,
                   gender: str | None = None,
                   is_alive: bool | None = None,
                   last_name: str | None = None,
                   maiden_name: str | None = None,
                   marriage: dict[str, Any] | None = None,
                   middle_name: str | None = None,
                   names: dict[str, dict[str, str]] | None = None,
                   nicknames: list[str] | None = None,
                   public: bool | None = None,
                   relationship_modifier: str | None = None,
                   suffix: str | None = None,
                   title: str | None = None,
                   ) -> dict[str, Any]:
        """
        Adds a parent to a profile and returns the added profile.

        :param guid: str
            The GUID of the profile (required).
        :param about_me: str, optional
            The "About Me" section of the profile (must be requested).
        :param baptism: dict, optional
            Information about the baptism event (e.g., date, place).
        :param birth: dict, optional
            Information about the birth event (e.g., date, place).
        :param burial: dict, optional
            Information about the burial event (e.g., date, place).
        :param death: dict, optional
            Information about the death event (e.g., date, place).
        :param display_name: str, optional
            The profile's display name.
        :param divorce: dict, optional
            Divorce event (e.g., date, place).
        :param email: str, optional
            Profile's email address.
        :param first_name: str, optional
            Profile's first name.
        :param gender: str, optional
            Profile's gender.
        :param is_alive: bool, optional
            True if the profile is living.
        :param last_name: str, optional
            Profile's last name.
        :param maiden_name: str, optional
            Profile's maiden name.
        :param marriage: dict, optional
            Information about the marriage event (e.g., date, place).
        :param middle_name: str, optional
            Profile's middle name.
        :param names: dict, optional
            Nested maps of locales to name fields to values.
        :param nicknames: list of str, optional
            Also known as. Returned as an array, but can be set as a comma-delimited list.
        :param public: bool, optional
            True if the profile is public.
        :param relationship_modifier: str, optional
            Set to 'adopt' or 'foster' when adding children or siblings to the profile.
        :param suffix: str, optional
            Profile suffix.
        :param title: str, optional
            Profile name title.
        :return: dict
            The response from the API containing the added child's profile information.

        :return: dict
            The response from the API containing the added parent's profile information.
        """
        url = "https://www.geni.com/api/profile/add-parent"
        params = self._shared_params(
            about_me=about_me, baptism=baptism, birth=birth, burial=burial, death=death, display_name=display_name,
            divorce=divorce, email=email, first_name=first_name, gender=gender, is_alive=is_alive,
            last_name=last_name, maiden_name=maiden_name, middle_name=middle_name, marriage=marriage, names=names,
            nicknames=nicknames, public=public, relationship_modifier=relationship_modifier, suffix=suffix,
            title=title, )
        params["guid"] = guid

        response = self._call(url, params=params, method="post")
        return response.json()

    def add_partner(self, guid: str,
                    about_me: str | None = None,
                    baptism: dict[str, Any] | None = None,
                    birth: dict[str, Any] | None = None,
                    burial: dict[str, Any] | None = None,
                    death: dict[str, Any] | None = None,
                    display_name: str | None = None,
                    divorce: dict[str, Any] | None = None,
                    email: str | None = None,
                    first_name: str | None = None,
                    gender: str | None = None,
                    is_alive: bool | None = None,
                    last_name: str | None = None,
                    maiden_name: str | None = None,
                    marriage: dict[str, Any] | None = None,
                    middle_name: str | None = None,
                    names: dict[str, dict[str, str]] | None = None,
                    nicknames: list[str] | None = None,
                    public: bool | None = None,
                    relationship_modifier: str | None = None,
                    suffix: str | None = None,
                    title: str | None = None,
                    ) -> dict[str, Any]:
        """
        Adds a partner to a profile and returns the added profile.

        :param guid: str
            The GUID of the profile (required).
        :param about_me: str, optional
            The "About Me" section of the profile (must be requested).
        :param baptism: dict, optional
            Information about the baptism event (e.g., date, place).
        :param birth: dict, optional
            Information about the birth event (e.g., date, place).
        :param burial: dict, optional
            Information about the burial event (e.g., date, place).
        :param death: dict, optional
            Information about the death event (e.g., date, place).
        :param display_name: str, optional
            The profile's display name.
        :param divorce: dict, optional
            Divorce event (e.g., date, place).
        :param email: str, optional
            Profile's email address.
        :param first_name: str, optional
            Profile's first name.
        :param gender: str, optional
            Profile's gender.
        :param is_alive: bool, optional
            True if the profile is living.
        :param last_name: str, optional
            Profile's last name.
        :param maiden_name: str, optional
            Profile's maiden name.
        :param marriage: dict, optional
            Information about the marriage event (e.g., date, place).
        :param middle_name: str, optional
            Profile's middle name.
        :param names: dict, optional
            Nested maps of locales to name fields to values.
        :param nicknames: list of str, optional
            Also known as. Returned as an array, but can be set as a comma-delimited list.
        :param public: bool, optional
            True if the profile is public.
        :param relationship_modifier: str, optional
            Set to 'adopt' or 'foster' when adding children or siblings to the profile.
        :param suffix: str, optional
            Profile suffix.
        :param title: str, optional
            Profile name title.
        :return: dict
            The response from the API containing the added child's profile information.

        :return: dict
            The response from the API containing the added partner's profile information.
        """
        url = "https://www.geni.com/api/profile/add-partner"
        params = self._shared_params(
            about_me=about_me, baptism=baptism, birth=birth, burial=burial, death=death, display_name=display_name,
            divorce=divorce, email=email, first_name=first_name, gender=gender, is_alive=is_alive,
            last_name=last_name, maiden_name=maiden_name, middle_name=middle_name, marriage=marriage, names=names,
            nicknames=nicknames, public=public, relationship_modifier=relationship_modifier, suffix=suffix,
            title=title, )
        params["guid"] = guid

        response = self._call(url, params=params, method="post")
        return response.json()

    def add_sibling(self, guid: str,
                    about_me: str | None = None,
                    baptism: dict[str, Any] | None = None,
                    birth: dict[str, Any] | None = None,
                    burial: dict[str, Any] | None = None,
                    death: dict[str, Any] | None = None,
                    display_name: str | None = None,
                    divorce: dict[str, Any] | None = None,
                    email: str | None = None,
                    first_name: str | None = None,
                    gender: str | None = None,
                    is_alive: bool | None = None,
                    last_name: str | None = None,
                    maiden_name: str | None = None,
                    marriage: dict[str, Any] | None = None,
                    middle_name: str | None = None,
                    names: dict[str, dict[str, str]] | None = None,
                    nicknames: list[str] | None = None,
                    public: bool | None = None,
                    relationship_modifier: str | None = None,
                    suffix: str | None = None,
                    title: str | None = None,
                    ) -> dict[str, Any]:
        """
        Adds a sibling to a profile and returns the added profile.

        :param guid: str
            The GUID of the profile (required).
        :param about_me: str, optional
            The "About Me" section of the profile (must be requested).
        :param baptism: dict, optional
            Information about the baptism event (e.g., date, place).
        :param birth: dict, optional
            Information about the birth event (e.g., date, place).
        :param burial: dict, optional
            Information about the burial event (e.g., date, place).
        :param death: dict, optional
            Information about the death event (e.g., date, place).
        :param display_name: str, optional
            The profile's display name.
        :param divorce: dict, optional
            Divorce event (e.g., date, place).
        :param email: str, optional
            Profile's email address.
        :param first_name: str, optional
            Profile's first name.
        :param gender: str, optional
            Profile's gender.
        :param is_alive: bool, optional
            True if the profile is living.
        :param last_name: str, optional
            Profile's last name.
        :param maiden_name: str, optional
            Profile's maiden name.
        :param marriage: dict, optional
            Information about the marriage event (e.g., date, place).
        :param middle_name: str, optional
            Profile's middle name.
        :param names: dict, optional
            Nested maps of locales to name fields to values.
        :param nicknames: list of str, optional
            Also known as. Returned as an array, but can be set as a comma-delimited list.
        :param public: bool, optional
            True if the profile is public.
        :param relationship_modifier: str, optional
            Set to 'adopt' or 'foster' when adding children or siblings to the profile.
        :param suffix: str, optional
            Profile suffix.
        :param title: str, optional
            Profile name title.
        :return: dict
            The response from the API containing the added child's profile information.

        :return: dict
            The response from the API containing the added sibling's profile information.
        """
        url = "https://www.geni.com/api/profile/add-sibling"
        params = self._shared_params(
            about_me=about_me, baptism=baptism, birth=birth, burial=burial, death=death, display_name=display_name,
            divorce=divorce, email=email, first_name=first_name, gender=gender, is_alive=is_alive,
            last_name=last_name, maiden_name=maiden_name, middle_name=middle_name, marriage=marriage, names=names,
            nicknames=nicknames, public=public, relationship_modifier=relationship_modifier, suffix=suffix,
            title=title, )
        params["guid"] = guid

        response = self._call(url, params=params, method="post")
        return response.json()

    def delete(self, guids: list[str]) -> dict[str, str]:
        """
        Deletes a profile.

        :param guids: list of str
            The GUIDs of the profiles to delete (required).
        :return: dict
            The response from the API containing the deleted profile GUIDs.
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
        Updates basic profile information for a specific profile.

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

        params = self._shared_params(
            about_me=about_me, baptism=baptism, birth=birth, burial=burial, death=death, display_name=display_name,
            first_name=first_name, gender=gender, is_alive=is_alive,
            last_name=last_name, maiden_name=maiden_name, middle_name=middle_name, names=names, nicknames=nicknames,
            suffix=suffix, title=title, )

        for key in ["divorce", "email", "marriage", "public", "relationship_modifier"]:
            params.pop(key)

        params["guid"] = guid
        params["cause_of_death"] = cause_of_death

        response = self._call(url, params=params, method="post")
        return response.json()

    @staticmethod
    def _shared_params(about_me: str | None = None,
                       baptism: dict[str, Any] | None = None,
                       birth: dict[str, Any] | None = None,
                       burial: dict[str, Any] | None = None,
                       death: dict[str, Any] | None = None,
                       display_name: str | None = None,
                       divorce: dict[str, Any] | None = None,
                       email: str | None = None,
                       first_name: str | None = None,
                       gender: str | None = None,
                       is_alive: bool | None = None,
                       last_name: str | None = None,
                       maiden_name: str | None = None,
                       marriage: dict[str, Any] | None = None,
                       middle_name: str | None = None,
                       names: dict[str, dict[str, str]] | None = None,
                       nicknames: list[str] | None = None,
                       public: bool | None = None,
                       relationship_modifier: str | None = None,
                       suffix: str | None = None,
                       title: str | None = None,
                       ) -> dict[str, Any]:
        return {
            "about_me": about_me,
            "baptism": baptism,
            "birth": birth,
            "burial": burial,
            "death": death,
            "display_name": display_name,
            "divorce": divorce,
            "email": email,
            "first_name": first_name,
            "gender": gender,
            "is_alive": is_alive,
            "last_name": last_name,
            "maiden_name": maiden_name,
            "marriage": marriage,
            "middle_name": middle_name,
            "names": names,
            "nicknames": nicknames,
            "public": public,
            "relationship_modifier": relationship_modifier,
            "suffix": suffix,
            "title": title,
        }
