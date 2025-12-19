from machine import Pin
from ws2812 import ws2812
from graphics import *
import time
import micropython


class matrix_8x8:
    def __init__(self, pin_num, matrixes=1, brightness=1.0):
        self.ws2812 = ws2812(matrixes*64, pin_num, brightness)

    def fill(self, color, offset=0, show=True):
        offset *= 64
        self.ws2812.pixels_fill_range(offset, 64, color)
        if show:
            self.ws2812.pixels_show()

    def show_symbol(self, symbol, offset=0, color=WHITE, backround=BLACK):
        offset *= 64
        matrix = self._translate_8x8_to_led(symbol)
        self._set_none_or_color(matrix, 0, offset, color, backround)
        self.ws2812.pixels_show()

    def show_number(self, number, offset=0, color=WHITE, backround=BLACK):
        offset *= 64
        if number < 0 and number > 99 :
            print(f'Given number is outside range 0-99: {number}')
            return 
        
        digits = [int(x) for x in str(number)]
        digits.reverse()

        i = 0
        for digit in digits:
            matrix = self._translate_4x8_to_led(raw_digits[digit])
            self._set_none_or_color(matrix, i, offset, color, backround)
            i += 1

        if len(digits) == 1:
            matrix = self._translate_4x8_to_led(raw_blank)
            self._set_none_or_color(matrix, i, offset, color, backround)

        self.ws2812.pixels_show()

    def change_brightness(self, brightness):
        self.ws2812.brightness = brightness

    def _translate_4x8_to_led(self, symbol):
        return [
            symbol[31], symbol[27], symbol[23], symbol[19], symbol[15], symbol[11], symbol[ 7], symbol[ 3],
            symbol[ 2], symbol[ 6], symbol[10], symbol[14], symbol[18], symbol[22], symbol[26], symbol[30],
            symbol[29], symbol[25], symbol[21], symbol[17], symbol[13], symbol[ 9], symbol[ 5], symbol[ 1],
            symbol[ 0], symbol[ 4], symbol[ 8], symbol[12], symbol[16], symbol[20], symbol[24], symbol[28]
        ]
    
    def _translate_8x8_to_led(self, symbol):
        return [
            symbol[63], symbol[55], symbol[47], symbol[39], symbol[31], symbol[23], symbol[15], symbol[ 7],
            symbol[ 6], symbol[14], symbol[22], symbol[30], symbol[38], symbol[46], symbol[54], symbol[62],
            symbol[61], symbol[53], symbol[45], symbol[37], symbol[29], symbol[21], symbol[13], symbol[ 5],
            symbol[ 4], symbol[12], symbol[20], symbol[28], symbol[36], symbol[44], symbol[52], symbol[60],
            symbol[59], symbol[51], symbol[43], symbol[35], symbol[27], symbol[19], symbol[11], symbol[ 3],
            symbol[ 2], symbol[10], symbol[18], symbol[26], symbol[34], symbol[42], symbol[50], symbol[58],
            symbol[57], symbol[49], symbol[41], symbol[33], symbol[25], symbol[17], symbol[ 9], symbol[ 1],
            symbol[ 0], symbol[ 8], symbol[16], symbol[24], symbol[32], symbol[40], symbol[48], symbol[56]
        ]

    @micropython.viper
    @staticmethod
    def _set_pixels_viper(ar: ptr32, matrix: ptr8, length: int, start_idx: int, c_int: int, bg_int: int):
        # Native code loop: extremely fast, no python overhead
        for j in range(length):
            if matrix[j]:
                ar[start_idx + j] = c_int
            else:
                ar[start_idx + j] = bg_int

    def _set_none_or_color(self, matrix, i, offset, color, backround):
        # Pre-calculate colors (GRB format for WS2812)
        c_int = (color[1] << 16) | (color[0] << 8) | color[2]
        bg_int = (backround[1] << 16) | (backround[0] << 8) | backround[2]
        
        # Convert list to bytes so Viper can access it as a raw pointer
        matrix_bytes = bytes(matrix)
        length = len(matrix_bytes)
        start_idx = (i * length) + offset
        
        # Pass the raw array buffer and bytes buffer to the Viper worker
        # Changed .pixels to .ar to match the ws2812 class definition
        self._set_pixels_viper(self.ws2812.ar, matrix_bytes, length, start_idx, c_int, bg_int)