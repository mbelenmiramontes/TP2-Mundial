from flask import Blueprint, request
from controller.user_controller import get_users


user_bp = Blueprint('user', __name__)

@user_bp.route("/usuarios", methods=["GET"])
def list_users():
    return get_users(request)