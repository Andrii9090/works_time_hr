from typing import List
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db
from app.addons import bcrypt


class User(db.Model):
    first_name: Mapped[str]
    last_name: Mapped[str]
    _password: Mapped[str] = mapped_column(name='password')
    position: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    document: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    times: Mapped[List['WorkTime']] = relationship()

    def __init__(self, first_name, last_name, position, phone, password, email, document):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.phone = phone
        self.email = email
        self.document = document
        self._password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.generate_hash_password(password)

    @staticmethod
    def generate_hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def generate_temp_pass():
        return str(uuid.uuid4())

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'


class UserRegistered(db.Model):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    hash: Mapped[str]

    def __init__(self, user_id):
        self.user_id = user_id
        self.hash = User.generate_temp_pass()
