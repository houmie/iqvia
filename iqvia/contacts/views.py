from flask import Blueprint
from uuid import uuid4
from .services import does_contact_username_exist, does_contact_email_exist
from .schemas import ContactSchema
from .models import Contact
from .. import db, io

app = Blueprint('contacts', __name__, url_prefix='/contacts')


@app.route('/', methods=['POST'])
@io.from_body('contact', ContactSchema)
@io.marshal_with(ContactSchema)
def add_contact(contact):
    """
    @api {post} /contacts Adds a contact
    @apiDescription Adds a new contact
    @apiName add_contact
    @apiGroup Contacts

    @apiParam (Body) {String{1-50}}      first_name           The first name of the contact.
    @apiParam (Body) {String{1-50}}      surname              The surname of the contact.
    @apiParam (Body) {String{6-32}}      username             The username of the contact.
    @apiParam (Body) {String{5-128}}     email                The email of the contact.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {String{5-128}}          email                The email of the contact.
    """
    contact.id = str(uuid4())

    if does_contact_username_exist(contact.username):
        return io.bad_request('Sorry, the username {} of the contact you try '
                              'to add already exists'.format(contact.username))

    if does_contact_email_exist(contact.email):
        return io.bad_request('Sorry, the email {} of the contact you try '
                              'to add already exists'.format(contact.email))
    db.session.add(contact)
    db.session.commit()

    return contact


@app.route('/', methods=['GET'])
@io.marshal_with(ContactSchema, envelope='contacts')
def get_contacts():
    """
    @api {get} /contacts Gets all the contacts
    @apiDescription Gets all the contacts
    @apiName get_contacts
    @apiGroup Contacts

    @apiSuccess {Array}                  contacts                The contacts retrieved.
    @apiSuccess {UUID}                   contacts.id             The ID of the contact.
    @apiSuccess {String{1-50}}           contacts.first_name     The first name of the contact.
    @apiSuccess {String{1-50}}           contacts.surname        The surname of the contact.
    @apiSuccess {String{6-32}}           contacts.username       The username of the contact.
    @apiSuccess {String{5-128}}          contacts.email          The email of the contact.
    """
    return Contact.query.all()


@app.route('/<string:username>', methods=['GET'])
@io.marshal_with(ContactSchema)
def get_contact_by_username(username):
    """
    @api {get} /contacts/<username> Gets a contact
    @apiDescription Gets a contact by username
    @apiName get_contacts
    @apiGroup Contacts

    @apiParam {String{6-32}}             [username]           Username of the contact.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {String{5-128}}          email                The email of the contact.
    """
    contact = Contact.query.filter(Contact.username == str(username)).first()
    if not contact:
        return io.bad_request('Sorry, there is no contact with the username {}'.format(username))
    return contact


@app.route('/<uuid:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """
    @api {delete} /contacts/<contact_id> Deletes a contact
    @apiDescription Deletes a contact
    @apiName delete_contact
    @apiGroup Contacts

    @apiParam {UUID}  contact_id  The ID of the contact.
    """
    contact = Contact.query.filter(Contact.id == str(contact_id)).first()
    if not contact:
        return io.bad_request('Sorry, the contact {} you try to delete does not exist'.format(contact_id))

    db.session.delete(contact)
    db.session.commit()


@app.route('/<uuid:contact_id>', methods=['PATCH', 'PUT', 'POST'])
@io.from_body('contact_data', ContactSchema(partial=True))
@io.marshal_with(ContactSchema())
def update_contact(contact_id, contact_data):
    """
    @api {patch} /contacts/<contact_id> Updates an item
    @apiDescription Updates a contact
    @apiName update_contact
    @apiGroup Contacts

    @apiParam (Body) {String{1-50}}      [first_name]         The first name of the contact.
    @apiParam (Body) {String{1-50}}      [surname]            The last name of the contact.
    @apiParam (Body) {String{1-32}}      [username]           The username of the contact.
    @apiParam (Body) {String{128}}       [email]              The email of the contact.

    @apiSuccess {UUID}                   id                   The ID of the contact.
    @apiSuccess {String{1-50}}           first_name           The first name of the contact.
    @apiSuccess {String{1-50}}           surname              The surname of the contact.
    @apiSuccess {String{6-32}}           username             The username of the contact.
    @apiSuccess {String{5-128}}          email                The email of the contact.
    """
    contact = Contact.query.filter(Contact.id == str(contact_id)).first()
    if not contact:
        return io.bad_request('Sorry, the contact {} you try to update does not exist'.format(contact_id))

    if 'username' in contact_data and does_contact_username_exist(contact.username):
        return io.bad_request('Sorry, you cannot update the contact '
                              'with the username {}: it already exists'.format(contact.username))

    if 'email' in contact_data and does_contact_email_exist(contact.email):
        return io.bad_request('Sorry, you cannot update the contact '
                              'with the email {}: it already exists'.format(contact.email))

    # TODO: use fromdict
    if 'first_name' in contact_data:
        contact.first_name = contact_data['first_name']
    if 'surname' in contact_data:
        contact.surname = contact_data['surname']
    if 'username' in contact_data:
        contact.username = contact_data['username']
    if 'email' in contact_data:
        contact.email = contact_data['email']

    db.session.commit()
    return contact
