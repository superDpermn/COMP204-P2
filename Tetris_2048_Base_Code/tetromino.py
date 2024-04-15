from tile import Tile  # used for modeling each tile on the tetrominoes
from animation import pickRandom, Animation
import math
import lib.stddraw as StdDraw


# Custom-made tetromino class
class Tetromino:
    CELL_EDGE_LENGTH = 30
    GRID_WIDTH = 12
    GRID_HEIGHT = 20
    canvas_height = CELL_EDGE_LENGTH*GRID_HEIGHT
    canvas_width = CELL_EDGE_LENGTH*GRID_WIDTH
    box_offset_x = 15
    box_offset_y = 15
    yModifier = 0
    xModifier = 0

    # A static method to update class variables.
    # Must be called before any Tetromino objects are created.
    @classmethod
    def set_grid(cls, canvas):
        cls.GRID_WIDTH = canvas.grid_w
        cls.GRID_HEIGHT = canvas.grid_h
        cls.CELL_EDGE_LENGTH = canvas.edge_length
        cls.canvas_width, cls.canvas_height = cls.CELL_EDGE_LENGTH*cls.GRID_WIDTH, cls.CELL_EDGE_LENGTH*cls.GRID_HEIGHT
        cls.box_offset_x = canvas.x + canvas.style.padding
        cls.box_offset_y = canvas.y + canvas.style.padding
        cls.yModifier = cls.box_offset_y + cls.canvas_height - cls.CELL_EDGE_LENGTH
        cls.xModifier = cls.box_offset_x
        Tile.UpdateConstants(cls.CELL_EDGE_LENGTH)

    def __init__(self):
        self.type = pickRandom(["O", "L", "J", "T", "Z", "S", "I"])
        self.tilePositions = []
        self.rotationAxis = []
        self.centerGridCoords = [0, 0]
        self.assignTilePositions()
        self.borderCoords = []
        self.tiles = [Tile(), Tile(), Tile(), Tile()]
        self.spawnOffset = 0
        anim_start_positions = [
            [
                (self.tilePositions[t][0]) * Tetromino.CELL_EDGE_LENGTH,
                (self.tilePositions[t][1]) * Tetromino.CELL_EDGE_LENGTH
            ]
            for t in range(len(self.tilePositions))]
        self.animation = [
            Animation(anim_start_positions[i], anim_start_positions[i])
            for i in range(len(self.tilePositions))
        ]
        self.animation_positions = anim_start_positions
        centerStartPosY = self.centerGridCoords[0]*Tetromino.CELL_EDGE_LENGTH+Tetromino.yModifier
        centerStartPosX = self.centerGridCoords[1]*Tetromino.CELL_EDGE_LENGTH+Tetromino.xModifier
        self.centerAnimation = Animation([centerStartPosY, centerStartPosX],
                                         [centerStartPosY, centerStartPosX])
        self.center_position = [self.centerAnimation.current_pos[0], self.centerAnimation.current_pos[1]]

    def assignTilePositions(self):
        if self.type == "O":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [1, 1+xOffset], [1, xOffset]]
            self.rotationAxis = [0.5, 0.5+xOffset]
            self.centerGridCoords = [0.5, 0.5+xOffset]
        elif self.type == "L":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [1, xOffset], [2, xOffset], [2, 1+xOffset]]
            self.rotationAxis = [1, xOffset]
            self.centerGridCoords = [1.5, 0.5+xOffset]
        elif self.type == "J":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, 1+xOffset], [1, 1+xOffset], [2, 1+xOffset], [2, xOffset]]
            self.rotationAxis = [1, 1+xOffset]
            self.centerGridCoords = [2.5, 1.5+xOffset]
        elif self.type == "T":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 3))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [0, 2+xOffset], [1, 1+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
            self.centerGridCoords = [0.5, 1.5+xOffset]
        elif self.type == "Z":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 3))
            self.tilePositions = [[0, 1+xOffset], [0, 2+xOffset], [1, xOffset], [1, 1+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
            self.centerGridCoords = [1, 1.5+xOffset]
        elif self.type == "S":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [1, 1+xOffset], [1, 2+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
            self.centerGridCoords = [1, 1.5+xOffset]
        elif self.type == "I":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 1))
            self.tilePositions = [[0, xOffset], [1, xOffset], [2, xOffset], [3, xOffset]]
            self.rotationAxis = [1, xOffset]
            self.centerGridCoords = [2, 0.5+xOffset]
        else:
            return

    def onUpdate(self):
        for animIndex in range(len(self.animation)):
            self.animation[animIndex].start(
                [self.tilePositions[animIndex][i] * Tetromino.CELL_EDGE_LENGTH for i in range(2)]
            )
        self.centerAnimation.start(
            [-self.centerGridCoords[0]*Tetromino.CELL_EDGE_LENGTH+Tetromino.yModifier,
             self.centerGridCoords[1]*Tetromino.CELL_EDGE_LENGTH+Tetromino.xModifier]
        )

    def canMove(self, direction="down"):
        canMove = True
        coords = []
        if direction == "left":
            for pos in self.tilePositions:
                if pos[1] <= 0:
                    canMove = False
                    break
                coords.append([pos[0], pos[1]-1])
            if canMove:
                return coords
        elif direction == "right":
            for pos in self.tilePositions:
                if pos[1] >= Tetromino.GRID_WIDTH-1:
                    canMove = False
                    break
                coords.append([pos[0], pos[1]+1])
            if canMove:
                return coords
        elif direction == "down":
            for pos in self.tilePositions:
                if pos[0] >= Tetromino.GRID_HEIGHT-1:
                    canMove = False
                    break
                coords.append([pos[0]+1, pos[1]])
            if canMove:
                return coords
        elif direction == "up":
            for pos in self.tilePositions:
                newCoord = [int(self.rotationAxis[1]+self.rotationAxis[0]-pos[1]),
                            int(self.rotationAxis[1]-self.rotationAxis[0]+pos[0])]
                if (newCoord[0] < 0 or newCoord[0] > Tetromino.GRID_HEIGHT-1
                        or newCoord[1] > Tetromino.GRID_WIDTH-1 or newCoord[1] < 0):
                    canMove = False
                    break
                coords.append(newCoord)
            if canMove:
                return coords
        return None

    def animation_update(self, delta_time):
        for i in range(4):
            self.animation_positions[i] = self.animation[i].update(delta_time)
        self.centerAnimation.update(delta_time)

    def draw(self, x=None, y=None):
        if x is not None and y is not None:
            for i in range(4):
                self.tiles[i].draw(y-(self.tilePositions[i][0]-self.rotationAxis[0]+1)*Tetromino.CELL_EDGE_LENGTH,
                                   x+(self.tilePositions[i][1]-self.rotationAxis[1]+1)*Tetromino.CELL_EDGE_LENGTH)
        else:
            for i in range(4):
                self.tiles[i].draw(Tetromino.yModifier
                                   - self.animation_positions[i][0],
                                   Tetromino.box_offset_x
                                   + self.animation_positions[i][1])
            # self.draw_border()

    def draw_border(self):
        border_coordinates = set()
        for pos in self.animation_positions:
            y, x = pos
            border_coordinates.add((y, x))
            border_coordinates.add((y-Tetromino.CELL_EDGE_LENGTH, x))
            border_coordinates.add((y, x+Tetromino.CELL_EDGE_LENGTH))
            border_coordinates.add((y-Tetromino.CELL_EDGE_LENGTH, x+Tetromino.CELL_EDGE_LENGTH))

        def get_angle(point, reference):  # points as (y, x)
            # Calculate angle of point with respect to reference point
            dx = point[1] - reference[1]
            dy = point[0] - reference[0]
            return math.atan2(dy, dx)

        sorted_points = sorted(border_coordinates,
                               key=lambda temp: get_angle(temp, (self.center_position[0], self.center_position[1])))

        # StdDraw.setPenColor(StdDraw.BLACK)
        # StdDraw.setFontSize(10)
        # for p in range(len(sorted_points)):
        #     StdDraw.text(Tetromino.xModifier+sorted_points[p][1], Tetromino.yModifier-sorted_points[p][0], str(p))
        # StdDraw.point(self.centerAnimation.current_pos[1],
        #               self.centerAnimation.current_pos[0])

        StdDraw.setPenColor(StdDraw.WHITE)
        StdDraw.setPenRadius(0.005)
        StdDraw.polygon([Tetromino.xModifier+sorted_points[i][1] for i in range(len(sorted_points))],
                        [Tetromino.yModifier-sorted_points[i][0] for i in range(len(sorted_points))])

    def moveLeft(self):
        for i in range(4):
            self.tilePositions[i][1] -= 1
        self.rotationAxis[1] -= 1
        self.centerGridCoords[1] -= 1
        self.onUpdate()

    def moveRight(self):
        for i in range(4):
            self.tilePositions[i][1] += 1
        self.rotationAxis[1] += 1
        self.centerGridCoords[1] += 1
        self.onUpdate()

    def moveDown(self):
        for i in range(4):
            self.tilePositions[i][0] += 1
        self.rotationAxis[0] += 1
        self.centerGridCoords[0] += 1
        self.onUpdate()

    def rotate(self):
        newCoords = []
        for pos in self.tilePositions:
            newCoords.append(
                [
                    int(self.rotationAxis[1] + self.rotationAxis[0] - pos[1]),
                    int(self.rotationAxis[1] - self.rotationAxis[0] + pos[0])
                ]
            )
        for i in range(4):
            self.tilePositions[i] = newCoords[i]
        self.centerGridCoords = [
            self.rotationAxis[1] + self.rotationAxis[0] - self.centerGridCoords[1],
            self.rotationAxis[1] - self.rotationAxis[0] + self.centerGridCoords[0]
        ]
        self.onUpdate()
