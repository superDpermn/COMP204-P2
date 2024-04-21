import os
from lib.picture import Picture
import lib.stddraw as StdDraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
from animation import pickRandom


colorDictionary = {2: Color(238, 228, 218),
                   4: Color(236, 224, 202),
                   8: Color(242, 177, 121),
                   16: Color(236, 141, 83),
                   32: Color(245, 124, 95),
                   64: Color(233, 88, 57),
                   128: Color(237, 207, 114),
                   256: Color(241, 208, 75),
                   512: Color(237, 200, 80),
                   1024: Color(237, 197, 63),
                   2048: Color(237, 194, 46)
                   }

defaultColor = Color(60, 58, 50)


class Tile:
    HALF_EDGE = 15
    TILE_GAP = 1

    startingValues = (2, 4)
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 20

    @classmethod
    def UpdateConstants(cls, EDGE_LENGTH=30, GAP=1):
        cls.HALF_EDGE = EDGE_LENGTH/2
        cls.TILE_GAP = GAP

    tileImages = [Picture(os.path.dirname(os.path.realpath(__file__)) + "/images/Tile" + str(tileNum) + ".png")
                  for tileNum in colorDictionary.keys()]

    imageMap = {2: 0, 4: 1, 8: 2, 16: 3, 32: 4, 64: 5, 128: 6, 256: 7, 512: 8, 1024: 9, 2048: 10}

    def __init__(self, value=None):
        self.value: int = value if value is not None else pickRandom(Tile.startingValues)
        if self.value < 4096:
            self.image = Tile.tileImages[Tile.imageMap.get(self.value, 0)]
        else:
            self.image = None
        self.isEmpty = self.value == 0
        self.destroyMe = False

        self.background_color = colorDictionary.get(self.value, defaultColor)
        self.foreground_color = Color(249, 246, 242) if (4 < self.value < 128) else Color(119, 110, 101)

    def merge(self, otherTile):
        if not self.isEmpty:
            if self.value == otherTile.value:
                self.value += otherTile.value
                otherTile.value = 0
                otherTile.isEmpty = True
                otherTile.destroyMe = True
                otherTile.updateColor()
                self.updateColor()
                return True
        return False

    def updateColor(self):
        self.background_color = colorDictionary.get(self.value, defaultColor)
        self.foreground_color = Color(249, 246, 242) if self.value > 4 else Color(119, 110, 101)
        if self.value < 4096:
            self.image = Tile.tileImages[Tile.imageMap.get(self.value, 0)]
        else:
            self.image = None

    def draw(self, y, x):
        if self.image is not None:
            StdDraw.picture(self.image, x+Tile.HALF_EDGE, y+Tile.HALF_EDGE)
        else:
            # draw the tile as a filled square
            StdDraw.setPenColor(self.background_color)
            StdDraw.filledSquare(x+Tile.HALF_EDGE, y+Tile.HALF_EDGE, Tile.HALF_EDGE-Tile.TILE_GAP)
            # draw the bounding box around the tile as a square (disabled as a style choice)
            # StdDraw.setPenColor(self.box_color)
            # StdDraw.setPenRadius(Tile.boundary_thickness)
            # StdDraw.square(x+Tile.HALF_EDGE, y+Tile.HALF_EDGE, Tile.HALF_EDGE)
            StdDraw.setPenRadius()  # reset the pen radius to its default value
            # draw the number on the tile
            StdDraw.setPenColor(self.foreground_color)
            StdDraw.setFontFamily(Tile.font_family)
            StdDraw.setFontSize(Tile.font_size)
            StdDraw.text(x+Tile.HALF_EDGE, y+Tile.HALF_EDGE, str(self.value))

