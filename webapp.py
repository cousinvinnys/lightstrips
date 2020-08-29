from flask import Flask, render_template, request
from threading import Thread
from lights import LightController
from job import Job
from effects import *

app = Flask(__name__)
lights = LightController(300, debug=True)


@app.route('/hello/<user>')
def hello_name(user):
    return render_template('hello.html', name=user)


@app.route("/gae")
def gae():
    global lights
    print("Adding a job to the queue")
    lights.add_job(Job(rainbow_wave(300), ttl=10, name="u gae lol"))
    return "You gae"


@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        return render_template("result.html", result=result)


def run_lights(lights):
    while True:
        lights.step()


if __name__ == '__main__':
    light_thread = Thread(target=run_lights, args=(lights, ), daemon=True)
    light_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


