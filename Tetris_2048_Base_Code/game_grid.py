from tetromino import Tetromino
from tile import Tile

difficultyIntervalMultipliers = {"EASY": 1.4, "NORMAL": 1, "HARD": 0.7}


class GameGrid:
    def __init__(self, grid_size: tuple[int, int] = (12, 20),
                 starting_tetromino=Tetromino()):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_size[1]
        self.grid_width = grid_size[0]
        self.tile_matrix: list[list[Tile | None]] = [
            [None for i in range(self.grid_width)] for j in range(self.grid_height)
        ]
        self.scoreList: list[int] = []
        # create a tile matrix to store the tiles locked on the game grid
        # self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino: Tetromino = starting_tetromino
        self.nextTetromino = Tetromino()
        self.difficulty = "NORMAL"
        self.auto_fall_interval = 1000
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        self.placed_count = 0

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.auto_fall_interval = difficultyIntervalMultipliers.get(self.difficulty, 1)*1000

    def place_tetromino(self):
        self.placed_count += 1
        self.auto_fall_interval = ((difficultyIntervalMultipliers.get(self.difficulty, 1)
                                   * max((1000-self.placed_count), 0)) + 150)
        # ...
        # game logic
        for t in range(4):
            pos = self.current_tetromino.tilePositions[t]
            self.tile_matrix[pos[0]][pos[1]] = self.current_tetromino.tiles[t]

        mergeRow = self.grid_height-1
        while mergeRow > 0:  # ignore the topmost row for this loop
            didMerge = False
            for col in range(self.grid_width):
                currentTile = self.tile_matrix[mergeRow][col]
                currentNB = self.tile_matrix[mergeRow-1][col]
                if isinstance(currentTile, Tile) and isinstance(currentNB, Tile):
                    if currentTile.value == currentNB.value:
                        self.scoreList.append(currentTile.value * 2)

                        self.tile_matrix[mergeRow][col].value = self.tile_matrix[mergeRow][col].value * 2
                        self.tile_matrix[mergeRow][col].updateColor()
                        self.tile_matrix[mergeRow-1][col] = None

                        for slideIndex in range(mergeRow-1, 0, -1):
                            self.tile_matrix[slideIndex][col] = self.tile_matrix[slideIndex-1][col]
                        self.tile_matrix[0][col] = None
                        # check from the very bottom again
                        mergeRow = self.grid_height-1
                        didMerge = True
            # this is effective only if there are no more merge operations left for the current column
            if not didMerge:
                mergeRow -= 1

        clearRow = self.grid_height-1
        while clearRow > 0:
            combo = 0
            comboScore = 0
            for col in range(self.grid_width):
                if self.tile_matrix[clearRow][col] is not None:
                    combo += 1
                    comboScore += self.tile_matrix[clearRow][col].value
                else:
                    break
            if combo == self.grid_width:
                # Take a note of the score
                self.scoreList.append(comboScore)
                # Clear current row
                for clearCol in range(self.grid_width):
                    self.tile_matrix[clearRow][clearCol] = None
                # Slide the remaining tiles
                for h in range(clearRow, 0, -1):
                    self.tile_matrix[h] = self.tile_matrix[h-1]
                self.tile_matrix[0] = [None for i in range(self.grid_width)]
                # Check again as another full row may have replaced the current row
            else:
                clearRow -= 1
        # ...
        while self.handleNonConnectedTiles():
            continue

        # create new tetromino
        self.current_tetromino = self.nextTetromino
        # create next tetromino for showing the user
        self.nextTetromino = Tetromino()

        # if the new tetromino collides with a placed tile, it is game over
        for t in self.current_tetromino.tilePositions:
            if self.tile_matrix[t[0]][t[1]] is not None:
                self.game_over = True
                break

    def rotate(self):
        answer = self.current_tetromino.canMove("up")
        if answer is not None:
            confirm = True
            for t in answer:
                if self.tile_matrix[t[0]][t[1]] is not None:
                    confirm = False
                    break
            if confirm:
                self.current_tetromino.rotate()

    def move_LEFT(self):
        answer = self.current_tetromino.canMove("left")
        if answer is not None:
            confirm = True
            for t in answer:
                if self.tile_matrix[t[0]][t[1]] is not None:
                    confirm = False
                    break
            if confirm:
                self.current_tetromino.moveLeft()

    def move_DOWN(self) -> bool:
        # temporary, for testing animations
        answer = self.current_tetromino.canMove("down")
        if answer is not None:
            confirm = True
            for t in answer:
                if self.tile_matrix[t[0]][t[1]] is not None:
                    confirm = False
                    break
            if confirm:
                self.current_tetromino.moveDown()
                return False
            else:
                self.place_tetromino()
                return True
        else:
            self.place_tetromino()
            return True

    def move_RIGHT(self):
        answer = self.current_tetromino.canMove("right")
        if answer is not None:
            confirm = True
            for t in answer:
                if self.tile_matrix[t[0]][t[1]] is not None:
                    confirm = False
                    break
            if confirm:
                self.current_tetromino.moveRight()

    def handleNonConnectedTiles(self):
        connectedPositions = [(self.grid_height-1, col) for col in range(self.grid_width)
                              if self.tile_matrix[self.grid_height-1][col] is not None]

        iterationSuccess = True
        while iterationSuccess:
            iterationSuccess = False
            for row in range(self.grid_height-2, 0, -1):
                for col in range(self.grid_width):
                    if self.tile_matrix[row][col] is not None and (row, col) not in connectedPositions:
                        if (row + 1, col) in connectedPositions:
                            connectedPositions.append((row, col))
                            iterationSuccess = True
                            continue
                        if col > 0:
                            if (row, col-1) in connectedPositions:
                                connectedPositions.append((row, col))
                                iterationSuccess = True
                                continue
                        if col < self.grid_width-1:
                            if (row, col+1) in connectedPositions:
                                connectedPositions.append((row, col))
                                iterationSuccess = True
                                continue
        ret = False
        for row in range(self.grid_height-2, 0, -1):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None and (row, col) not in connectedPositions:
                    self.tile_matrix[row+1][col] = self.tile_matrix[row][col]
                    self.tile_matrix[row][col] = None
                    ret = True
        return ret
