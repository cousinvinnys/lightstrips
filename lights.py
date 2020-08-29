#!/usr/bin/env python3
import board
from neopixel import NeoPixel
import neopixel
from time import sleep
from random import randint
import colorsys
from job import Job
from effects import *

STRIP_LENGTH = 300
pixels = NeoPixel(board.D18, STRIP_LENGTH, auto_write=False)


def write_line(data):
    global pixels
    
    for i in range(len(pixels)):
        pixels[i] = data[i % len(data)]
    pixels.show()

if __name__ == '__main__':
    jobs = []
    jobs.append(Job(rainbow_breathe, name='Rainbow Breathe'))
    current_job = None
    while True:
        if len(jobs) > 0:
            # Sort by job nice values, smallest to largest
            jobs.sort(key=lambda x: x.nice)
            current_job = jobs[0]
        else:
            # Default job is off
            write_line(STRIP_LENGTH * [(0, 0, 0)])
        
        # Check if current job is running, if not, start it
        if not current_job.is_running():
            print(f'Started job: {current_job.name}')
            print('Started job: ' + str(current_job.name))
            current_job.start()
        
        # Get/render next line of current job
        next_line = current_job.get_next_line()
        if next_line is not None:
            write_line(next_line)
        # Kill/remove the job if past ttl
        else:
            print(f'Removed job: {current_job.name}')
            jobs.pop(0)
