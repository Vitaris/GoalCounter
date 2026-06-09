# Example using PIO to drive a set of WS2812 LEDs.

import time
from array import array
from machine import Pin
import rp2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812_asm():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class ws2812:
    
    def __init__(self, 
                 num_leds: int,
                 pin_num: int,
                 brightness: float = 1.0):
        self.num_leds: int = num_leds
        self.brightness: float = brightness
        self.sm: rp2.StateMachine = rp2.StateMachine(0, ws2812_asm, freq=8_000_000, sideset_base=Pin(pin_num, Pin.PULL_DOWN))
        self.ar: array = array("I", [0 for _ in range(self.num_leds)])
        # Pre-allocate the array to avoid creating it every time pixels_show is called
        self.output_ar: array = array("I", [0 for _ in range(self.num_leds)])
        self.sm.active(1)

    @micropython.viper
    def _pixels_show_viper(self, bri: int, colors_ar: object):
        src_ptr = ptr32(colors_ar) 
        dest_ptr = ptr32(self.output_ar)
        n = int(self.num_leds)
        
        for i in range(n):
            c = src_ptr[i]
            
            r = ((c >> 8) & 0xFF) * bri >> 8
            g = ((c >> 16) & 0xFF) * bri >> 8
            b = (c & 0xFF) * bri >> 8
            
            dest_ptr[i] = (g << 16) | (r << 8) | b

    def pixels_show(self, colors: array):
        brightness: int = int(self.brightness * 256)
        self._pixels_show_viper(brightness, colors)
        self.sm.put(self.output_ar, 8)
