#!/usr/bin/env python3

import sys
import signal
import argparse
import datetime
import time
from sense_hat import SenseHat

sense = SenseHat()
running = True

# Colors
year_color = (0, 255, 0)
month_color = (0, 0, 255)
day_color = (255, 0, 0)
hour_color = (0, 255, 0)
minute_color = (0, 0, 255)
second_color = (255, 0, 0)
hundredths_color = (127, 127, 0)
off = (0, 0, 0)

def display_binary(value, row, color):
    binary_str = f"{value:08b}"
    for x in range(8):
        sense.set_pixel(x, row, color if binary_str[x] == '1' else off)

# Signal handling
def handle_exit(signum, frame):
    global running
    running = False
    sense.clear()

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Rotation support
parser = argparse.ArgumentParser(description="Binary Clock for Sense HAT")
parser.add_argument('-r', '--rotate', type=int, default=0, help="Rotate display (0, 90, 180, 270)")
args = parser.parse_args()

if args.rotate in [0, 90, 180, 270]:
    sense.set_rotation(args.rotate)
else:
    print("kan ikke rotere med det angivet input")
    sys.exit(1)

# Main clock loop
while running:
    now = datetime.datetime.now()
    display_binary(now.year % 100, 0, year_color)
    display_binary(now.month,      1, month_color)
    display_binary(now.day,        2, day_color)
    display_binary(now.hour,       3, hour_color)
    display_binary(now.minute,     4, minute_color)
    display_binary(now.second,     5, second_color)
    display_binary(int(now.microsecond / 10000), 6, hundredths_color)
    time.sleep(0.1)

sense.clear()