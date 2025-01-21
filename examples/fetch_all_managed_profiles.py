### NOTE: Geni API allows 1 request per 10 seconds, max profiles per request is 50.
### on a large tree this script may take a few minutes to run.
import json

from geni import Geni


PROFILES_FILE = "processed_profiles.json"


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
    with open(PROFILES_FILE, "w") as f:
        f.write(json.dumps(profiles))
        print(f"Saved {len(profiles)} profiles to {PROFILES_FILE}")
