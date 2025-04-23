from sense_hat import SenseHat, ACTION_PRESSED
from time import sleep
import random

def run(sense):
    sense.clear()

    # Snake state
    snake = [(2, 4), (2, 5), (2, 6)]
    direction = (0, -1)
    food = (random.randint(0, 7), random.randint(0, 7))
    while food in snake:
        food = (random.randint(0, 7), random.randint(0, 7))

    running = True

    def draw():
        sense.clear()
        for segment in snake:
            sense.set_pixel(segment[0], segment[1], (0, 255, 0))
        sense.set_pixel(food[0], food[1], (255, 0, 0))

    while running:
        # Poll joystick events
        for event in sense.stick.get_events():
            if event.action == ACTION_PRESSED:
                if event.direction == "up" and direction != (0, 1):
                    direction = (0, -1)
                elif event.direction == "down" and direction != (0, -1):
                    direction = (0, 1)
                elif event.direction == "left" and direction != (1, 0):
                    direction = (-1, 0)
                elif event.direction == "right" and direction != (-1, 0):
                    direction = (1, 0)
                elif event.direction == "middle":
                    running = False
        # Advance snake
        new_head = ((snake[0][0] + direction[0]) % 8,
                    (snake[0][1] + direction[1]) % 8)
        if new_head in snake:
            running = False
        else:
            snake.insert(0, new_head)
            if new_head == food:
                food = (random.randint(0, 7), random.randint(0, 7))
                while food in snake:
                    food = (random.randint(0, 7), random.randint(0, 7))
            else:
                snake.pop()
        draw()
        sleep(0.3)

    # Exit message back to clock
    sense.clear()
    sense.show_message("Tilbage til ur", text_colour=(0, 255, 255))