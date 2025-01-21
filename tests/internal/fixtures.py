import json

import requests

dummyResponse = requests.Response()
dummyResponse._content = json.dumps("content").encode("utf-8")

noneProfile = {
    "about_me": None,
    "baptism": None,
    "birth": None,
    "burial": None,
    "cause_of_death": None,
    "death": None,
    "display_name": None,
    "first_name": None,
    "gender": None,
    "is_alive": None,
    "last_name": None,
    "maiden_name": None,
    "middle_name": None,
    "names": None,
    "nicknames": None,
    "suffix": None,
    "title": None,
}

sampleProfile = {
    "about_me": "one of us",
    "baptism": {"date": "2000-01-01", "location": "St. Peter's Church, NYC"},
    "birth": {"date": "1985-05-15", "location": "San Francisco, CA"},
    "burial": {"date": "2060-06-01", "location": "Greenwood Cemetery, Brooklyn"},
    "cause_of_death": "Heart failure",
    "death": {"date": "2060-05-30", "location": "New York, NY"},
    "display_name": "John Doe",
    "first_name": "John",
    "gender": "Male",
    "is_alive": False,
    "last_name": "Doe",
    "maiden_name": "Smith",
    "middle_name": "Alexander",
    "names": {
        "en": {"first_name": "John", "last_name": "Doe"},
        "es": {"first_name": "Juan", "last_name": "Perez"},
    },
    "nicknames": ["Johnny", "JD"],
    "suffix": "Jr.",
    "title": "Dr."
}
