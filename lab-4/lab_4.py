from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, logout_user, current_user, login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def is_valid_email(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Загрузка юзера
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Главная страница
@app.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template('index.html', name=current_user.name)


# Логин (GET + POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_valid_email(email):
            return render_template('login.html', error='Некорректный email')

        # проверка пустых полей
        if not email or not password:
            return render_template('login.html', error='Все поля обязательны')

        user = User.query.filter_by(email=email).first()

        # пользователь не найден
        if not user:
            return render_template('login.html', error='Пользователь не найден')

        # неверный пароль
        if not user.check_password(password):
            return render_template('login.html', error='Неверный пароль')

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')


# Вход (GET + POST)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # проверка пустых полей
        if not name or not email or not password:
            return render_template('signup.html', error='Все поля обязательны')
        
        if not is_valid_email(email):
            return render_template('signup.html', error='Некорректный email')

        # проверка существования пользователя
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Пользователь уже существует')

        # создание пользователя
        new_user = User(email=email, name=name)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


# Выход
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # создаем таблицы в контексте приложения
    with app.app_context():
        db.create_all()
    # запускаем сервер
    app.run(debug=True)