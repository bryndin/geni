### NOTE: Geni API allows 1 request per 10 seconds,
### on a large tree this script may take a few minutes to run.
import logging

from geni import Geni

from fetch_all_managed_profiles import fetch_all_profiles, load_profiles, save_profiles, PROFILES_FILE

# Rate limiting events are reported at the INFO level
logging.basicConfig(level=logging.INFO)


def delete_all_profiles(client, profiles, batch_size=1):
    guids = [profile["guid"] for profile in profiles]

    batch_size = 1
    for i in range(0, len(guids), batch_size):
        guids_to_delete = guids[i:i + batch_size]
        response = client.profile.delete(",".join(guids_to_delete))

        # Occasionally Geni API returns "Access Denied" for some reason,
        # especially on large batches and doesn't delete the profile.
        # This will help you to figure the optimal batch size.
        try:
            print(response.json())
            continue
        except:
            pass
        try:
            print(response.text)
            continue
        except:
            pass
        print(response)


if __name__ == "__main__":
    client = Geni()  # API key is stored in the api key file
    try:
        profiles = load_profiles(PROFILES_FILE)
    except FileNotFoundError:
        profiles = fetch_all_profiles(client)
        save_profiles(profiles, PROFILES_FILE)

    delete_all_profiles(client, profiles)
