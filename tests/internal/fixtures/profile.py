from typing import Any

sampleParamsUpdateBasics: dict[str, Any] = {
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

noneParamsUpdateBasics: dict[str, None] = {k: None for k in sampleParamsUpdateBasics}

sampleParamsAddChild: dict[str, Any] = {
    "about_me": "I am a genealogy enthusiast with a passion for history.",
    "baptism": {"date": "1990-02-01", "location": "New York, USA"},
    "birth": {"date": "1990-01-01", "location": "New York, USA"},
    "burial": {'date': '2080-02-02', 'location': 'Los Angeles, USA'},
    "death": {'date': '2080-01-01', 'location': 'Los Angeles, USA', },
    "display_name": "Jane Doe",
    "divorce": {'date': '2020-01-01', 'location': 'Chicago, USA'},
    "email": "johndoe@example.com",
    "first_name": "Jane",
    "gender": "Female",
    "is_alive": True,
    "last_name": "Doe",
    "maiden_name": "Brown",
    "marriage": {"date": "2010-01-01", "location": "New York, USA"},
    "middle_name": "Cherry",
    "names": {
        "en": {"first_name": "John", "last_name": "Doe"},
        "de": {"first_name": "Johann", "last_name": "Doe"}
    },
    "nicknames": ["JD", "Johnny"],
    "public": True,
    "relationship_modifier": "adopted",
    "suffix": "Jr.",
    "title": "Mr."
}

noneParamsAddChild: dict[str, None] = {k: None for k in sampleParamsAddChild}

sampleParamsAddParent = sampleParamsAddChild.copy()
noneParamsAddParent: dict[str, None] = {k: None for k in sampleParamsAddParent}

sampleParamsAddPartner = sampleParamsAddChild.copy()
noneParamsAddPartner: dict[str, None] = {k: None for k in sampleParamsAddPartner}

sampleParamsAddSibling = sampleParamsAddChild.copy()
noneParamsAddSibling: dict[str, None] = {k: None for k in sampleParamsAddSibling}