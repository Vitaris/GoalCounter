# Example using PIO to drive a set of WS2812 LEDs.

import array, time
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
    
    def __init__(self, num_leds, pin_num, brightness):
        self.num_leds = num_leds
        self.brightness = brightness
        self.sm = rp2.StateMachine(0, ws2812_asm, freq=8_000_000, sideset_base=Pin(pin_num, Pin.PULL_DOWN))
        self.ar = array.array("I", [0 for _ in range(self.num_leds)])
        # Pre-allocate the array to avoid creating it every time pixels_show is called
        self.dimmer_ar = array.array("I", [0 for _ in range(self.num_leds)])
        self.sm.active(1)

    @micropython.viper
    def _pixels_show_viper(self, bri: int):
        # Viper worker: handles the heavy loop with raw pointers
        ar_ptr = ptr32(self.ar)
        dimmer_ar_ptr = ptr32(self.dimmer_ar)
        n = int(self.num_leds)
        
        for i in range(n):
            c = ar_ptr[i]
            r = ((c >> 8) & 0xFF) * bri >> 8
            g = ((c >> 16) & 0xFF) * bri >> 8
            b = (c & 0xFF) * bri >> 8
            dimmer_ar_ptr[i] = (g << 16) | (r << 8) | b

    def pixels_show(self):
        # Standard Python wrapper: handles float math and object calls
        bri = int(self.brightness * 256)
        self._pixels_show_viper(bri)
        self.sm.put(self.dimmer_ar, 8)

    def pixel_set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 