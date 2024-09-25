import datetime

from sqlalchemy import and_

from app.db import db
from models.user import User
from models.work_time import WorkTime


class WorkerController:

    def __init__(self, user_id=None, email=None):
        if user_id:
            self.user = User.query.filter(User.id == user_id).first()
        if email:
            self.user = User.query.filter(User.email == email).first()

    def start_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if WorkTime.query.filter(and_(WorkTime.user_id == self.user.id, WorkTime.finish.is_(None))).first():
            return {'error': True, 'msg': 'User is working'}
        work_time = WorkTime(now, self.user.id)
        db.session.add(work_time)
        db.session.commit()
        return {'error': False, 'msg': 'Saved'}

    def finish_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        last_row = WorkTime.query.filter(and_(WorkTime.finish.is_(None), WorkTime.user_id == self.user.id)).first()
        if last_row:
            last_row.finish = now
            db.session.commit()
            return {'msg': 'Saved', 'error': False}
        else:
            return {'msg': 'Error', 'error': True}

    @staticmethod
    def add_comment(comment_id, comment):
        work_time = WorkTime.query.filter(WorkTime.id == comment_id).first()
        if work_time:
            work_time.comment = comment
            db.session.commit()
            return {'msg': 'Saved', 'error': False}
        else:
            return {'msg': 'Error', 'error': True}

