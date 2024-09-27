import datetime
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from app.db import db
from decorators import catch_errors
from models.user import User, UserRegistered
from models.work_time import WorkTime
from users.helpers.mail import send_register_mail


class UserController:

    def __init__(self, user_id=None, email=None):
        if user_id:
            self.user = User.query.filter(User.id == user_id).first()
        if email:
            self.user = User.query.filter(User.email == email).first()

    @staticmethod
    @catch_errors(IntegrityError, {'error': True, 'msg': 'Email is exist!'})
    def create_user(admin_user_id, data):
        admin_user = User.query.filter(User.id == admin_user_id).first()
        if admin_user.is_admin:
            existed_user = User.query.filter(User.email == data['email']).first()
            if existed_user is not None:
                return {'error': True, 'msg': 'Email is exist!'}
            else:
                password = User.generate_temp_pass()
                user = User(first_name=data['first_name'], last_name=data['last_name'], position=data['position'],
                            email=data['email'], document=data['document'], phone=data['phone'], password=password)
                db.session.add(user)
                db.session.commit()
                new_user = db.session.query(User).filter(User.email == data['email']).first()
                temp_user_data = UserRegistered(new_user.id)
                db.session.add(temp_user_data)
                db.session.commit()
                send_register_mail(new_user.id, temp_user_data.hash)
                return {'error': False, 'msg': 'User has been registered'}
        else:
            return {'error': True, 'msg': 'User don\'t have permissions'}

    def start_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start_time = WorkTime(now, self.user.id)
        db.session.add(start_time)
        db.session.commit()
        return {'error': False, 'msg': 'Saved'}

    def finish_work(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        last_row = WorkTime.query.filter(WorkTime.finish.is_(None), WorkTime.user_id == self.user.id).first()
        if last_row:
            last_row.finish = now
            db.session.commit()
            return {'msg': 'Saved', 'error': False}
        else:
            return {'msg': 'Error', 'error': True}

    @staticmethod
    def add_comment(record_id, comment):
        last_row = WorkTime.query.filter(WorkTime.id == record_id).first()
        last_row.comment = comment
        db.session.commit()

    @staticmethod
    def login(email, password, is_admin=False):
        user = User.query.filter_by(email=email).first()

        if user is None:
            return {"error": True, "msg": "Bad username or password"}
        if user:
            if not user.is_active:
                return {"error": True, "msg": "User is not active"}
            if is_admin and not user.is_admin:
                return {"error": True, "msg": "User don't have permissions"}
            if not user.check_password(user.password, password):
                return {"error": True, "msg": "Bad username or password"}

        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=180))
        return {"error": False, "data": {"token": access_token}}

    @staticmethod
    def confirm(code, user_id, password, password_1):
        user_register = UserRegistered.query.filter_by(user_id=int(user_id), hash=code).first()
        if not user_register:
            return 'User not found'
        if user_register and password == password_1:
            user = User.query.filter(User.id == user_register.user_id).first()
            user.password = password
            db.session.delete(user_register)
            db.session.commit()
            return 'User has been activated'
        else:
            return 'User not found'

    def get_user_info(self):
        return {'error': False, 'data': self.user.get_user()}

    def update_user(self, data):
        for key, value in data.items():
            setattr(self.user, key, value)
        db.session.commit()
        return {'error': False, 'data': self.user.get_user()}