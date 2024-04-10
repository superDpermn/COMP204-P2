from tile import Tile  # used for modeling each tile on the tetrominoes
from animation import pickRandom, Animation
from Tetris_2048_init import get_finalized_UI as getUI


# Custom-made tetromino class
class Tetromino:
    # get the UIContainer object with finalized parameters
    UI = getUI()
    # synchronize parameters
    CELL_EDGE_LENGTH = UI.canvas.edge_length
    GRID_WIDTH = UI.canvas.grid_w
    GRID_HEIGHT = UI.canvas.grid_h
    canvas_height = UI.canvas.box_height
    canvas_width = UI.canvas.box_width
    box_offset_x = UI.canvas.x + UI.canvas.style.padding
    box_offset_y = UI.canvas.y + UI.canvas.style.padding

    # A static method to update class variables.
    # Must be called before any Tetromino objects are created.
    @classmethod
    def set_grid(cls, grid_width, grid_height, visual_edge_length):
        cls.GRID_WIDTH = grid_width
        cls.GRID_HEIGHT = grid_height
        cls.CELL_EDGE_LENGTH = visual_edge_length

    def __init__(self):
        self.type = pickRandom(["O", "L", "J", "T", "Z", "N", "I"])
        self.tilePositions = []
        self.rotationAxis = []
        self.assignTilePositions()
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

    def assignTilePositions(self):
        xOffset = 0
        if self.type == "O":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [1, xOffset], [1, 1+xOffset]]
            self.rotationAxis = [1, xOffset]
        elif self.type == "L":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [1, xOffset], [2, xOffset], [2, 1+xOffset]]
            self.rotationAxis = [1, xOffset]
        elif self.type == "J":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, 1+xOffset], [1, 1+xOffset], [2, xOffset], [2, 1+xOffset]]
            self.rotationAxis = [1, 1+xOffset]
        elif self.type == "T":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 3))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [0, 2+xOffset], [1, 1+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
        elif self.type == "Z":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 3))
            self.tilePositions = [[0, 1+xOffset], [0, 2+xOffset], [1, xOffset], [1, 1+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
        elif self.type == "N":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 2))
            self.tilePositions = [[0, xOffset], [0, 1+xOffset], [1, 1+xOffset], [1, 2+xOffset]]
            self.rotationAxis = [0, 1+xOffset]
        elif self.type == "I":
            xOffset = pickRandom(range(0, Tetromino.GRID_WIDTH - 1))
            self.tilePositions = [[0, xOffset], [1, xOffset], [2, xOffset], [3, xOffset]]
            self.rotationAxis = [1, xOffset]
        else:
            return
        self.spawnOffset = xOffset

    def onUpdate(self):
        for animIndex in range(len(self.animation)):
            self.animation[animIndex].start(
                [self.tilePositions[animIndex][i] * Tetromino.CELL_EDGE_LENGTH for i in range(2)]
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
                newCoord = [self.rotationAxis[1]+self.rotationAxis[0]-pos[1],
                            self.rotationAxis[1]-self.rotationAxis[0]+pos[0]]
                if (newCoord[0] < 0 or newCoord[0] > Tetromino.GRID_HEIGHT-1
                        or newCoord[1] > Tetromino.GRID_WIDTH-1 or newCoord[1] < 0):
                    canMove = False
                    break
                coords.append(newCoord)
            if canMove:
                return coords
        return None

    # TODO: add tetromino border effect

    def animation_update(self, delta_time):
        for i in range(4):
            self.animation_positions[i] = self.animation[i].update(delta_time)

    def draw(self, x=None, y=None):
        if x is not None and y is not None:
            for i in range(4):
                self.tiles[i].draw(y-self.tilePositions[i][0]*Tetromino.CELL_EDGE_LENGTH,
                                   x+(self.tilePositions[i][1]-self.rotationAxis[1]+1)*Tetromino.CELL_EDGE_LENGTH)
        else:
            for i in range(4):
                self.tiles[i].draw(Tetromino.box_offset_y
                                   + Tetromino.canvas_height
                                   - Tetromino.CELL_EDGE_LENGTH
                                   - self.animation_positions[i][0],
                                   Tetromino.box_offset_x
                                   + self.animation_positions[i][1])

    def moveLeft(self):
        for i in range(4):
            self.tilePositions[i][1] -= 1
        self.rotationAxis[1] -= 1
        self.onUpdate()

    def moveRight(self):
        for i in range(4):
            self.tilePositions[i][1] += 1
        self.rotationAxis[1] += 1
        self.onUpdate()

    def moveDown(self):
        for i in range(4):
            self.tilePositions[i][0] += 1
        self.rotationAxis[0] += 1
        self.onUpdate()

    def rotate(self):
        newCoords = []
        for pos in self.tilePositions:
            newCoords.append(
                [
                    self.rotationAxis[1] + self.rotationAxis[0] - pos[1],
                    self.rotationAxis[1] - self.rotationAxis[0] + pos[0]
                ]
            )
        for i in range(4):
            self.tilePositions[i] = newCoords[i]
        self.onUpdate()
