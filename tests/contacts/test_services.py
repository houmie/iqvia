from iqvia.contacts.services import validate_username, does_contact_username_exist
from unittest.mock import Mock


def test_valid_usernames():
    """
    Testing valid usernames.
    :return:
    """
    assert validate_username('rewrijofsdfn') is True
    assert validate_username('1234687990.3') is True


def test_invalid_usernames():
    """
    Testing invalid usernames. Invalid characters and invalid length.
    :return:
    """
    assert validate_username('?Fd0***32ew%%%') is False
    assert validate_username('waaaaaaaaaaaaaaaaaytooooooooooolongggggggggggggggggggggggggggggggggggggggggggg') is False


def test_contact_exists(monkeypatch):
    """
    Testing contact exists.
    n.b: 1 entry found, scalar() returns 1.
    :return:
    """
    monkeypatch.setattr('iqvia.contacts.services.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(scalar=Mock(return_value=1))))))

    assert does_contact_username_exist('username') is True


def test_contact_doesnt_exists(monkeypatch):
    """
    Testing contact exists.
    n.b: 0 entry found, scalar() returns None.
    :return:
    """
    monkeypatch.setattr('iqvia.contacts.services.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(scalar=Mock(return_value=None))))))
    assert does_contact_username_exist('username') is False
