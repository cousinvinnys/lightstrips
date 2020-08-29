from flask import Flask, render_template, request
from inspect import getmembers, isfunction, getfullargspec
from threading import Thread
from lights import LightController
from job import Job
import effects
from effects import *

app = Flask(__name__)
lights = LightController(300, debug=False)


@app.route('/')
def student():
    return render_template('index.html')


@app.route('/hardCoded/<effect>')
def hard_coded(effect):
    global lights
    if effect == 'rainbowWave':
        lights.add_job(Job(rainbow_wave(), ttl=10, name=effect))
    elif effect == 'rainbowWave2':
        lights.add_job(Job(rainbow_wave(wave_speed=-0.01), ttl=10, name=effect))
    elif effect == 'rainbowBreathe':
        lights.add_job(Job(rainbow_breathe(speed=-0.01), ttl=10, name=effect))
    return f'Yup you doin that {effect}'


@app.route('/effects', methods=['POST', 'GET'])
def radio_menu():
    if request.method == 'POST':
        print(f'Got a new effect request: {dict(request.form.items())}')

    return render_template('effects.html', effects=[o[1].__name__ for o in getmembers(effects) if isfunction(o[1]) and o[1].__name__[0] != '_'])#


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


def run_lights(lights):
    while True:
        lights.step()


if __name__ == '__main__':
    light_thread = Thread(target=run_lights, args=(lights, ), daemon=True)
    light_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


