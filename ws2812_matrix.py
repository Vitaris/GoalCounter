from machine import Pin
from array import array
from ws2812 import ws2812
from graphics import *


class ws2812_matrix:
    """
    A class to manage a matrix of WS2812 LEDs, providing methods to show pixels, symbols, numbers, and a chess board.
    The matrix is assumed to be wired in a zig-zag pattern, and the class handles the translation from 2D coordinates to the correct LED index.
    """
    def __init__(self,
                 pin_num: int,
                 matrix_size: int = 8,
                 matrixes_count: int = 1,
                 brightness: float = 1.0):
        self.ws2812: ws2812 = ws2812((matrix_size ** 2) * matrixes_count, pin_num, brightness)

    def matrix_show(self, colors: array):
        self.ws2812.pixels_show(colors)

    def change_brightness(self, brightness: float):
        self.ws2812.brightness = brightness

    def increase_brightness(self, step: float = 0.1):
        self.ws2812.brightness = min(1.0, self.ws2812.brightness + step)

    def decrease_brightness(self, step: float = 0.1):
        self.ws2812.brightness = max(0.0, self.ws2812.brightness - step)

    def _translate_4x8_to_led(self, frame_buffer: array) -> array:
        return array("I", [
            frame_buffer[31], frame_buffer[27], frame_buffer[23], frame_buffer[19], frame_buffer[15], frame_buffer[11], frame_buffer[ 7], frame_buffer[ 3],
            frame_buffer[ 2], frame_buffer[ 6], frame_buffer[10], frame_buffer[14], frame_buffer[18], frame_buffer[22], frame_buffer[26], frame_buffer[30],
            frame_buffer[29], frame_buffer[25], frame_buffer[21], frame_buffer[17], frame_buffer[13], frame_buffer[ 9], frame_buffer[ 5], frame_buffer[ 1],
            frame_buffer[ 0], frame_buffer[ 4], frame_buffer[ 8], frame_buffer[12], frame_buffer[16], frame_buffer[20], frame_buffer[24], frame_buffer[28]
        ])

    def _translate_8x8_to_led(self, frame_buffer: array) -> array:
        return array("I", [
            frame_buffer[63], frame_buffer[55], frame_buffer[47], frame_buffer[39], frame_buffer[31], frame_buffer[23], frame_buffer[15], frame_buffer[ 7],
            frame_buffer[ 6], frame_buffer[14], frame_buffer[22], frame_buffer[30], frame_buffer[38], frame_buffer[46], frame_buffer[54], frame_buffer[62],
            frame_buffer[61], frame_buffer[53], frame_buffer[45], frame_buffer[37], frame_buffer[29], frame_buffer[21], frame_buffer[13], frame_buffer[ 5],
            frame_buffer[ 4], frame_buffer[12], frame_buffer[20], frame_buffer[28], frame_buffer[36], frame_buffer[44], frame_buffer[52], frame_buffer[60],
            frame_buffer[59], frame_buffer[51], frame_buffer[43], frame_buffer[35], frame_buffer[27], frame_buffer[19], frame_buffer[11], frame_buffer[ 3],
            frame_buffer[ 2], frame_buffer[10], frame_buffer[18], frame_buffer[26], frame_buffer[34], frame_buffer[42], frame_buffer[50], frame_buffer[58],
            frame_buffer[57], frame_buffer[49], frame_buffer[41], frame_buffer[33], frame_buffer[25], frame_buffer[17], frame_buffer[ 9], frame_buffer[ 1],
            frame_buffer[ 0], frame_buffer[ 8], frame_buffer[16], frame_buffer[24], frame_buffer[32], frame_buffer[40], frame_buffer[48], frame_buffer[56]
        ])

    def _translate_16x16_to_led(self, frame_buffer: array) -> array:
        """
        Translates a 16x16 symbol array (row-major, 16 cols) into LED order matching zig-zag wiring.
        LED col 0 = physical col 0, top-to-bottom. LED col 1 = physical col 1, bottom-to-top. Etc.
        """
        return array("I", [
            frame_buffer[  0], frame_buffer[ 16], frame_buffer[ 32], frame_buffer[ 48], frame_buffer[ 64], frame_buffer[ 80], frame_buffer[ 96], frame_buffer[112], frame_buffer[128], frame_buffer[144], frame_buffer[160], frame_buffer[176], frame_buffer[192], frame_buffer[208], frame_buffer[224], frame_buffer[240],
            frame_buffer[241], frame_buffer[225], frame_buffer[209], frame_buffer[193], frame_buffer[177], frame_buffer[161], frame_buffer[145], frame_buffer[129], frame_buffer[113], frame_buffer[ 97], frame_buffer[ 81], frame_buffer[ 65], frame_buffer[ 49], frame_buffer[ 33], frame_buffer[ 17], frame_buffer[  1],
            frame_buffer[  2], frame_buffer[ 18], frame_buffer[ 34], frame_buffer[ 50], frame_buffer[ 66], frame_buffer[ 82], frame_buffer[ 98], frame_buffer[114], frame_buffer[130], frame_buffer[146], frame_buffer[162], frame_buffer[178], frame_buffer[194], frame_buffer[210], frame_buffer[226], frame_buffer[242],
            frame_buffer[243], frame_buffer[227], frame_buffer[211], frame_buffer[195], frame_buffer[179], frame_buffer[163], frame_buffer[147], frame_buffer[131], frame_buffer[115], frame_buffer[ 99], frame_buffer[ 83], frame_buffer[ 67], frame_buffer[ 51], frame_buffer[ 35], frame_buffer[ 19], frame_buffer[  3],
            frame_buffer[  4], frame_buffer[ 20], frame_buffer[ 36], frame_buffer[ 52], frame_buffer[ 68], frame_buffer[ 84], frame_buffer[100], frame_buffer[116], frame_buffer[132], frame_buffer[148], frame_buffer[164], frame_buffer[180], frame_buffer[196], frame_buffer[212], frame_buffer[228], frame_buffer[244],
            frame_buffer[245], frame_buffer[229], frame_buffer[213], frame_buffer[197], frame_buffer[181], frame_buffer[165], frame_buffer[149], frame_buffer[133], frame_buffer[117], frame_buffer[101], frame_buffer[ 85], frame_buffer[ 69], frame_buffer[ 53], frame_buffer[ 37], frame_buffer[ 21], frame_buffer[  5],
            frame_buffer[  6], frame_buffer[ 22], frame_buffer[ 38], frame_buffer[ 54], frame_buffer[ 70], frame_buffer[ 86], frame_buffer[102], frame_buffer[118], frame_buffer[134], frame_buffer[150], frame_buffer[166], frame_buffer[182], frame_buffer[198], frame_buffer[214], frame_buffer[230], frame_buffer[246],
            frame_buffer[247], frame_buffer[231], frame_buffer[215], frame_buffer[199], frame_buffer[183], frame_buffer[167], frame_buffer[151], frame_buffer[135], frame_buffer[119], frame_buffer[103], frame_buffer[ 87], frame_buffer[ 71], frame_buffer[ 55], frame_buffer[ 39], frame_buffer[ 23], frame_buffer[  7],
            frame_buffer[  8], frame_buffer[ 24], frame_buffer[ 40], frame_buffer[ 56], frame_buffer[ 72], frame_buffer[ 88], frame_buffer[104], frame_buffer[120], frame_buffer[136], frame_buffer[152], frame_buffer[168], frame_buffer[184], frame_buffer[200], frame_buffer[216], frame_buffer[232], frame_buffer[248],
            frame_buffer[249], frame_buffer[233], frame_buffer[217], frame_buffer[201], frame_buffer[185], frame_buffer[169], frame_buffer[153], frame_buffer[137], frame_buffer[121], frame_buffer[105], frame_buffer[ 89], frame_buffer[ 73], frame_buffer[ 57], frame_buffer[ 41], frame_buffer[ 25], frame_buffer[  9],
            frame_buffer[ 10], frame_buffer[ 26], frame_buffer[ 42], frame_buffer[ 58], frame_buffer[ 74], frame_buffer[ 90], frame_buffer[106], frame_buffer[122], frame_buffer[138], frame_buffer[154], frame_buffer[170], frame_buffer[186], frame_buffer[202], frame_buffer[218], frame_buffer[234], frame_buffer[250],
            frame_buffer[251], frame_buffer[235], frame_buffer[219], frame_buffer[203], frame_buffer[187], frame_buffer[171], frame_buffer[155], frame_buffer[139], frame_buffer[123], frame_buffer[107], frame_buffer[ 91], frame_buffer[ 75], frame_buffer[ 59], frame_buffer[ 43], frame_buffer[ 27], frame_buffer[ 11],
            frame_buffer[ 12], frame_buffer[ 28], frame_buffer[ 44], frame_buffer[ 60], frame_buffer[ 76], frame_buffer[ 92], frame_buffer[108], frame_buffer[124], frame_buffer[140], frame_buffer[156], frame_buffer[172], frame_buffer[188], frame_buffer[204], frame_buffer[220], frame_buffer[236], frame_buffer[252],
            frame_buffer[253], frame_buffer[237], frame_buffer[221], frame_buffer[205], frame_buffer[189], frame_buffer[173], frame_buffer[157], frame_buffer[141], frame_buffer[125], frame_buffer[109], frame_buffer[ 93], frame_buffer[ 77], frame_buffer[ 61], frame_buffer[ 45], frame_buffer[ 29], frame_buffer[ 13],
            frame_buffer[ 14], frame_buffer[ 30], frame_buffer[ 46], frame_buffer[ 62], frame_buffer[ 78], frame_buffer[ 94], frame_buffer[110], frame_buffer[126], frame_buffer[142], frame_buffer[158], frame_buffer[174], frame_buffer[190], frame_buffer[206], frame_buffer[222], frame_buffer[238], frame_buffer[254],
            frame_buffer[255], frame_buffer[239], frame_buffer[223], frame_buffer[207], frame_buffer[191], frame_buffer[175], frame_buffer[159], frame_buffer[143], frame_buffer[127], frame_buffer[111], frame_buffer[ 95], frame_buffer[ 79], frame_buffer[ 63], frame_buffer[ 47], frame_buffer[ 31], frame_buffer[ 15],
        ])
