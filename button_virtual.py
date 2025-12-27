from button import ButtonState
from time import ticks_ms, ticks_diff
from machine import Pin
from enum import Enum


class ButtonVirtualState(Enum):
    IDLE = 0
    WAITING_FOR_BOTH_HELD = 1
    HELD = 2

class ButtonVirtual:
    instances = []
    last_btn_check = ticks_ms()
    HOLD_INTERVAL = 3000 # milliseconds

    def __init__(self, btn1, btn2, callback, args=()):
        self.btn1 = btn1
        self.btn2 = btn2
        # Link buttons so they know about each other for interlocking
        self.btn1.set_partner(self.btn2)
        self.btn2.set_partner(self.btn1)
        
        self.state = ButtonVirtualState.IDLE
        self.is_enabled = True
        self.callback = callback
        self.args = args
        self.time_pressed = 0
        ButtonVirtual.instances.append(self)

    def compute(self):
        if not self.is_enabled:
            return

        # Check if both physical buttons are currently pressed
        both_pressed = self.btn1.is_pressed() and self.btn2.is_pressed()

        match self.state:
            case ButtonVirtualState.IDLE:
                if both_pressed:
                    self.state = ButtonVirtualState.WAITING_FOR_BOTH_HELD
                    self.time_pressed = ticks_ms()

            case ButtonVirtualState.WAITING_FOR_BOTH_HELD:
                if not both_pressed:
                    self.state = ButtonVirtualState.IDLE
                elif ticks_diff(ticks_ms(), self.time_pressed) >= self.HOLD_INTERVAL:
                    # Both held for 3 seconds
                    self.callback(*self.args)
                    # Suppress individual button actions
                    self.btn1.suppress()
                    self.btn2.suppress()
                    self.state = ButtonVirtualState.HELD
                        
            case ButtonVirtualState.HELD:
                if not both_pressed: # released one or both
                    self.state = ButtonVirtualState.IDLE
                    self.time_pressed = 0
 

    def set_enabled(self, enabled: bool):
        self.is_enabled = enabled

    @classmethod
    def update_all(cls):
        for button in cls.instances:
            button.compute()





