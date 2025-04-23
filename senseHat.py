#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD
from time import sleep
from signal import pause
import threading
import datetime

sense = SenseHat()
sense.clear()

running = True
current_mode = "clock"
off = (0, 0, 0)

def display_binary(value, row, color):
    binary_str = f"{value:08b}"
    for x in range(8):
        sense.set_pixel(x, row, color if binary_str[x] == '1' else off)

def binary_clock_loop():
    while running:
        if current_mode == "clock":
            now = datetime.datetime.now()
            display_binary(now.year % 100, 0, (0, 255, 0))
            display_binary(now.month,      1, (0, 0, 255))
            display_binary(now.day,        2, (255, 0, 0))
            display_binary(now.hour,       3, (0, 255, 0))
            display_binary(now.minute,     4, (0, 0, 255))
            display_binary(now.second,     5, (255, 0, 0))
            display_binary(int(now.microsecond / 10000), 6, (127, 127, 0))
        sleep(0.1)

clock_thread = threading.Thread(target=binary_clock_loop)
clock_thread.start()

def show_danish_flag():
    global current_mode
    current_mode = "flag"
    R = (255, 0, 0)
    W = (255, 255, 255)
    flag = [
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        W, W, W, W, W, W, W, W,
        W, W, W, W, W, W, W, W,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R
    ]
    sense.set_pixels(flag)

def show_temperature():
    global current_mode
    current_mode = "temp"
    temp = sense.get_temperature()
    sense.show_message(f"{temp:.1f}C", text_colour=(255, 255, 0))

def show_humidity():
    global current_mode
    current_mode = "humid"
    hum = sense.get_humidity()
    sense.show_message(f"{hum:.1f}%", text_colour=(0, 255, 255))

def start_snake_game():
    global current_mode
    current_mode = "game"
    sense.clear()
    import snake_game
    snake_game.run(sense)
    current_mode = "clock"

def handle_event(event):
    global current_mode
    if event.action not in [ACTION_PRESSED, ACTION_HELD]:
        return

    if event.direction == "up":
        show_danish_flag()
    elif event.direction == "down":
        if current_mode == "flag":
            current_mode = "clock"
            sense.clear()
        else:
            show_temperature()
    elif event.direction == "left":
        show_humidity()
    elif event.direction == "right":
        start_snake_game()
    elif event.direction == "middle":
        current_mode = "clock"
        sense.clear()

sense.stick.direction_any = handle_event

try:
    pause()
except KeyboardInterrupt:
    running = False
    clock_thread.join()
    sense.clear()
#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD
from time import sleep
from signal import pause
import threading
import datetime

sense = SenseHat()
sense.clear()

running = True
current_mode = "clock"
off = (0, 0, 0)

# ==== Binary Clock Display ====
def display_binary(value, row, color):
    binary_str = f"{value:08b}"
    for x in range(8):
        sense.set_pixel(x, row, color if binary_str[x] == '1' else off)

def binary_clock_loop():
    while running:
        if current_mode == "clock":
            now = datetime.datetime.now()
            display_binary(now.year % 100, 0, (0, 255, 0))
            display_binary(now.month,      1, (0, 0, 255))
            display_binary(now.day,        2, (255, 0, 0))
            display_binary(now.hour,       3, (0, 255, 0))
            display_binary(now.minute,     4, (0, 0, 255))
            display_binary(now.second,     5, (255, 0, 0))
            display_binary(int(now.microsecond / 10000), 6, (127, 127, 0))
        sleep(0.1)

# Start clock thread
clock_thread = threading.Thread(target=binary_clock_loop)
clock_thread.start()

# ==== Danish Flag ====
def show_danish_flag():
    global current_mode
    current_mode = "flag"
    R = (255, 0, 0)
    W = (255, 255, 255)
    flag = [
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        W, W, W, W, W, W, W, W,
        W, W, W, W, W, W, W, W,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
        R, R, R, W, W, R, R, R,
    ]
    sense.set_pixels(flag)

# ==== Temperature ====
def show_temperature():
    global current_mode
    current_mode = "temp"
    temp = sense.get_temperature()
    sense.show_message(f"{temp:.1f}C", text_colour=(255, 255, 0))

# ==== Humidity ====
def show_humidity():
    global current_mode
    current_mode = "humid"
    hum = sense.get_humidity()
    sense.show_message(f"{hum:.1f}%", text_colour=(0, 255, 255))

# ==== Snake Game ====
def start_snake_game():
    global current_mode
    current_mode = "game"
    sense.clear()
    import snake_game
    snake_game.run(sense)
    current_mode = "clock"

# ==== Event-handler ====
def handle_event(event):
    global current_mode
    if event.action not in [ACTION_PRESSED, ACTION_HELD]:
        return

    if event.direction == "up":
        show_danish_flag()
    elif event.direction == "down":
        if current_mode == "flag":
            current_mode = "clock"
            sense.clear()
        else:
            show_temperature()
    elif event.direction == "left":
        show_humidity()
    elif event.direction == "right":
        start_snake_game()
    elif event.direction == "middle":
        current_mode = "clock"
        sense.clear()

sense.stick.direction_any = handle_event

# ==== Keep program running ====
try:
    pause()
except KeyboardInterrupt:
    running = False
    clock_thread.join()
    sense.clear()