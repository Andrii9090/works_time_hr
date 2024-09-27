from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from users.controllers.user import UserController

user_module = Blueprint('users', __name__, template_folder='templates')


@user_module.route('/', methods=["POST"])
@jwt_required()
def create_user():
    user_id = get_jwt_identity()
    result = UserController.create_user(user_id, request.get_json())
    return jsonify(result)


@user_module.route('/user', methods=["GET"])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    controller = UserController(user_id)
    result = controller.get_user_info()
    return jsonify(result)


@user_module.route('/user', methods=["PUT"])
@jwt_required()
def update_user_info():
    user_id = get_jwt_identity()
    controller = UserController(user_id)
    result = controller.update_user(request.get_json())
    return jsonify(result)


@user_module.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    return jsonify(UserController.login(email, password))


@user_module.route('/login/admin', methods=["POST"])
def login_admin():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    return jsonify(UserController.login(email, password, True))


@user_module.route('/confirm/<code>')
def confirm(code):
    if request.method == 'GET':
        user_id, code = code.split('_')
        return render_template('confirm.html', data={'code': code, 'user_id': user_id})
    if request.method == 'POST':
        password = request.form.get('password')
        password_1 = request.form.get('password_1')
        code = request.form.get('code')
        user_id = request.form.get('user_id')

        return UserController.confirm(code, user_id, password, password_1)
