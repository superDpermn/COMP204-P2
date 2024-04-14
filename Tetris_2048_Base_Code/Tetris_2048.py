################################################################################
#                                                                              #
#               The main program of Tetris 2048 Game (by Group 7)              #
#                                                                              #
################################################################################

import lib.stddraw as StdDraw  # for creating an animation with user interactions
from game_grid import GameGrid
from tetromino import Tetromino  # the class for modeling the tetrominoes
from Tetris_2048_init import get_finalized_UI as getUI
from InputController import InputController


class GameInstance:
    def __init__(self):
        self.UI = getUI()
        gridSizes = self.UI.getGridSizes()
        # set the game grid dimension values stored and used in the Tetromino class
        Tetromino.grid_width, Tetromino.grid_height = gridSizes

        self.grid = GameGrid(gridSizes)
        self.UI.canvas.finalize(self.grid)

        self.inputController = InputController()
        # define the condition to run the program loop for
        self.play = True

    def scene_loop(self):
        while True:
            self.inputController.update()
            keyEvents = self.inputController.getKeyEvents()
            mouseEvent = self.inputController.mouseEvent
            # draw and update the current scene
            self.UI.draw(keyEvents, mouseEvent, 17)  # this argument does not pause StdDraw
            # show and pause for 17ms duration ~= 59 frames/second
            StdDraw.show(17)

            # clear the canvas
            StdDraw.clear(StdDraw.BLACK)
            if self.UI.canvas.game_grid.game_over:
                break
        return True

    def run(self):
        # game_canvas = UI.canvas

        # It is assumed at this point that double buffering is enabled.

        # Set the current scene before creating the program window
        self.UI.launch("main")

        while self.play:
            self.scene_loop()

            self.UI.set_scene("end")

            StdDraw.clear(StdDraw.BLACK)
            self.UI.draw((), (), 17)

            StdDraw.show(3000)
            self.play = False

        print("Thanks for playing!")


# Create new game instance
Game = GameInstance()
# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    Game.run()
