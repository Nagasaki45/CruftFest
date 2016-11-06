#!/usr/bin/env python3

_HELP_TEXT = ('Analyse the arduino serial output to find the audio cassette '
              'wheel spead. Send it to target over OSC.')

import argparse
import glob

import numpy as np
import serial  # pySerial
from pythonosc import udp_client

SERIAL_PORT = '/dev/ttyACM*'
SERIAL_BAUD_RATE = 9600
OSC_MONITOR_PORT = 5005
OSC_TARGET_PORT = 5006
BUFFER_SIZE = 128
PEAK_STABILITY = 0.98
SPECTRAL_THRESHOLD = 30  # Got this from printing spectrum.max() and trying


def connect_serial_port():
    """Tries to connect to ports. Return the one that connects."""
    port = glob.glob(SERIAL_PORT)[0]
    print("Connecting to {}".format(port))
    return serial.Serial(port, SERIAL_BAUD_RATE)


def update_buffer(buffer, new_value):
    """Roll the buffer to the left and set the new value in it's end."""
    new_buffer = np.roll(buffer, -1)
    new_buffer[-1] = new_value
    return new_buffer


def calculate_spectrum(buffer):
    full_size = len(buffer)
    half_size = int(full_size / 2)
    return abs(np.fft.fft(buffer).real[:half_size]) / np.sqrt(full_size)


def find_peak(spectrum):
    """Returns the bin of the spectral peak and ignores noisy data."""
    if spectrum.max() < SPECTRAL_THRESHOLD:
        return 0
    else:
        return spectrum.argmax()


def update_peak(peak, spectrum):
    """Returns smoothly changed peak."""
    new_peak = find_peak(spectrum)
    return PEAK_STABILITY * peak + (1 - PEAK_STABILITY) * new_peak


def parse_arguments():
    parser = argparse.ArgumentParser(description=_HELP_TEXT)
    parser.add_argument('-m', '--monitor', action='store_true',
                        help='send OSC data to monitor app.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    osc_monitor = udp_client.SimpleUDPClient('localhost', OSC_MONITOR_PORT)
    osc_target = udp_client.SimpleUDPClient('localhost', OSC_TARGET_PORT)
    port = connect_serial_port()
    buffer = np.zeros(BUFFER_SIZE, dtype=float)
    peak = 0
    while True:
        new_value = port.readline().strip()
        try:
            new_value = float(new_value)
        except ValueError:
            # There is a chance for broken messages in the serial communication.
            # In this case just skip the message.
            continue
        buffer = update_buffer(buffer, new_value)
        spectrum = calculate_spectrum(buffer)
        spectrum[0] = 0  # Drop the DC
        peak = update_peak(peak, spectrum)

        if args.monitor:
            osc_monitor.send_message('/buffer', map(buffer, float))
            osc_monitor.send_message('/spectrum', map(spectrum, float))
            osc_monitor.send_message('/peak', float(peak))

        osc_target.send_message('/speed', float(peak))


if __name__ == '__main__':
    main()
