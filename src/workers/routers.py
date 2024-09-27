from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from workers.controllers.record import RecordController
from workers.controllers.worker import WorkerController
from workers.helpers import records_to_list

worker_module = Blueprint('workers', __name__)


@worker_module.route('/', methods=['GET'])
@jwt_required()
def get_workers():
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return controller.get_workers()


@worker_module.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_worker_info(user_id):
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return controller.get_worker_info(user_id)


@worker_module.route('/<user_id>', methods=['PATCH'])
@jwt_required()
def change_active(user_id):
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return controller.change_active(user_id)


@worker_module.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_worker(user_id):
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return controller.update_worker(user_id, request.get_json())


@worker_module.route('/working', methods=['GET'])
@jwt_required()
def get_working_users():
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return jsonify(controller.get_working_users())


@worker_module.route('/records', methods=['POST'])
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    data = request.get_json()
    work_records = controller.get_records(data['start'], data['end'], data['user_id'])
    return jsonify({'error': False, 'data': records_to_list(work_records)})


@worker_module.route('/records/start', methods=["GET"])
@jwt_required()
def start_work():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    return jsonify(controller.start_work())


@worker_module.route('/records/finish', methods=["GET"])
@jwt_required()
def finish_work():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    return jsonify(controller.finish_work())


@worker_module.route('/records/comments', methods=["POST"])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    comment = request.get_json()['comment']
    work_time_id = request.get_json()['id']
    controller = RecordController(user_id)
    return jsonify(controller.add_comment(work_time_id, comment))


@worker_module.route('/records/chronometer', methods=['GET'])
@jwt_required()
def get_chronometer():
    user_id = get_jwt_identity()
    controller = RecordController(user_id)
    return jsonify(controller.get_chronometer())


@worker_module.route('/report/<user_id>', methods=['POST'])
@jwt_required()
def get_report(user_id):
    actual_user_id = get_jwt_identity()
    controller = WorkerController(actual_user_id)
    return controller.get_report(user_id, request.get_json())
