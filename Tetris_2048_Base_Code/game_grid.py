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
        # the game_over flag shows whether the game is over or not
        self.game_over = False

    def place_tetromino(self):
        # ...
        # game logic
        # ...

        # create new tetromino
        self.current_tetromino = Tetromino()

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

    def move_DOWN(self):
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

