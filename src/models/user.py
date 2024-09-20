from typing import List
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db
from app.addons import bcrypt

class User(db.Model):
    first_name:Mapped[str]
    last_name:Mapped[str]
    password:Mapped[str]
    position:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    is_active:Mapped[bool] = mapped_column(default=True)
    is_admin:Mapped[bool] = mapped_column(default=False)
    times:Mapped[List['WorkTime']] = relationship()
    
    def __init__(self, first_name, last_name, position, password, email):
        self.first_name = first_name
        self.last_name = last_name 
        self.position = position
        self.email = email
        self.password = self._generate_hash_password(password)
        
    def _generate_hash_password(self, password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    @staticmethod
    def generate_temp_pass():
        return str(uuid.uuid4())
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
    
    
