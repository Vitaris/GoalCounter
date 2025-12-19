import time
from machine import Pin
from debounced_input import DebouncedInput
from matrix_8x8 import matrix_8x8
from graphics import *
import utime
import random

# Define button press/release callback
def callback0(pin, pressed, duration_ms):
    global speed
    if (pressed):
        if speed < 30:
            speed += 2

def callback1(pin, pressed, duration_ms):
    global speed
    if (pressed):
        if speed > 6:
            speed -= 2

if __name__ == "__main__":
    matrix = matrix_8x8(28, 2, brightness=0.01)

    speed = 0.05
    # button0 = DebouncedInput(0, callback0, debounce_ms=20, pin_pull=Pin.PULL_DOWN)
    # button1 = DebouncedInput(1, callback1, debounce_ms=20, pin_pull=Pin.PULL_DOWN)

    k = 0
    direction = 18
    color_0 = GREEN
    color_1 = RED

    i = 0

    start_time = time.ticks_ms()
    while True:
        # time.sleep_ms(100)
        k += speed * direction

        if k < 0:
            k = 0
            direction = 1
            color_0 = random.choice(color_list)
            color_1 = random.choice(color_list)
        elif k > 10:
            k = 10
            direction = -1

        matrix.change_brightness(k * 0.01)

        # Use fill instead of show_symbol(square)
        # Only show() after the last update to save time
        matrix.fill(color_0, show=False)
        matrix.fill(color_1, offset=1, show=True)
        if time.ticks_diff(time.ticks_ms(), start_time) >= 1000:
            print(f"Speed measurement: {i} frames/sec")
            start_time = time.ticks_ms()
            i = 0
        else:
            i += 1
