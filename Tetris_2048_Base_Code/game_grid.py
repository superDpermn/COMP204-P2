from tetromino import Tetromino
from user_interface import UIContainer
from InputController import KeyboardEvent


class GameGrid:
    def __init__(self, UI: UIContainer, grid_size: tuple[int, int] = (12, 20),
                 starting_tetromino: Tetromino = Tetromino()):
        # set the dimensions of the game grid as the given arguments
        self.UI = UI
        self.grid_height = grid_size[1]
        self.grid_width = grid_size[0]
        self.tile_matrix = [[None for i in range(self.grid_width)] for j in range(self.grid_height)]
        # create a tile matrix to store the tiles locked on the game grid
        # self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino: Tetromino = starting_tetromino
        # the game_over flag shows whether the game is over or not
        self.game_over = False

    def onInput(self, *events):
        for event in events:
            if isinstance(event, KeyboardEvent):
                # handle keyboard event with a switch-like statement
                if event.key == "up" or event.key == "w":
                    self.move_UP()
                elif event.key == "left" or event.key == "a":
                    self.move_LEFT()
                elif event.key == "down" or event.key == "s":
                    self.move_DOWN()
                elif event.key == "right" or event.key == "d":
                    self.move_RIGHT()

    def place_tetromino(self):
        pass

    def move_UP(self):
        pass

    def move_LEFT(self):
        pass

    def move_DOWN(self):
        pass

    def move_RIGHT(self):
        pass

    def get_canvas_data(self):
        return self.current_tetromino, self.tile_matrix
