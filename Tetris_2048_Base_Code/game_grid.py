from tetromino import Tetromino


class GameGrid:
    def __init__(self, grid_size: tuple[int, int] = (12, 20),
                 starting_tetromino=Tetromino()):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_size[1]
        self.grid_width = grid_size[0]
        self.tile_matrix = [[None for i in range(self.grid_width)] for j in range(self.grid_height)]
        # create a tile matrix to store the tiles locked on the game grid
        # self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino: Tetromino = starting_tetromino
        self.nextTetromino = Tetromino()
        self.difficulty = "NORMAL"
        # the game_over flag shows whether the game is over or not
        self.game_over = False

    def place_tetromino(self):
        # ...
        # game logic
        for t in range(4):
            pos = self.current_tetromino.tilePositions[t]
            self.tile_matrix[pos[0]][pos[1]] = self.current_tetromino.tiles[t]
        # ...

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
