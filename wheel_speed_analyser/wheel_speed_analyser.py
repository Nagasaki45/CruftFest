import glob

import numpy as np
import serial  # pySerial
from pythonosc import udp_client, osc_message_builder

SERIAL_PORT = '/dev/ttyACM*'
SERIAL_BAUD_RATE = 9600
OSC_PORT = 5005
BUFFER_SIZE = 128
PEAK_STABILITY = 0.98
SPECTRAL_THRESHOLD = 30  # Got this from printing spectrum.max() and trying

osc_client = udp_client.UDPClient('localhost', OSC_PORT)


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


def send_osc_message(buffer, address):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    for value in buffer:
        msg.add_arg(float(value))
    msg = msg.build()
    osc_client.send(msg)


def main():
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
        peak = PEAK_STABILITY * peak + (1 - PEAK_STABILITY) * find_peak(spectrum)

        # Monitor results with OSC
        send_osc_message(buffer, '/buffer')
        send_osc_message(spectrum, '/spectrum')
        send_osc_message([peak], '/peak')


if __name__ == '__main__':
    main()
