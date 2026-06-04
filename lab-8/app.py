from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
data = {}


def load_data():
    global data

    if not os.path.exists(DATA_FILE):
        data = {}
        save_data()
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = {}


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@app.route("/set", methods=["POST"])
@limiter.limit("10 per minute")
def set_value():

    request_data = request.get_json()

    if not request_data:
        return jsonify({"error": "Необходимо передать JSON-данные"}), 400

    key = request_data.get("key")
    value = request_data.get("value")

    if key is None or value is None:
        return jsonify({"error": "Поля key и value обязательны"}), 400

    data[key] = value
    save_data()

    return jsonify({
        "message": "Данные успешно сохранены",
        "key": key,
        "value": value
    }), 201


@app.route("/get/<key>", methods=["GET"])
def get_value(key):
    if key not in data:
        return jsonify({"error": "Ключ не найден"}), 404

    return jsonify({
        "key": key,
        "value": data[key]
    })


@app.route("/delete/<key>", methods=["DELETE"])
@limiter.limit("10 per minute")
def delete_value(key):
    if key not in data:
        return jsonify({"error": "Ключ не найден"}), 404

    deleted_value = data.pop(key)
    save_data()

    return jsonify({
        "message": "Ключ успешно удалён",
        "key": key,
        "deleted_value": deleted_value
    })


@app.route("/exists/<key>", methods=["GET"])
def exists_key(key):
    return jsonify({
        "key": key,
        "exists": key in data
    })


if __name__ == "__main__":
    load_data()
    app.run(debug=True)