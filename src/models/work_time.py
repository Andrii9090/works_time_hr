import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.db import db


class WorkTime(db.Model):
    date: Mapped[datetime.date]
    start: Mapped[datetime.datetime]
    finish: Mapped[datetime.datetime] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, date, user_id):
        self.date = date.date()
        self.start = date
        self.user_id = user_id

    def __str__(self):
        return f'{self.user_id} - {self.date} {self.start} - {self.finish}'

    def __repr__(self):
        return self.__str__()
