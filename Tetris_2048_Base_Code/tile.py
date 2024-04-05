import lib.stddraw as StdDraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
from Tetris_2048_init import get_finalized_UI as getUI
from animation import pickRandom


class Tile:
    UI = getUI()
    HALF_EDGE = UI.canvas.edge_length / 2

    startingValues = [2, 4]
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 25

    def __init__(self, value=None):
        self.value = value if value is not None else pickRandom(Tile.startingValues)
        self.isEmpty = self.value == 0
        self.destroyMe = False

        # TODO: update color logic
        if self.isEmpty:
            self.background_color = Color(255, 255, 255)
            self.foreground_color = Color(0, 0, 0)
            self.box_color = Color(200, 200, 200)
        else:
            self.background_color = Color(151, 178, 199)  # background (tile) color
            self.foreground_color = Color(0, 100, 200)  # foreground (number) color
            self.box_color = Color(0, 100, 200)  # box (boundary) color

    def merge(self, otherTile):
        if not self.isEmpty:
            if self.value == otherTile.value:
                self.value += otherTile.value
                otherTile.value = 0
                otherTile.isEmpty = True
                otherTile.destroyMe = True
                self.updateColor()
                return True
        return False

    def updateColor(self):
        pass

    def draw(self, y, x):
        # draw the tile as a filled square
        StdDraw.setPenColor(self.background_color)
        StdDraw.filledSquare(x, y, Tile.HALF_EDGE)
        # draw the bounding box around the tile as a square
        StdDraw.setPenColor(self.box_color)
        StdDraw.setPenRadius(Tile.boundary_thickness)
        StdDraw.square(x, y, Tile.HALF_EDGE)
        StdDraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        StdDraw.setPenColor(self.foreground_color)
        StdDraw.setFontFamily(Tile.font_family)
        StdDraw.setFontSize(Tile.font_size)
        StdDraw.text(x, y, str(self.value))
