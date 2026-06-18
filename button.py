from time import ticks_ms, ticks_diff
from machine import Pin

class ButtonState:
    IDLE = 0
    PRESSED = 1
    HELD = 2


class Button:
    instances = []
    combos = []
    last_btn_check = ticks_ms()
    DEBOUNCE_INTERVAL = 30 # milliseconds
    HOLD_INTERVAL = 1000 # milliseconds

    def __init__(self, pin, callback, hold_callback=None,  args=(), pull=Pin.PULL_UP, master=False):
        self.pin = Pin(pin, Pin.IN, pull)
        self.state = ButtonState.IDLE
        self.is_enabled = True
        self.time_pressed = 0
        self.is_master = master
        self.callback = callback
        self.hold_callback = hold_callback
        self.hold_executed = False
        self.on_hold = False
        self.args = args
        Button.instances.append(self)

    def is_pressed(self):
        return not self.pin.value()

    def compute(self):
        if not self.is_enabled:
            return

        if self.state == ButtonState.IDLE:
            if not self.pin.value(): # pressed
                self.state = ButtonState.PRESSED
                self.time_pressed = ticks_ms()

        elif self.state == ButtonState.PRESSED:
            if ticks_diff(ticks_ms(), self.time_pressed) >= self.DEBOUNCE_INTERVAL:
                if not self.pin.value(): # still pressed
                    if ticks_diff(ticks_ms(), self.time_pressed) >= self.HOLD_INTERVAL:
                        self.state = ButtonState.HELD
                else: # released
                    if self.callback:
                        self.callback(*self.args)
                    self.state = ButtonState.IDLE
        elif self.state == ButtonState.HELD:
            if not self.hold_executed and self.hold_callback:
                self.hold_callback(*self.args)
                self.hold_executed = True
            if self.pin.value(): # released
                self.state = ButtonState.IDLE
                self.hold_executed = False


    def set_enabled(self, enabled: bool):
        self.is_enabled = enabled

    @classmethod
    def register_combo(cls, button_a, button_b, callback, args=()):
        cls.combos.append({'buttons': (button_a, button_b), 'callback': callback, 'args': args, 'executed': False})

    @classmethod
    def update_all(cls):
        for button in cls.instances:
            button.compute()
        for combo in cls.combos:
            a, b = combo['buttons']
            if a.state == ButtonState.HELD and b.state == ButtonState.HELD:
                if not combo['executed']:
                    combo['callback'](*combo['args'])
                    combo['executed'] = True
            else:
                combo['executed'] = False





