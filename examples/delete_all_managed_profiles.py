### NOTE: Geni API allows 1 request per 10 seconds,
### on a large tree this script may take a few minutes to run.
import json

from geni import Geni

from .fetch_all_managed_profiles import fetch_all_profiles, PROFILES_FILE


def load_profiles(input_file):
    with (open(input_file, "r") as f):
        profiles = json.load(f)
        print(f"Loaded {len(profiles)} profile IDs from {input_file}")
        return profiles


def save_profiles(profiles, output_file):
    with open(output_file, "w") as f:
        json.dump(profiles, f, indent=4)
    print(f"Saved {len(profiles)} profile IDs to {output_file}")


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
    except:
        profiles = fetch_all_profiles(client)
        save_profiles(profiles, PROFILES_FILE)

    delete_all_profiles(client, profiles)
