from .. import post, get, delete
from iqvia.contacts.models import Contact
from unittest.mock import Mock


def test_add_contact_ok(monkeypatch):
    """
    Testing a valid contact creation.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstname",
                 "surname": "testsurname",
                 "email": "testemail2@gmail.com",
                 "username": "testusername1234"}

    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))
    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=False))
    status_code, response_data = post('contacts/', test_data)

    assert response_data == {'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'first_name': 'tesfirstname',
                             'surname': 'testsurname',
                             'username': 'testusername1234',
                             'email': 'testemail2@gmail.com'}
    assert status_code == 200
    assert database_mock.call_count == 2


def test_add_contact_nok_username_already_exists(monkeypatch):
    """
    Testing an invalid contact creation: the username already exists
    :return:
    """
    test_data = {"first_name": "tesfirstname",
                 "surname": "testsurname",
                 "email": "testemail2@gmail.com",
                 "username": "testusername1234"}
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=True))
    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=False))
    status_code, response_data = post('contacts/', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, the username testusername1234 '
                                                    'of the contact you try to add already exists'}]}
    assert status_code == 400
    assert database_mock.call_count == 0


def test_add_contact_nok_email_already_exists(monkeypatch):
    """
    Testing an invalid contact creation: the email already exists
    :return:
    """
    test_data = {"first_name": "tesfirstname",
                 "surname": "testsurname",
                 "email": "testemail@gmail.com",
                 "username": "testusername1234"}
    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))
    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=True))
    status_code, response_data = post('contacts/', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, the email testemail@gmail.com '
                                                    'of the contact you try to add already exists'}]}
    assert status_code == 400


def test_get_contacts_ok(monkeypatch):
    """
    Testing a valid contact fetching: list of contacts found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    contact_1 = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname1',
                        surname='testsurname1', username='testusername1234', email='testemail1@gmail.com')
    contact_2 = Contact(id='6e8377af-bdc3-4b9e-a491-2d9ddff3253g', first_name='testfirstname2',
                        surname='testsurname2', username='testusername4567', email='testemail12@gmail.com')

    monkeypatch.setattr('iqvia.contacts.views.Contact', Mock(query=Mock(all=Mock(return_value=[contact_1, contact_2]))))

    status_code, response_data = get('contacts/')
    assert response_data == {'contacts': [{'email': 'testemail1@gmail.com',
                                           'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                                           'username': 'testusername1234',
                                           'surname': 'testsurname1',
                                           'first_name': 'testfirstname1'},
                                          {'email': 'testemail12@gmail.com',
                                           'id': '6e8377af-bdc3-4b9e-a491-2d9ddff3253g',
                                           'username': 'testusername4567',
                                           'surname': 'testsurname2',
                                           'first_name': 'testfirstname2'}]}
    assert status_code == 200


def test_get_contact_by_username_ok(monkeypatch):
    """
    Testing a valid get by username scenario.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', email='testemail1@gmail.com')
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))

    status_code, response_data = get('contacts/testsurname')
    assert response_data == {'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'surname': 'testsurname',
                             'username': 'testusername1234',
                             'email': 'testemail1@gmail.com',
                             'first_name': 'testfirstname'}
    assert status_code == 200


def test_get_contact_by_username_nok_contact_not_found(monkeypatch):
    """
    Testing an invalid get by username scenario: contact not found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None))))))

    status_code, response_data = get('contacts/wrongusername')

    assert response_data == {'errors': [{'message': 'Sorry, there is no contact with the username wrongusername'}]}

    assert status_code == 400


def test_delete_contacts_ok(monkeypatch):
    """
    Testing a valid delete scenario.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', email='testemail1@gmail.com')
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))
    monkeypatch.setattr('iqvia.contacts.views.db.session.delete', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)

    status_code = delete('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f')

    assert database_mock.call_count == 2
    assert status_code == 204


def test_delete_contacts_nok_contact_not_found(monkeypatch):
    """
    Testing a invalid delete scenario: contact not found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None))))))
    monkeypatch.setattr('iqvia.contacts.views.db.session.delete', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    status_code = delete('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f')
    assert status_code == 400
    assert database_mock.call_count == 0


def test_update_contact_ok(monkeypatch):
    """
    Testing a valid contact update.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "email": "testemail2comUPDATED@gmail.com",
                 "username": "testusername1234UPDATED"}

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', email='testemail1@gmail.com')
    database_mock = Mock()

    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))
    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=False))
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'first_name': 'tesfirstnameUPDATED',
                             'id': '7e8377af-bdc3-4b9e-a491-2d9ddff3253f',
                             'email': 'testemail2comUPDATED@gmail.com',
                             'surname': 'testsurnameUPDATED',
                             'username': 'testusername1234UPDATED'}

    assert status_code == 200
    assert database_mock.call_count == 1


def test_update_contact_nok_username_already_exists(monkeypatch):
    """
    Testing a invalid contact update: the username passed already exists.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "email": "testemail2comUPDATED@gmail.com",
                 "username": "testusername1234UPDATED"}

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', email='testemail1@gmail.com')
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)

    # Username already exists
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=True))

    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=False))
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, you cannot update the contact '
                                                    'with the username testusername1234: it already exists'}]}

    assert status_code == 400
    assert database_mock.call_count == 0


def test_update_contact_nok_email_already_exists(monkeypatch):
    """
    Testing a invalid contact update: the email passed already exists.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "email": "testemail2comUPDATED@gmail.com",
                 "username": "testusername1234UPDATED"}

    contact = Contact(id='7e8377af-bdc3-4b9e-a491-2d9ddff3253f', first_name='testfirstname',
                      surname='testsurname', username='testusername1234', email='testemail1@gmail.com')
    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.uuid4', Mock(return_value='7e8377af-bdc3-4b9e-a491-2d9ddff3253f'))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)

    # Email already exists
    monkeypatch.setattr('iqvia.contacts.views.does_contact_username_exist', Mock(return_value=False))

    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=True))
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=contact))))))
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, you cannot update the contact '
                                                    'with the email testemail1@gmail.com: it already exists'}]}

    assert status_code == 400
    assert database_mock.call_count == 0


def test_update_contact_nok_contact_not_found(monkeypatch):
    """
    Testing a invalid contact update: the contact is not found.
    :param monkeypatch: a monkeypatching instance.
    :return:
    """
    test_data = {"first_name": "tesfirstnameUPDATED",
                 "surname": "testsurnameUPDATED",
                 "email": "testemail2comUPDATED@gmail.com",
                 "username": "testusername1234UPDATED"}

    database_mock = Mock()
    monkeypatch.setattr('iqvia.contacts.views.does_contact_email_exist', Mock(return_value=True))
    monkeypatch.setattr('iqvia.contacts.views.db.session.add', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.db.session.commit', database_mock)
    monkeypatch.setattr('iqvia.contacts.views.Contact',
                        Mock(query=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None))))))
    status_code, response_data = post('contacts/7e8377af-bdc3-4b9e-a491-2d9ddff3253f', test_data)

    assert response_data == {'errors': [{'message': 'Sorry, the contact 7e8377af-bdc3-4b9e-a491-2d9ddff3253f '
                                                    'you try to update does not exist'}]}

    assert status_code == 400
    assert database_mock.call_count == 0
