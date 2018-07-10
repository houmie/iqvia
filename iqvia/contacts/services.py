from sqlalchemy import func
from .models import Contact
import re


def validate_username(username: str) -> bool:
    """
    Checking that the username is valid (length and characters)
    :param str username: the username to be validated.
    e.g: 'we9fdoie023kd'
    :return bool: True if valid username.
    """
    return True if re.match("^([a-zA-Z0-9]|\.){6,32}$", username) else False


def does_contact_username_exist(username: str):
    """
    True if a contact already exists with this username.
    :param str username: The username to verify the unicity of.
    e.g: 'username1234'
    :return bool: True if a contact with this username does exist.
    """
    return Contact.query.filter(func.lower(Contact.username) == func.lower(str(username))).scalar() is not None


def does_contact_email_exist(email: str):
    """
    True if a contact already exists with this email.
    :param str email: The email to verify the unicity of.
    e.g: 'guyemailaddress@gmail.com'
    :return bool: True if a contact with this email does exist.
    """
    return Contact.query.filter(func.lower(Contact.email) == func.lower(str(email))).scalar() is not None
