from flask import Flask, request, jsonify
import os

app = Flask(__name__)

GREETING_PREFIX = os.environ.get("GREETING_PREFIX", "Hello")


@app.route("/greet")
def greet():
    name = request.args.get("name", "World")
    return jsonify({"message": f"{GREETING_PREFIX}, {name}!"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
