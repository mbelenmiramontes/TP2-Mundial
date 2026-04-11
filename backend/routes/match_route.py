from flask import Blueprint

match_bp = Blueprint('match', __name__)
@match_bp.route("/partidos", methods=["GET"])
def listar_partidos():
    return

