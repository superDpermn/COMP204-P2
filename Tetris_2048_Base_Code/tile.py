import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
from additions.gamemap_constants import get_tile_color as num_color
from additions.gamemap_constants import get_start_num
# Class used for modeling numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a tile with 2 as the number on it
    def __init__(self, num = None):
        # set the number on the tile
        self.number = num if num is not None else get_start_num()
        # set the colors of the tile
        temp_bg = num_color(self.number)
        temp_border = num_color(self.number, True)
        self.background_color = Color(temp_bg[0], temp_bg[1], temp_bg[2]) # background (tile) color
        self.foreground_color = Color(0, 100, 200)  # foreground (number) color
        self.box_color = Color(temp_border[0], temp_border[1], temp_border[2]) # box (boundary) color

    # Method for drawing the tile
    def draw(self, position, length=100):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x * 100 + 50, position.y * 100 + 50, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x * 100 + 50, position.y * 100 + 50, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x * 100 + 50, position.y * 100 + 50, str(self.number))
