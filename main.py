import time
from machine import Pin
from debounced_input import DebouncedInput
from matrix_8x8 import matrix_8x8
from graphics import *
import utime
import random

# Define button press/release callback
def callback0(pin, pressed, duration_ms):
    global score_0
    if (pressed):
        score_0 += 1
    if score_0 > 99:
        score_0 = 0
    matrix.show_number(score_0)

def callback1(pin, pressed, duration_ms):
    global score_1
    if (pressed):
        score_1 += 1
    if score_1 > 99:
        score_1 = 0
    matrix.show_number(score_1, offset=1)

if __name__ == "__main__":
    matrix = matrix_8x8(28, 2, brightness=0.02)
    matrix.show_number(0)
    matrix.show_number(0, offset=1)

    score_0 = 0
    score_1 = 0

    button0 = DebouncedInput(0, callback0, debounce_ms=20, pin_pull=Pin.PULL_DOWN)
    button1 = DebouncedInput(1, callback1, debounce_ms=20, pin_pull=Pin.PULL_DOWN)
    
    while True:
        time.sleep_ms(100)
    