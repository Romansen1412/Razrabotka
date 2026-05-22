from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:postgres@localhost:5432/currency_db'
)
db = SQLAlchemy(app)
class Currencies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(50), unique=True, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)
    
    

@app.route('/load', methods=['POST'])
def load():
    currency_name = request.json.get('currency_name')
    currency_rate = request.json.get('currency_rate')

    try:
        currency_rate = float(currency_rate)
    except ValueError:
        return {'message': 'Курс должен быть числом'}, 400
    
    if currency_rate <= 0:
        return {'message': 'Курс должен быть положительным'}, 400
    
    # Проверка на наличие валюты в БД
    existing_currency = Currencies.query.filter_by(currency_name=currency_name).first()
    if existing_currency:
        return {'message': 'Валюта уже существует'}, 400

    # Сохранение валюты в БД
    new_currency = Currencies(currency_name=currency_name, rate=currency_rate)
    db.session.add(new_currency)
    db.session.commit()

    return {'message': 'Валюта успешно добавлена'}, 200

@app.route('/update_currency', methods=['POST'])
def update_currency():
    currency_name = request.json.get('currency_name')
    currency_rate = request.json.get('currency_rate')

    existing_currency = Currencies.query.filter_by(currency_name=currency_name).first()

    try:
        currency_rate = float(currency_rate)
    except ValueError:
        return {'message': 'Курс должен быть числом'}, 400
    
    if currency_rate <= 0:
        return {'message': 'Курс должен быть положительным'}, 400
    
    if existing_currency:
        fetch_currency = Currencies.query.filter_by(currency_name=currency_name).first()
        fetch_currency.rate = currency_rate
        db.session.commit()
        return {'message': 'Валюта успешно обновлена'}, 200

    return {'message': 'Валюта не найдена'}, 404

@app.route('/delete', methods=['POST'])
def delete():
    currency_name = request.json.get('currency_name')

    existing_currency = Currencies.query.filter_by(currency_name=currency_name).first()
    if existing_currency:
        db.session.delete(existing_currency)
        db.session.commit()
        return {'message': 'Валюта успешно удалена'}, 200

    return {'message': 'Валюта не найдена'}, 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)