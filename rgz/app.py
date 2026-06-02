from datetime import datetime

import requests
from flask import Flask, request, jsonify, render_template
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Подключение БД
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@127.0.0.1:5432/dsa_rgz"

# Внешний сервис курса валют
RATE_SERVICE_URL = "http://127.0.0.1:5001/rate"

db = SQLAlchemy(app)

# Инициализаця flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# Модель для работы с пользователями
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Модель для работы с категориями
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

# Модель для работы с операциями
class Operation(db.Model):
    __tablename__ = "operations"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sum = db.Column(db.Numeric(12, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type_operation = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

# Получение данных о пользователе
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Если пользователь не авторизован
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Пользователь не авторизован"}), 401

# Регистрация через JSON-запрос
@app.route("/reg", methods=["POST"])
def reg():
    try:
        data = request.get_json()

        name = data.get("name")
        password = data.get("password")

        check_user = User.query.filter_by(name=name).first()

        if check_user:
            return jsonify({"error": "Пользователь уже зарегистрирован"}), 500

        new_user = User(name=name)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Пользователь зарегистрирован"}), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ошибка при регистрации"}), 500

# Авторизация через JSON-запрос
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        name = data.get("name")
        password = data.get("password")

        user = User.query.filter_by(name=name).first()

        if not user:
            return jsonify({"error": "Пользователь с таким логином не найден"}), 401

        if not user.check_password(password):
            return jsonify({"error": "Неверный пароль"}), 401

        login_user(user)
        return jsonify({"message": "Пользователь авторизован"}), 200

    except Exception:
        return jsonify({"error": "Ошибка при авторизации"}), 500

# Страница добавления категории
@app.route("/add_category", methods=["GET"])
@login_required
def add_category_page():
    return render_template("add_category.html")

# Сохранение категории
@app.route("/add_category", methods=["POST"])
@login_required
def add_category():
    try:
        name = request.form.get("name")

        if not name:
            return render_template(
                "add_category.html",
                error="Введите название категории"
            )

        new_category = Category(
            name=name,
            user_id=current_user.id
        )

        db.session.add(new_category)
        db.session.commit()

        return render_template(
            "add_category.html",
            message="Категория добавлена"
        )

    except Exception:
        db.session.rollback()
        return render_template(
            "add_category.html",
            error="Ошибка при добавлении категории"
        )

# Страница добавления операции
@app.route("/add_operation", methods=["GET"])
@login_required
def add_operation_page():
    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "add_operation.html",
        categories=categories
    )

# Добавление новой операции
@app.route("/add_operation", methods=["POST"])
@login_required
def add_operation():
    try:
        type_operation = request.form.get("type_operation")
        operation_sum = request.form.get("sum")
        operation_date = request.form.get("date")
        category_id = request.form.get("category_id")

        category = Category.query.filter_by(
            id=category_id,
            user_id=current_user.id
        ).first()

        if not category:
            categories = Category.query.filter_by(user_id=current_user.id).all()

            return render_template(
                "add_operation.html",
                categories=categories,
                error="Выбранная категория не найдена"
            )

        if type_operation not in ["расход", "доход"]:
            categories = Category.query.filter_by(user_id=current_user.id).all()

            return render_template(
                "add_operation.html",
                categories=categories,
                error="Некорректный тип операции"
            )

        operation_date = datetime.strptime(operation_date, "%Y-%m-%d").date()

        new_operation = Operation(
            date=operation_date,
            sum=operation_sum,
            user_id=current_user.id,
            type_operation=type_operation,
            category_id=category.id
        )

        db.session.add(new_operation)
        db.session.commit()

        categories = Category.query.filter_by(user_id=current_user.id).all()

        return render_template(
            "add_operation.html",
            categories=categories,
            message="Операция добавлена"
        )

    except Exception:
        db.session.rollback()

        categories = Category.query.filter_by(user_id=current_user.id).all()

        return render_template(
            "add_operation.html",
            categories=categories,
            error="Ошибка при добавлении операции"
        )

# Просмотр операций пользователя
@app.route("/operations", methods=["GET"])
@login_required
def operations():
    try:
        currency = request.args.get("currency")

        if currency not in ["RUB", "EUR", "USD"]:
            return jsonify({"error": "Некорректная валюта"}), 500

        rate = 1

        if currency in ["EUR", "USD"]:
            response = requests.get(
                RATE_SERVICE_URL,
                params={"currency": currency},
            )

            if response.status_code != 200:
                return jsonify({"error": "Ошибка получения курса валюты"}), 500

            rate = response.json().get("rate")

        user_operations = Operation.query.filter_by(user_id=current_user.id).all()

        result = []

        for operation in user_operations:
            converted_sum = float(operation.sum) / rate

            category = Category.query.get(operation.category_id)

            result.append({
                "id": operation.id,
                "date": operation.date.strftime("%Y-%m-%d"),
                "type_operation": operation.type_operation,
                "sum": round(converted_sum, 2),
                "currency": currency,
                "category": category.name
            })

        return jsonify({"operations": result}), 200

    except Exception:
        return jsonify({"error": "Ошибка при получении операций"}), 500

# Выход
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Пользователь вышел из системы"}), 200

if __name__ == "__main__":
    app.run(debug=True)