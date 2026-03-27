import random
from flask import Flask, request, jsonify

app = Flask(__name__)

def apply_operation(a, b, operation):
    if operation == "sum":
        return a + b
    elif operation == "sub":
        return a - b
    elif operation == "mul":
        return a * b
    elif operation == "div":
        if b == 0:
            return None  # деление на ноль недопустимо
        return a / b

def get_random_operation():
    return random.choice(["sum", "sub", "mul", "div"])

# 1) GET
@app.route('/number/', methods=['GET'])
def get_number():
    try:
        param = float(request.args.get('param'))
    except (TypeError, ValueError):
        return jsonify({"error": "param должен быть числом"}), 400

    rand_num = random.randint(1, 10)
    result = apply_operation(rand_num, param, "mul")

    return jsonify({
        "random": rand_num,
        "param": param,
        "operation": "mul",
        "result": result
    })

# 2) POST
@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()
    if not data or "jsonParam" not in data:
        return jsonify({"error": "JSON должен содержать поле jsonParam"}), 400

    try:
        json_param = float(data["jsonParam"])
    except (TypeError, ValueError):
        return jsonify({"error": "jsonParam должен быть числом"}), 400

    rand_num = random.randint(1, 10)
    operation = get_random_operation()
    result = apply_operation(rand_num, json_param, operation)

    # если div на 0
    if result is None and operation == "div":
        return jsonify({
            "random": rand_num,
            "jsonParam": json_param,
            "operation": operation,
            "error": "деление на ноль невозможно"
        }), 400

    return jsonify({
        "random": rand_num,
        "jsonParam": json_param,
        "operation": operation,
        "result": result
    })

# 3) DELETE
@app.route('/number/', methods=['DELETE'])
def delete_number():
    rand_num = random.randint(1, 10)
    operation = get_random_operation()

    return jsonify({
        "random": rand_num,
        "operation": operation
    })





import requests

BASE_URL = "http://127.0.0.1:5000/number/"

def run_requests():
    # GET
    param = random.randint(1, 10)
    get_resp = requests.get(BASE_URL, params={"param": param}).json()

    # сохраняем число и операцию
    get_number = get_resp["random"]
    get_operation = get_resp["operation"]

    print("GET:", get_resp)

    # POST
    json_param = random.randint(1, 10)
    post_resp = requests.post(
        BASE_URL,
        json={"jsonParam": json_param},
    ).json()

    post_number = post_resp["random"]
    post_operation = post_resp["operation"]

    print("POST:", post_resp)

    # DELETE
    delete_resp = requests.delete(BASE_URL).json()

    delete_number = delete_resp["random"]
    delete_operation = delete_resp["operation"]

    print("DELETE:", delete_resp)

    # Составляем выражение и вычисляем результат
    result = get_number

    # GET операция между GET и POST
    result = apply_operation(result, post_number, get_operation)

    # POST операция между результатом и DELETE
    result = apply_operation(result, delete_number, post_operation)

    result = int(result)

    print("\nПример:")
    print(f"{get_number} {get_operation} {post_number} {post_operation} {delete_number}")
    print("Не использовалось:", delete_operation)
    print("Результат:", result)

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        # запуск клиентской части
        run_requests()
    else:
        # запуск сервера
        app.run(debug=True)