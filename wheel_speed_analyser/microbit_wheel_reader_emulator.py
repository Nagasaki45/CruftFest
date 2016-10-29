"""
Emulates the serial output from arduino when it reads the wheels.

Use uflash to build and flash to the microbit:

    uflash --watch microbit_wheel_reader_emulator.py
"""

import random
import math

from microbit import sleep

psuedo_time = 0

while True:
    frequency_modulation = 30 * math.sin(0.005 * psuedo_time)
    value_of_interest = 70 * math.sin(.2 * psuedo_time + frequency_modulation)
    low_freq = 50 * math.sin(.01 * psuedo_time)
    noise = 100 * (random.random() - 0.5) * 0.5
    base_level = 400
    sensor_value = value_of_interest + low_freq + noise + base_level

    print(sensor_value)

    sleep(1)
    psuedo_time += 1
