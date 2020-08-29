#!/usr/bin/env python3
try:
    import board
    from neopixel import NeoPixel
    import neopixel
    print("Running lights")
except ImportError:
    from virtual_lights import VirtualBoard as board
    from virtual_lights import VirtualPixels as NeoPixel
    print("Running virtual lights")

from time import sleep, perf_counter
from random import randint
import colorsys
from job import Job
from effects import *
from threading import Lock


DEBUG = True
PRINT_FRAMERATE = False
STRIP_LENGTH = 300


class LightController:
    def __init__(self, strip_length=300, print_framerate=PRINT_FRAMERATE, debug=DEBUG, rest_state=None):
        self.strip_length = strip_length
        self.print_framerate = print_framerate
        self.debug = debug
        self.pixels = NeoPixel(board.D18, self.strip_length, auto_write=False)

        self.current_job = None

        self.rest_state = rest_state if rest_state is not None else [(0, 0, 0)] * self.strip_length

        # Create the array of jobs
        self.jobs = []

        self._job_lock = Lock()

    def _write_line(self, data):
        for i in range(len(self.pixels)):
            self.pixels[i] = data[i % len(data)]
        self.pixels.show()

    def add_job(self, job):
        with self._job_lock:
            self.jobs.append(job)

            # Sort by job nice values, smallest to largest
            self.jobs.sort(key=lambda x: x.nice)

    def clear_jobs(self):
        with self._job_lock:
            self.jobs.clear()

    def step(self):
        if self.print_framerate:
            frame_start = perf_counter()

        # Get the current most important job
        with self._job_lock:
            if len(self.jobs) > 0:
                self.current_job = self.jobs[0]

            # If there is no job, set the strip to its rest state
            else:
                self._write_line(self.rest_state)

            if type(self.current_job) == Job:

                # If the current job hasn't been started, start it
                if not self.current_job.is_running() and not self.current_job.is_dead():
                    self.current_job.start()
                    if self.debug:
                        print(f'Started job: {self.current_job.name} ({round(self.current_job.time_remaining(), 3)}s remaining)')

                # Get the next line fromt he job generator and push it to the strip
                next_line = self.current_job.get_next_line()
                if next_line is not None:
                    self._write_line(next_line)

                # If the job has expired, kill it and remove it from the the list
                else:
                    if self.debug:
                        print(f'Removed job: {self.current_job.name}')
                    self.jobs.pop(0)
                    self.current_job = None

        if self.print_framerate:
            print(f'{round(1 / (perf_counter() - frame_start), 2)} fps')


if __name__ == '__main__':
    lights = LightController(300, debug=True)
    lights.add_job(Job(rainbow_wave(300, -0.01), ttl=5, name='Rainbow Wave'))
    lights.add_job(Job(rainbow_breathe(300, -0.01), ttl=5, name='Rainbow Breathe'))
    lights.add_job(Job(rainbow_wave(300, 0.01), ttl=5, name='Rainbow Wave 2'))
    lights.add_job(Job(breathe_color(300, color1=(0, 255, 127), speed=0.1), ttl=10, name='Breath to black'))
    lights.add_job(Job(breathe_color(300, color1=(255, 0, 0), color2=(0, 255, 0), speed=0.1), ttl=10, name='Colour Breath'))
    lights.add_job(Job(solid_color(300, (255, 0, 255)), ttl=2, name='Solid Pink'))
    lights.add_job(Job(solid_color(300, (69, 17, 125)), ttl=2, name='Solid Periwinkle'))

    while True:
        lights.step()
