from collections import namedtuple
import requests

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

Message = namedtuple('Message', 'text tag')
messages = []

api_address1 = 'http://api.openweathermap.org/data/2.5/weather?q='
api_address2 = '&appid=4e34d2a32527511de3aed7f59e036302'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['city']
    url = f'{api_address1}{text}{api_address2}'
    json_data = requests.get(url).json()
    try:
        weather = ''
        weather += 'overall is ' + json_data['weather'][0]['description']
        main_weather = json_data['weather'][0]['main']
        if main_weather == 'Rain' or main_weather == 'Thunderstorm' or main_weather == 'Storm':
            weather += ', definitely need to take an umbrella or raincoat'
        elif main_weather == 'Clear':
            weather += ', take your good mood with you :)'
        elif main_weather == 'Clouds':
            weather += ', maybe it will rain, whether you would to take an umbrella?'
        else:
            weather += ', I do not even know what you should wear, sorry.'
    except Exception:
        text = f'Вы ввели: {text}. '
        weather = f'Не могу найти данные :( Проверьте их правильность, пожалуйста'

    messages.clear()
    messages.append(Message(text, weather))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
