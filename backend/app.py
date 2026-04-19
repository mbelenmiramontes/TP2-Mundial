from flask import Flask
from rutas import partido_bp, usuario_bp, predicciones_bp, ranking_bp

app = Flask(__name__)

@app.route("/")
def index():
    return "API Backend de ProDe levantada correctamente."

# Registro de blueprints para las modulaciones de rutas
app.register_blueprint(partido_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(predicciones_bp)
app.register_blueprint(ranking_bp)

if __name__== "__main__":
    app.run(port=8000, debug=True)