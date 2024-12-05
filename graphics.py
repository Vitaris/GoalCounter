# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 80, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (RED, YELLOW, ORANGE, GREEN, CYAN, BLUE, PURPLE, WHITE)
color_list = [RED, YELLOW, ORANGE, GREEN, CYAN, BLUE, PURPLE]

# Digits
raw_digits = {
    0: [0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0],

    1: [0, 0, 0, 1,
        0, 0, 1, 1,
        0, 1, 0, 1,
        0, 0, 0, 1,
        0, 0, 0, 1,
        0, 0, 0, 1,
        0, 0, 0, 1,
        0, 0, 0, 1],

    2: [0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 0, 1, 0,
        0, 1, 0, 0,
        1, 0, 0, 0,
        1, 0, 0, 0,
        1, 1, 1, 1],

    3: [0, 1, 1, 0,
        1, 0, 0, 1,
        0, 0, 0, 1,
        0, 0, 1, 0,
        0, 0, 0, 1,
        0, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0],

    4: [0, 0, 1, 0,
        0, 1, 0, 0,
        1, 0, 0, 0,
        1, 0, 1, 0,
        1, 1, 1, 1,
        0, 0, 1, 0,
        0, 0, 1, 0,
        0, 0, 1, 0],

    5: [1, 1, 1, 1,
        1, 0, 0, 0,
        1, 0, 0, 0,
        1, 1, 1, 0,
        0, 0, 0, 1,
        0, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0],

    6: [0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 0,
        1, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0],

    7: [1, 1, 1, 1,
        1, 0, 0, 1,
        0, 0, 0, 1,
        0, 0, 1, 0,
        0, 0, 1, 0,
        0, 1, 0, 0,
        0, 1, 0, 0,
        0, 1, 0, 0],

    8: [0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0],

    9: [0, 1, 1, 0,
        1, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 1,
        0, 0, 0, 1,
        0, 0, 0, 1,
        1, 0, 0, 1,
        0, 1, 1, 0]
    }

raw_blank = [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
    ]

# Symbols
circle = [
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 1, 1, 1, 1, 0, 0
    ]

triangle = [
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1
    ]

smile = [
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 0, 0, 0, 0, 1, 0,
        1, 0, 1, 0, 0, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 0, 0, 1, 0, 1,
        1, 0, 0, 1, 1, 0, 0, 1,
        0, 1, 0, 0, 0, 0, 1, 0,
        0, 0, 1, 1, 1, 1, 0, 0
    ]

sad = [
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 0, 0, 0, 0, 1, 0,
        1, 0, 1, 0, 0, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 1, 1, 1, 0, 1,
        0, 1, 0, 0, 0, 0, 1, 0,
        0, 0, 1, 1, 1, 1, 0, 0
    ]

heart = [
        0, 1, 1, 0, 0, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0
    ]

walk = [
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 1, 1,
        0, 0, 0, 1, 1, 1, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 1, 1, 0, 0, 1, 1, 0,
        0, 1, 0, 0, 0, 0, 1, 0
    ]

no_walk = [
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0
    ]

square = [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1
    ]

SYMBOLS = (circle, triangle, smile, sad, heart, walk, no_walk, square)