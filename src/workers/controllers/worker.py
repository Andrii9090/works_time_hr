import datetime

from app.db import db
from models.user import User
from models.work_time import WorkTime
from workers.helpers.mail import send_register_mail

class WorkerController:
    
    def __init__(self, user_id=None, email=None):
        if user_id:
            self.user = User.query.filter(User.id == user_id).first()
        if email:
            self.user = User.query.filter(User.email == email).first()

    def start_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start_time = WorkTime(now, self.user.id)
        db.session.add(start_time)
        db.session.commit()
        return {'error':False,'msg':'Saved'}
    
    def finish_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        last_row = WorkTime.query.filter(WorkTime.finish == None, WorkTime.user_id == self.user.user_id).first()
        if last_row:
            last_row.finish = now
            db.session.commit()
            return {'msg':'Saved','error':False}
        else:
            return {'msg':'Error', 'error':True}
        
    def add_comment(self, id,comment):
        last_row = WorkTime.query.filter(WorkTime.id == id).first()
        last_row.comment = comment
        db.session.commit()
