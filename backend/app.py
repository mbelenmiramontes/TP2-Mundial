from flask import Flask, request


app = Flask(__name__)

@app.route("/")
def index():
    return "Esta funcionando!"

if __name__== "__main__":
    app.run(port=8000, debug=True)