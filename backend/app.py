from flask import Flask
from routes.match_route import match_bp
from routes.user_route import usuario_bp
from routes.predicciones_route import predicciones_bp

app = Flask(__name__)

@app.route("/")
def index():
    return "Esta funcionando!"

app.register_blueprint(match_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(predicciones_bp)

if __name__== "__main__":
    app.run(port=8000, debug=True)