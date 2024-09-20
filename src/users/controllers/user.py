import datetime
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from app.db import db
from decorators import catch_errors
from models.user import User
from models.work_time import WorkTime
from workers.helpers.mail import send_register_mail

class UserController:
    
    def __init__(self, user_id=None, email=None):
        if user_id:
            self.user = User.query.filter(User.id == user_id).first()
        if email:
            self.user = User.query.filter(User.email == email).first()
    
    @staticmethod
    @catch_errors(IntegrityError, {'error':True, 'msg':'Email is exist!'})
    def createUser(admin_user_id, data):
        admin_user = User.query.filter(User.id == admin_user_id, User.is_admin == True)
        if admin_user:
            pasword = User.generate_temp_pass()
            user = User(data['first_name'], data['last_name'], data['position'], pasword, data['email'])
            db.session.add(user)
            db.session.commit()
            hash = db.session.query(User).filter(User.email == data['email']).first()
            send_register_mail(hash.password)
            return {'error':False, 'msg':'User has been registered'}
        else:
            return {'error':True, 'msg':'User don\'t have permissions'}
        
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
        
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email, password=password).first()

        if user is None:
            return {"error":True, "msg": "Bad username or password"}
        
        access_token = create_access_token(identity=user.id)
        return  { "error":False, "token": access_token }
            