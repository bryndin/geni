### NOTE: Geni API allows 1 request per 10 seconds, max profiles per request is 50.
### on a large tree this script may take a few minutes to run.
import json
import logging

from geni import Geni

PROFILES_FILE = "profiles.json"

# Rate limiting events are reported at the INFO level
logging.basicConfig(level=logging.INFO)


def load_profiles(input_file):
    with (open(input_file, "r") as f):
        profiles = json.load(f)
        print(f"Loaded {len(profiles)} profile IDs from {input_file}")
        return profiles


def save_profiles(profiles, output_file):
    with open(output_file, "w") as f:
        json.dump(profiles, f, indent=4)
    print(f"Saved {len(profiles)} profile IDs to {output_file}")


def fetch_all_profiles(client):
    url = "non-blank"
    all_profiles = []
    page = 1

    while url:
        print(f"Fetching page {page}...\n")
        response = client.user.managed_profiles(page=page)

        profiles = response.get("results", [])
        all_profiles.extend(profiles)

        page += 1
        url = response.get("next_page")

    print(f"Fetched {len(all_profiles)} profiles")
    return all_profiles


if __name__ == "__main__":
    client = Geni()  # API key is stored in the api key file
    profiles = fetch_all_profiles(client)
    save_profiles(profiles, PROFILES_FILE)
