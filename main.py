import time
from machine import Pin, Timer
from matrix_8x8 import matrix_8x8
from graphics import *
import random
import micropython

# Allocate buffer for interrupt exceptions just in case
micropython.alloc_emergency_exception_buf(100)

# Flag to trigger the main loop
frame_tick = False

def on_timer(t):
    global frame_tick
    frame_tick = True

if __name__ == "__main__":
    matrix = matrix_8x8(28, 2, brightness=0.01)

    # Simple button setup
    btn_inc = Pin(1, Pin.IN, Pin.PULL_UP)
    btn_dec = Pin(14, Pin.IN, Pin.PULL_UP)

    # Setup Timer for 50 FPS (20ms interval)
    # The timer simply sets a flag, keeping the interrupt very short
    timer = Timer(-1)
    timer.init(period=20, mode=Timer.PERIODIC, callback=on_timer)

    speed = 0.05
    k = 0
    direction = 18
    color_0 = GREEN
    color_1 = RED
    symbol = random.choice(symbols_list)
    number = random.randint(0, 99)

    i = 0
    start_time = time.ticks_ms()
    last_btn_check = 0
    
    while True:
        # Wait for the timer interrupt to set the flag
        if frame_tick:
            frame_tick = False
            
            # --- Start of Frame Logic ---
            
            # 1. Poll buttons
            now = time.ticks_ms()
            if time.ticks_diff(now, last_btn_check) > 50:
                if not btn_inc.value():
                    if speed < 1: speed += 0.01
                    print(f"Speed increased: {speed:.2f}")
                if not btn_dec.value():
                    if speed > 0.02: speed -= 0.01
                    print(f"Speed decreased: {speed:.2f}")
                last_btn_check = now

            # 2. Animation Logic
            k += speed * direction
            if k < 0:
                k = 0
                direction = 1
                color_0 = random.choice(color_list)
                color_1 = random.choice(color_list)
                symbol = random.choice(symbols_list)
                number = random.randint(0, 99)
            elif k > 10:
                k = 10
                direction = -1

            matrix.change_brightness(k * 0.01)

            # 3. Render
            # This happens immediately after the tick, so we have ~10ms before the next one
            matrix.show_symbol(symbol, color=color_0, show=False)
            matrix.show_number(number, color=color_1, offset=1, show=True)
            
            # 4. FPS Counter
            i += 1
            if time.ticks_diff(now, start_time) >= 1000:
                print(f"Speed measurement: {i} frames/sec")
                start_time = now
                i = 0
