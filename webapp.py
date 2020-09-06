from flask import Flask, render_template, request
from inspect import getmembers, isfunction, getfullargspec
from threading import Thread
from lights import LightController
from job import Job
import effects
from effects import *

app = Flask(__name__)
lights = LightController(300, debug=True)

effects_dict = {}


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
    return f'Yup you doin\' that {effect}'


@app.route('/effects', methods=['POST', 'GET'])
def show_effects():
    global lights
    if request.method == 'POST' and 'effect' in request.form.keys():
        effect_name = request.form["effect"]

        effect_options = {}

        for key, raw_value in request.form.items():
            if key.startswith(f'{effect_name}_'):
                if effects_dict[effect_name]['options'][key[len(f'{effect_name}_'):]]['type'] == 'color':
                    value = (int(raw_value[1:3], 16), int(raw_value[3:5], 16), int(raw_value[5:7], 16))
                elif effects_dict[effect_name]['options'][key[len(f'{effect_name}_'):]]['type'] == 'float':
                    value = float(raw_value)
                elif effects_dict[effect_name]['options'][key[len(f'{effect_name}_'):]]['type'] == 'int':
                    value = int(raw_value)
                elif effects_dict[effect_name]['options'][key[len(f'{effect_name}_'):]]['type'] == 'string':
                    value = str(raw_value)
                else:
                    value = raw_value

                effect_options[key[len(f'{effect_name}_'):]] = value

        effect_priority = float(request.form['priority'])

        time_list = [float(i) for i in request.form['length'].split(':')]

        effect_length = 0

        for i, value in enumerate(time_list):
            effect_length += value * 60 ** (len(time_list) - (i + 1))

        lights.add_job(Job(effects_dict[effect_name]['generator'](300, **effect_options), nice=effect_priority, ttl=effect_length, name=effects_dict[effect_name]['name']))



    return render_template('effects.html', effects=effects_dict)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


def run_lights(lights):
    while True:
        lights.step()


if __name__ == '__main__':

    # Get all the effect functions listed in the module, excluding utility functions
    functions = [o for o in getmembers(effects) if isfunction(o[1]) and o[0][0] != '_']

    for function in functions:
        # Utility variable to make it so I don't have to type a big long mess over and over
        # Also a toxic spawnpeeker
        doc = function[1].__doc__ if function[1].__doc__ is not None else '  Args:  Yields:  '

        # Find the part of the string that describes the function
        description = doc[0:doc.find('Args:')].strip()


        effects_dict[function[0]] = {'name': function[0].replace('_', ' ').capitalize(), 'description': description, 'generator': function[1], 'options': {}}

        args = [i.strip() for i in doc[doc.find('Args:') + len('Args:') : doc.find('Yields:')].split('\n') if i.strip() != '']

        arg_name = ''
        arg_type = 'None'
        arg_description = ''
        arg_notes = {}

        # Extract the argument variables
        for arg in args:
            arg_name = arg[0:arg.find(' ')].strip()
            arg_type = arg[arg.find('(') + 1:arg.find(')')].strip()
            arg_descriptions = [i.strip() for i in arg[arg.find(':') + 1:].strip().split('$$')]
            arg_description = arg_descriptions[0]


            arg_notes = {}

            # Extract the notes about the argument
            if len(arg_descriptions) > 1:
                for note in arg_descriptions[1:]:
                    if '(' in note:
                        arg_notes[note[0:note.find('(')].strip()] = [i.strip() for i in note[note.find('(') + 1:note.find(')')].split(',')]
                    else:
                        arg_notes[note] = []

            effects_dict[function[0]]['options'][arg_name] = {'name': arg_name.replace('_', ' ').capitalize(), 'type': arg_type, 'description': arg_description, 'notes': arg_notes}

    print(effects_dict)

    light_thread = Thread(target=run_lights, args=(lights, ), daemon=True)
    light_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


