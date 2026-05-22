from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CURRENCY_MANAGER_URL = 'http://127.0.0.1:5001'
DATA_MANAGER_URL = 'http://127.0.0.1:5002'


@app.route('/')
def index():
    response = requests.get(f'{DATA_MANAGER_URL}/currencies')

    currencies = response.json().get('currencies', [])

    return render_template(
        'index.html',
        currencies=currencies,
        result=None,
        message=None
    )


@app.route('/load', methods=['POST'])
def load():
    data = {
        'currency_name': request.form.get('currency_name'),
        'currency_rate': request.form.get('currency_rate')
    }

    response = requests.post(
        f'{CURRENCY_MANAGER_URL}/load',
        json=data
    )

    answer = response.json()

    currencies_response = requests.get(
        f'{DATA_MANAGER_URL}/currencies'
    )

    currencies = currencies_response.json().get(
        'currencies',
        []
    )

    return render_template(
        'index.html',
        currencies=currencies,
        result=None,
        message=answer.get('message')
    )


@app.route('/update_currency', methods=['POST'])
def update_currency():
    data = {
        'currency_name': request.form.get('currency_name'),
        'currency_rate': request.form.get('currency_rate')
    }

    response = requests.post(
        f'{CURRENCY_MANAGER_URL}/update_currency',
        json=data
    )

    answer = response.json()

    currencies_response = requests.get(
        f'{DATA_MANAGER_URL}/currencies'
    )

    currencies = currencies_response.json().get(
        'currencies',
        []
    )

    return render_template(
        'index.html',
        currencies=currencies,
        result=None,
        message=answer.get('message')
    )


@app.route('/delete', methods=['POST'])
def delete():
    data = {
        'currency_name': request.form.get('currency_name')
    }

    response = requests.post(
        f'{CURRENCY_MANAGER_URL}/delete',
        json=data
    )

    answer = response.json()

    currencies_response = requests.get(
        f'{DATA_MANAGER_URL}/currencies'
    )

    currencies = currencies_response.json().get(
        'currencies',
        []
    )

    return render_template(
        'index.html',
        currencies=currencies,
        result=None,
        message=answer.get('message')
    )


@app.route('/convert', methods=['POST'])
def convert():
    currency_name = request.form.get('currency_name')
    convert_sum = request.form.get('convert_sum')

    response = requests.get(
        f'{DATA_MANAGER_URL}/convert',
        params={
            'currency_name': currency_name,
            'convert_sum': convert_sum
        }
    )

    result = response.json()

    currencies_response = requests.get(
        f'{DATA_MANAGER_URL}/currencies'
    )

    currencies = currencies_response.json().get(
        'currencies',
        []
    )

    return render_template(
        'index.html',
        currencies=currencies,
        result=result,
        message=result.get('message')
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)