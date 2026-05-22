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

@app.route('/convert', methods=['GET'])
def convert():
    currency_name = request.args.get('currency_name')
    convert_sum = request.args.get('convert_sum')
    
    try:
        convert_sum = float(convert_sum)
    except ValueError:
        return {'message': 'Сумма должна быть числом'}, 400

    if convert_sum <= 0:
        return {'message': 'Сумма должна быть положительной'}, 400
    
    if not currency_name or not convert_sum:
        return {'message': 'Недостаточно данных для конвертации'}, 400
    else:
        existing_currency = Currencies.query.filter_by(currency_name=currency_name).first()
        if existing_currency:
            converted_sum = float(convert_sum) * float(existing_currency.rate)
            return {'converted_sum': converted_sum}, 200
        else:
            return {'message': 'Валюта не найдена'}, 404

@app.route('/currencies', methods=['GET'])
def get_currencies():
    currencies = Currencies.query.all()
    currency_list = [{'name': currency.currency_name, 'rate': float(currency.rate)} for currency in currencies]
    return {'currencies': currency_list}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)