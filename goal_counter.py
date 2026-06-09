from graphics import WHITE
from ws2812_matrix import ws2812_matrix
from graphics import *
from array import array


class GoalCounter:
    def __init__(self, background_color=BLACK):
        self.matrix = ws2812_matrix(28, 2, matrixes_count=2, brightness=0.1)
        self.background_color = background_color





        self.score_0 = 0
        self.score_1 = 0

    def show_symbol(self, symbol, offset=0, color=WHITE, backround=BLACK):
        offset *= 64
        matrix = self._translate_8x8_to_led(symbol)
        self._set_none_or_color(matrix, 0, offset, color, backround)
        self.ws2812.pixels_show()

    def show_number(self, number, offset=0, color=WHITE, backround=BLACK):
        colors = array("I", [self.background_color] * 128)

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


    def _set_none_or_color(self, matrix, i, offset, color, backround):
        lenght = len(matrix)
        for pixel in range(len(matrix)):
            if matrix[pixel] == 1:
                self.ws2812.pixel_set(pixel + (i * lenght) + offset, color)
            elif matrix[pixel] == 0:
                self.ws2812.pixel_set(pixel + (i * lenght) + offset, backround)