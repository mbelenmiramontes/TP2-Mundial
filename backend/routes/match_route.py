from flask import Blueprint

match_bp = Blueprint('match', __name__)
@match_bp.route("/partido", methods=["GET", "POST"])
def procesar_partido():
    if request.method == "GET":
        

