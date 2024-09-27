import datetime
import pprint

from sqlalchemy import and_

from app.db import db
from models.user import User
from models.work_time import WorkTime
from workers.decorators import user_permissions, is_admin


class WorkerController:

    def __init__(self, user_id=None, email=None):
        if user_id:
            self.user = User.query.filter(User.id == user_id).first()
        if email:
            self.user = User.query.filter(User.email == email).first()



    @is_admin
    def get_worker_info(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return {'error': True, 'msg': 'User not found'}
        return {'error': False, 'data': user.get_user()}

    @is_admin
    def change_active(self, user_id):
        user = User.query.filter(User.id == user_id).first()

        user.is_active = not user.is_active
        db.session.commit()

        return {'error': False}

    @is_admin
    def update_worker(self, user_id, data):
        user = User.query.filter(User.id == user_id).first()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.position = data['position']
        user.email = data['email']
        user.document = data['document']
        user.phone = data['phone']
        db.session.commit()

        return {'error': False}

    @user_permissions
    @is_admin
    def get_report(self, user_id, data):
        # TODO add report
        user = User.query.filter(User.id == user_id).first()
        return {'error': False}

    @is_admin
    def get_workers(self):
        users = User.query.filter(User.id != self.user.id).all()
        return {'error': False, 'data': [user.get_user() for user in users]}

    @is_admin
    def get_working_users(self):
        users = WorkTime.query.filter(WorkTime.finish.is_(None)).join(User).all()
        result = []

        for user in users:
            result.append({
                'id': user.user_id,
                'first_name': user.user.first_name,
                'last_name': user.user.last_name,
                'start': user.start,
            })
        if not result:
            return {'error': False, 'data': []}
        return {'error': False, 'data': result}
