import datetime
import pprint
from sqlalchemy import and_
from models.user import User
from models.work_time import WorkTime


class RecordController:
    
    def __init__(self, user_id):
        self.user = User.query.filter(User.id == user_id).first()
        
    def get_records(self, day_start, day_end, user_id):
        date_start = datetime.datetime.strptime(f'{day_start} 00:00:00', '%d-%m-%Y %H:%M:%S')
        date_end = datetime.datetime.strptime(f'{day_end} 23:59:59', '%d-%m-%Y %H:%M:%S')
        if self.user.is_admin:
            records_db = WorkTime.query.where(and_((WorkTime.start>=date_start), (WorkTime.finish<=date_end), (WorkTime.user_id==user_id))).all()
        else:
            records_db = WorkTime.query.where(and_((WorkTime.start>=date_start), (WorkTime.finish<=date_end), (WorkTime.user_id==self.user))).all()
        return records_db
    
    def records_to_list(self, records):
        result = []
        total = 0
        for record in records:
            diff = self._get_diff(record.start, record.finish)
            total+= diff.seconds
            diff_str = str(diff)
            result.append({'start':record.start, 'finish':record.finish, 'comment':record.comment, 'diff':diff.seconds, 'diff_str':diff_str})
        result.append(total)
        return result
            
    def _get_diff(self, start, finish):
        return finish - start