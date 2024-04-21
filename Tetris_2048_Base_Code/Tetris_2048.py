################################################################################
#                                                                              #
#               The main program of Tetris 2048 Game (by Group 7)              #
#                                                                              #
################################################################################

import lib.stddraw as StdDraw  # for creating an animation with user interactions
from game_grid import GameGrid
from tetromino import Tetromino  # the class for modeling the tetrominoes
from Tetris_2048_init import get_finalized_UI as getUI
from Tetris_2048_init import update_settings as finalize_reset
from Tetris_2048_init import Settings
from Tetris_2048_init import updateScores
from Tetris_2048_init import registerScoreChanges
from Tetris_2048_init import dialog, resetDialog
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

        self.dialogAnswer = 0

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

    def game_end_loop(self):
        self.UI.scenes.get("end").actors[-1].text = str(self.UI.canvas.score)
        while True:
            self.inputController.update()
            self.UI.draw(self.inputController.getKeyEvents(), self.inputController.mouseEvent, 17)
            StdDraw.show(17)

            StdDraw.clear(StdDraw.BLACK)

            self.dialogAnswer = dialog()
            if self.dialogAnswer == 1:
                self.play = True
                self.dialogAnswer = 0
                resetDialog()
                return False
            elif self.dialogAnswer == 2:
                self.play = False
                self.dialogAnswer = 0
                resetDialog()
                return True

    def run(self):
        self.update_scores()
        # Set the current scene before creating the program window
        self.UI.launch("main")

        while self.play:
            self.UI.set_scene("main")

            self.scene_loop()
            self.update_scores()

            self.UI.set_scene("end")

            if self.game_end_loop():
                break

            if self.play:
                self.resetGrid()

        print("Thanks for playing!")

    def resetGrid(self):
        self.grid = GameGrid((Settings.get("GRID_WIDTH", 12), Settings.get("GRID_HEIGHT", 20)))
        self.UI.reset(finalize_reset(self.grid))

    def update_scores(self):
        # Read existing scores from the file
        try:
            with open("scoreboard.txt", 'r') as file:
                scores = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            scores = []

        # Add the new score to the list
        scores.append(self.UI.canvas.score)

        # Sort the scores in descending order
        scores.sort(reverse=True)

        # Keep only the top 10 scores
        scores = scores[:10]

        while len(scores) < 10:
            scores.append(0)

        # Write the updated scores back to the file
        with open("scoreboard.txt", 'w') as file:
            for s in scores:
                file.write(str(s) + '\n')

        updateScores(scores)
        registerScoreChanges()


# Create new game instance
Game = GameInstance()
# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    Game.run()
