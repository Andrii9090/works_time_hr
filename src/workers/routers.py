from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from workers.controllers.record import RecordController
from users.controllers.user import UserController
from workers.controllers.worker import WorkerController
from workers.helpers.mail import send_register_mail


worker_model = Blueprint('workers', __name__)

@worker_model.route('/', methods=["POST"])
@jwt_required()
def create_worker():
    user_id = get_jwt_identity()
    return jsonify(UserController.createUser(user_id, request.get_json()))

@worker_model.route('/start', methods=["GET"])
@jwt_required()
def start_work():
    user_id = get_jwt_identity()
    controller = WorkerController(user_id)
    return jsonify(controller.start_work())
    
@worker_model.route('/finish', methods=["GET"])
@jwt_required()
def finish_work():
    user_id = get_jwt_identity()
    controller = WorkerController(user_id)
    return jsonify(controller.finish_work())
    
@worker_model.route('/comments', methods=["POST"])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    comment = request.get_json()['comment']
    work_time_id = request.get_json()['id']
    controller = WorkerController(user_id)
    return jsonify(controller.add_comment(work_time_id, comment))

@worker_model.route('/records', methods=['POST'])
@jwt_required()
def records():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    data = request.get_json()
    records = controller.get_records(data['start'], data['end'])
    return jsonify(controller.records_to_list(records))

@worker_model.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    return jsonify(UserController.login(email, password))
    