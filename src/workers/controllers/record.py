import datetime
import pprint
from sqlalchemy import and_, or_
from models.user import User
from models.work_time import WorkTime


class RecordController:

    def __init__(self, user_id):
        self.user = User.query.filter(User.id == user_id).first()

    def get_records(self, day_start, day_end, user_id=None):
        date_start = datetime.datetime.strptime(day_start, '%d-%m-%Y').date()
        date_end = datetime.datetime.strptime(day_end, '%d-%m-%Y').date()
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
