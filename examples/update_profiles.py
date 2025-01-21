### NOTE: Geni API allows 1 request per 10 seconds,
### on a large tree this script may take a few minutes to run.
import logging

from geni import Geni

from fetch_all_managed_profiles import fetch_all_profiles, load_profiles, save_profiles, PROFILES_FILE

# Rate limiting events are reported at the INFO level
logging.basicConfig(level=logging.INFO)

PROCESSED_FILE = "processed_profiles.json"
ALL_NAME_FIELDS = ["title", "first_name", "middle_name", "maiden_name", "last_name", "suffix"]


def capitalize_names(resp, params):
    for name in ALL_NAME_FIELDS:
        if name in resp:
            params[name] = resp[name].capitalize()


def iterate_profiles(client, profiles):
    try:
        # make sure we don't process profiles already processed on the previous runs
        processed_profiles = load_profiles(PROCESSED_FILE)
    except FileNotFoundError:
        processed_profiles = []

    for profile in profiles:
        if profile in processed_profiles:
            continue

        guid = profile["guid"]
        print(f"Processing profile {guid}...\n")

        try:
            resp = client.profile.profile(guids=guid, fields=",".join(ALL_NAME_FIELDS))
        except Exception as e:
            print(f"Error reading profile {guid}. Exception: {e}")
            continue

        params = {}
        # Example processing of names: capitalize all names
        capitalize_names(resp, params=params)

        try:
            resp = client.profile.update_basics(guid, **params)
        except Exception as e:
            print(f"Error updating profile {guid}. Exception: {e}")
            continue

        # update the list of processed profiles
        processed_profiles.append(profile["guid"])
        save_profiles(processed_profiles, PROCESSED_FILE)


if __name__ == "__main__":
    client = Geni()  # API key is stored in the api key file
    try:
        profiles = load_profiles(PROFILES_FILE)
    except FileNotFoundError:
        profiles = fetch_all_profiles(client)
        save_profiles(profiles, PROFILES_FILE)

    iterate_profiles(client, profiles)
