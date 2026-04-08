import time
from machine import Pin
from matrix_8x8 import matrix_8x8
from button import Button
from graphics import *
import utime
import random

# Define button press/release callback
def score_0_callback():
    global score_0
    score_0 = (score_0 + 1) % 100

def score_0_hold_callback():
    global score_0
    score_0 = (score_0 - 1) % 100

def score_1_callback():
    global score_1
    score_1 = (score_1 + 1) % 100

def score_1_hold_callback():
    global score_1
    score_1 = (score_1 - 1) % 100

if __name__ == "__main__":
    matrix = matrix_8x8(28, 2, brightness=0.2)

    score_0 = 0
    score_1 = 0

    button0 = Button(1, score_0_callback, hold_callback=score_0_hold_callback)
    button1 = Button(14, score_1_callback, hold_callback=score_1_hold_callback)
    
    while True:
        Button.update_all()
        matrix.show_number(score_0)
        matrix.show_number(score_1, offset=1)
