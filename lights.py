#!/usr/bin/env python3
import board
from neopixel import NeoPixel
import neopixel
from time import sleep, perf_counter
from random import randint
import colorsys
from job import Job
from effects import *

DEBUG = True
PRINT_FRAMERATE = False
STRIP_LENGTH = 300
pixels = NeoPixel(board.D18, STRIP_LENGTH, auto_write=False)


def write_line(data):
    global pixels
    
    for i in range(len(pixels)):
        pixels[i] = data[i % len(data)]
    pixels.show()

if __name__ == '__main__':
    jobs = []
    jobs.append(Job(rainbow_breathe(0.005), ttl=5, name='Rainbow Breathe'))
    current_job = None
    while True:
        if PRINT_FRAMERATE:
            frame_start = perf_counter()
        
        if len(jobs) > 0:
            # Sort by job nice values, smallest to largest
            jobs.sort(key=lambda x: x.nice)
            current_job = jobs[0]
        else:
            # Default job is off
            if DEBUG:
                print('No jobs, shutting off')
            write_line(STRIP_LENGTH * [(0, 0, 0)])
        
        # Check if current job is running, if not, start it
        if type(current_job) == Job:
            if not current_job.is_running() and not current_job.is_dead():
                if DEBUG:
                    print(f'Started job: {current_job.name} ({current_job.time_remaining()}s remaining)')
                current_job.start()
        
            # Get/render next line of current job
            next_line = current_job.get_next_line()
            if next_line is not None:
                write_line(next_line)
            # Kill/remove the job if past ttl
            else:
                if DEBUG:
                    print(f'Removed job: {current_job.name}')
                jobs.pop(0)
                current_job = None
        
        if PRINT_FRAMERATE:
            print(f'{1 / (perf_counter() - frame_start)} fps')
