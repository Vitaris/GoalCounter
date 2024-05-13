from machine import Pin
from ws2812 import ws2812
from graphics import *


class matrix_8x8:
    def __init__(self, pin_num, matrixes=1, brightness=1.0):
        self.ws2812 = ws2812(matrixes*64, pin_num, brightness)

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

    def _set_none_or_color(self, matrix, i, offset, color, backround):
        lenght = len(matrix)
        for pixel in range(len(matrix)):
            if matrix[pixel] == 1:
                self.ws2812.pixel_set(pixel + (i * lenght) + offset, color)
            elif matrix[pixel] == 0:
                self.ws2812.pixel_set(pixel + (i * lenght) + offset, backround)