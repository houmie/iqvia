from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from .. import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(UUID, primary_key=True)
    first_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
