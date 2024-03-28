from random import randint

GRIDWIDTH, GRIDHEIGHT = 12,20
TILEWIDTH, TILEHEIGHT = 100,100
CANVAS_TILEWIDTH, CANVAS_TILEHEIGHT = 38, 38
CANVASWIDTH, CANVASHEIGHT = GRIDWIDTH * CANVAS_TILEWIDTH, GRIDHEIGHT * CANVAS_TILEHEIGHT


# ChatGPT code
def get_tile_color(value, is_border=False):
    if value > 4096:
        value = 4096
    color_map = {
        2: (238, 228, 218),  # beige
        4: (237, 224, 200),  # light yellow
        8: (242, 177, 121),  # orange
        16: (245, 149, 99),  # light orange
        32: (246, 124, 95),  # salmon
        64: (246, 94, 59),  # light red
        128: (237, 207, 114),  # yellow
        256: (237, 204, 97),  # light yellow
        512: (237, 200, 80),  # gold
        1024: (237, 197, 63),  # light gold
        2048: (237, 194, 46),  # goldenrod
        4096: (237, 194, 46),  # goldenrod (same color as 2048 for values > 4096)
    }
    temp = color_map.get(value, (0, 0, 0))  # default to black if value not in color_map
    tempR, tempG, tempB = temp[0], temp[1], temp[2]
    if is_border:
        tempR = tempR - 20 if tempR > 20 else 0
        tempG = tempG - 20 if tempG > 20 else 0
        tempB = tempB - 20 if tempB > 20 else 0
    return tempR, tempG, tempB


def get_start_num():
    possible_values = [2,4]
    return possible_values[randint(0,1)]