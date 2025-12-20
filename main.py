import time
from machine import Pin, Timer
from matrix_8x8 import matrix_8x8
from graphics import color_list, square
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

    # Pulse strat value to top brightness and back down to 0
    # If it strats from 50% brightness to 0%, its distance = 1.5

    # Time for 110 BPM: 60/110 = 0.545s per beat
    # Frames per beat: 0.545s / 0.02s (50FPS) = 27.27 frames

    # Formula: speed = distance / frames = 1.5 / 27.27 = ~0.055
    speed = 0.055

    brightness = 0
    dimm = 1.0
    direction = 1 # 1 = increasing, -1 = decreasing
    color_0 = random.choice(color_list)
    color_1 = random.choice(color_list)

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
            if time.ticks_diff(now, last_btn_check) >= 50:
                if not btn_inc.value():
                    if speed < 0.2: speed += 0.001
                    print(f"Speed increased: {speed:.5f}")

                if not btn_dec.value():
                    if speed > 0.0: speed -= 0.001
                    if speed < 0.0: speed = 0.0
                    print(f"Speed decreased: {speed:.5f}")

                last_btn_check = now

            # 2. Animation Logic
            brightness += speed * direction
            if brightness < 0:
                brightness = 0.5
                if speed < 0.02:
                    brightness = 0.0
                direction = 1
                color_0 = random.choice(color_list)
                color_1 = random.choice(color_list)
            elif brightness > 1:
                brightness = 1
                direction = -1

            matrix.change_brightness(brightness * dimm)
            # 3. Render
            # This happens immediately after the tick, so we have ~10ms before the next one
            matrix.show_symbol(square, color=color_0, show=False, )
            matrix.show_symbol(square, color=color_1, offset=1, show=True)
            
            # 4. FPS Counter
            i += 1
            if time.ticks_diff(now, start_time) >= 1000:
                print(f"Speed measurement: {i} frames/sec")
                start_time = now
                i = 0
