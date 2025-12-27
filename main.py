import random
import micropython
from machine import Pin, Timer
from time import ticks_ms, ticks_diff
from button import Button
from matrix_8x8 import matrix_8x8
from graphics import COLORS_LIST, square

# Allocate buffer for interrupt exceptions just in case
micropython.alloc_emergency_exception_buf(100)

# Flag to trigger the main loop
frame_tick = False

def on_timer(t):
    global frame_tick
    frame_tick = True

def button_callback_01():
    global speed
    if speed < 0.2: speed += 0.001

def button_callback_02():
    global speed
    if speed > 0.0: speed -= 0.001
    if speed < 0.0: speed = 0.0

def button_hold_callback():
    pass

if __name__ == "__main__":
    matrix = matrix_8x8(28, 2, brightness=0.01)

    # Simple button setup
    btn_inc = Button(1, button_callback_01, button_hold_callback)
    btn_dec = Button(14, button_callback_02, button_hold_callback)

    # Setup Timer for 50 FPS (20ms interval)
    # The timer simply sets a flag, keeping the interrupt very short
    timer = Timer(-1)
    timer.init(period=20, mode=Timer.PERIODIC, callback=on_timer)

    # Pulse strat value to top brightness and back down to 0
    # If it strats from 50% brightness to 0%, its distance = 1.5

    # Time for 110 BPM: 60/110 = 0.545s per beat
    # Frames per beat: 0.545s / 0.02s (50FPS) = 27.27 frames
 
    # Formula: speed = distance / frames = 1.5 / 27.27 = ~0.055
    global speed
    speed = 0.055

    brightness = 0
    dimm = 1.0
    direction = 1 # 1 = increasing, -1 = decreasing
    color_0 = random.choice(COLORS_LIST) # type: ignore
    color_1 = random.choice(COLORS_LIST) # type: ignore

    i = 0
    start_time = ticks_ms()
    
    while True:
        # Wait for the timer interrupt to set the flag
        if frame_tick:
            frame_tick = False
            
            # --- Start of Frame Logic ---
            
            # 1. Poll buttons
            Button.update_all()
 
            # 2. Animation Logic
            brightness += speed * direction
            if brightness < 0:
                brightness = 0.5
                if speed < 0.02:
                    brightness = 0.0
                direction = 1
                color_0 = random.choice(COLORS_LIST) # type: ignore
                color_1 = random.choice(COLORS_LIST) # type: ignore
            elif brightness > 1:
                brightness = 1
                direction = -1

            matrix.change_brightness(brightness * dimm)
            # 3. Render
            # This happens immediately after the tick, so we have ~10ms before the next one
            matrix.show_symbol(square, color=color_0, show=False, )
            matrix.show_symbol(square, color=color_1, offset=1, show=True)

