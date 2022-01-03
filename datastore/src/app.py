from flask import Flask, jsonify
from os import environ

SECRET_KEY = environ.get("SECRET_KEY")
print("SECRET KEY", SECRET_KEY)
app = Flask(__name__)

@app.route("/api")
def api():
    d = { "key": "value" }
    return jsonify(d)

if __name__ == "__main__":
    app.run(host='0.0.0.0')