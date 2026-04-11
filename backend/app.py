from flask import Flask, request
from routes.match_route import match_bp
from routes.user_route import user_bp

app = Flask(__name__)

@app.route("/")
def index():
    return "Esta funcionando!"

app.register_blueprint(match_bp)
app.register_blueprint(user_bp)

if __name__== "__main__":
    app.run(port=8000, debug=True)