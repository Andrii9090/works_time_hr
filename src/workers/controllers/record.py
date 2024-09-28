import datetime

from sqlalchemy import and_

from app.db import db
from models.user import User
from models.work_time import WorkTime


class RecordController:

    def     __init__(self, user_id):
        self.user = User.query.filter(User.id == user_id).first()

    def get_records(self, day_start, day_end, user_id=None):
        date_start = datetime.datetime.strptime(day_start, '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(day_end, '%Y-%m-%d').date()
        if self.user.is_admin and user_id:
            user_id = int(user_id)
        else:
            user_id = self.user.id
        records_db = WorkTime.query.where(
            WorkTime.date >= date_start, WorkTime.date <= date_end, WorkTime.user_id == user_id).order_by(
            WorkTime.date.desc()).all()
        return records_db

    def get_chronometer(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        work_time = WorkTime.query.filter(WorkTime.finish.is_(None), WorkTime.user_id == self.user.id).order_by(
            WorkTime.date.desc()).first()
        if work_time:
            diff = now - datetime.datetime(work_time.start.year,
                                           work_time.start.month,
                                           work_time.start.day,
                                           work_time.start.hour,
                                           work_time.start.minute,
                                           work_time.start.second,
                                           tzinfo=datetime.timezone.utc)

            hours = diff.total_seconds() // 3600
            minutes = (diff.seconds // 60) % 60
            seconds = diff.seconds % 60
            result = {'error': False, 'data': {
                'hours': hours,
                'minutes': minutes,
                'seconds': seconds
            }}
            return result
        else:
            return {'error': True, 'msg': 'User is not working'}

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