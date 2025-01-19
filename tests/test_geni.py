import pytest

from geni.geni import Geni
from geni.profile import Profile
from geni.user import User


_classes = {
    "profile": Profile,
    "user": User
}


def test_only_allow_fixed_attributes():
    geni = Geni(api_key="test_api_key")

    # Ensure no other attributes are added. Only these representing the Geni API classes are allowed.
    assert len(geni.__dict__) == len(_classes)


def test_attributes_match_api_classes():
    geni = Geni(api_key="test_api_key")

    for attr, cls in _classes.items():
        assert hasattr(geni, attr)
        assert isinstance(getattr(geni, attr), cls)

def test_api_key_is_passed_to_classes():
    api_key = "test_api_key"
    geni = Geni(api_key=api_key)

    for attr, cls in _classes.items():
        assert getattr(geni, attr)._auth._api_key == api_key
