from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from users.helpers.record import records_to_list
from workers.controllers.record import RecordController
from workers.controllers.worker import WorkerController

worker_module = Blueprint('workers', __name__)


@worker_module.route('/records/start', methods=["GET"])
@jwt_required()
def start_work():
    user_id = get_jwt_identity()
    controller = WorkerController(user_id)
    return jsonify(controller.start_work())


@worker_module.route('/records/finish', methods=["GET"])
@jwt_required()
def finish_work():
    user_id = get_jwt_identity()
    controller = WorkerController(user_id)
    return jsonify(controller.finish_work())


@worker_module.route('/records/comments', methods=["POST"])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    comment = request.get_json()['comment']
    work_time_id = request.get_json()['id']
    controller = WorkerController(user_id)
    return jsonify(controller.add_comment(work_time_id, comment))


@worker_module.route('/records', methods=['POST'])
@jwt_required()
def records():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    data = request.get_json()
    records = controller.get_records(data['start'], data['end'])
    return jsonify(records_to_list(records))
