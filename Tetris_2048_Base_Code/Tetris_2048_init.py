from user_interface import *
from lib.color import Color

EDGE_LENGTH = 30

# Create new GameCanvas object to represent the visual part of the game box
# This object does not store what happens in the game, or any logic
# it is mainly for cosmetic purposes
gameGrid = GameCanvas(15, 85, 12, 20, EDGE_LENGTH,
                      Style(background_color=Color(189, 180, 120),
                            foreground_color=Color(117, 108, 51)))

# define all UI elements one-by-one so that we can have fine control over each one.
gameLogo = UIImage(38, 453, 524, 197, "TETRIS2048LOGO.png")
startButton = UIButton(200, 200, 200, 70, "Start Game",
                       Style(background_color=StdDraw.BOOK_LIGHT_BLUE))

settingsButton = UIButton(200, 100, 200, 70, "Settings",
                          Style(background_color=Color(150, 150, 200),
                                border_color=Color(150, 150, 150), border_width=0.005))

score_label = UITextBox(390, 655, 195, 30, "Score:",
                        style=Style(font_size=20))
score_value = UITextBox(390, 600, 195, 55, "0",
                        style=Style(foreground_color=StdDraw.DARK_BLUE, font_size=30))
next_tetromino_label = UITextBox(390, 555, 195, 30, "Next")
# next_tetromino_view = TetrominoView(390, 525, 195, 195)  # don't delete, the positions are final
# next_tetromino_view.changeType("T", [2, 4, 4, 2])  # for testing

pauseButton = UIButton(388, 270, 200, 100
                       , style=Style(background_color=StdDraw.WHITE,
                                     border_color=StdDraw.BLACK,
                                     border_width=0.005))
pauseSymbol = UIImage(438, 270, 64, 64, "pause_play.png", style=Style(padding=9))

end_text = UITextBox(200, 300, 200, 100, "Game Over",
                     Style(font_size=30, background_color=Color(255, 255, 255),
                           border_width=0.005))

# This object is supposed to be the largest UI element, stretching the canvas to its size.
windowSpacer = UIBlock(0, 0, 600, 700)

# create scene objects like some lego assembly
# add all UIBlock objects in the main menu scene
mainMenu = Scene(gameLogo, startButton, settingsButton, sceneBackground=Color(48, 96, 130))
gameScene = Scene(gameGrid, score_label, score_value, pauseButton, pauseSymbol,
                  isGame=True, sceneBackground=Color(150, 120, 100))
gameOver = Scene(windowSpacer, end_text)

# The main container of the UI. stores Scene objects
UI = UIContainer(gameGrid, main=mainMenu, game=gameScene, end=gameOver)

startButton.onclick = lambda: UI.set_scene("game")
pauseButton.onclick = lambda: gameGrid.togglePause()
# TODO: remove the following line after UI design is complete
print("current window width:", UI.window_width, "current window height:", UI.window_height)


# This method ensures that the UI object is finalized and ready
def get_finalized_UI():
    return UI
