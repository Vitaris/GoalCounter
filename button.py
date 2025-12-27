from time import ticks_ms, ticks_diff
from machine import Pin
from enum import Enum

class ButtonState(Enum):
    IDLE = 0
    PRESSED = 1
    HELD = 2


class Button:
    instances = []
    last_btn_check = ticks_ms()
    DEBOUNCE_INTERVAL = 30 # milliseconds
    HOLD_INTERVAL = 3000 # milliseconds

    def __init__(self, pin, callback, hold_callback,  args=(), pull=Pin.PULL_UP, master=False):
        self.pin = Pin(pin, Pin.IN, pull)
        self.state = ButtonState.IDLE
        self.is_enabled = True
        self.time_pressed = 0
        self.is_master = master
        self.callback = callback
        self.hold_callback = hold_callback
        self.on_hold = False
        self.args = args
        self.partner = None
        self.suppressed = False
        Button.instances.append(self)

    def set_partner(self, partner):
        self.partner = partner

    def is_pressed(self):
        return not self.pin.value()

    def suppress(self):
        self.suppressed = True

    def compute(self):
        if not self.is_enabled:
            return

        match self.state:
            case ButtonState.IDLE:
                if not self.pin.value():
                    self.state = ButtonState.PRESSED
                    self.time_pressed = ticks_ms()
                    self.suppressed = False

            case ButtonState.PRESSED:
                if ticks_diff(ticks_ms(), self.time_pressed) >= self.DEBOUNCE_INTERVAL:
                    if not self.pin.value(): # still pressed
                        if ticks_diff(ticks_ms(), self.time_pressed) >= self.HOLD_INTERVAL:
                            # If suppressed (by virtual button) or partner is pressed (potential combo), don't fire hold
                            if self.suppressed:
                                pass 
                            elif self.partner and self.partner.is_pressed():
                                pass 
                            else:
                                self.state = ButtonState.HELD
                                self.hold_callback(*self.args)

                    else: # released
                        if not self.suppressed:
                            self.callback(*self.args)
                        self.state = ButtonState.IDLE
                        self.time_pressed = 0
                        self.suppressed = False
                        
            case ButtonState.HELD:
                if self.pin.value(): # released
                    self.state = ButtonState.IDLE
                    self.time_pressed = 0
                    self.suppressed = False
 

    def set_enabled(self, enabled: bool):
        self.is_enabled = enabled

    @classmethod
    def update_all(cls):
        for button in cls.instances:
            button.compute()





