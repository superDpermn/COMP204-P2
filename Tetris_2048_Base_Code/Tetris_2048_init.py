from user_interface import *
from lib.color import Color

EDGE_LENGTH = 30

# Create new GameCanvas object to represent the visual part of the game box
# This object does not store what happens in the game, or any logic
# it is mainly for cosmetic purposes
gameGrid = GameCanvas(0, 0, 12, 20, EDGE_LENGTH,
                      Style(padding=15, background_color=Color(189, 180, 120),
                            border_color=Color(150, 120, 100), border_width=0.01))

# define all UI elements one-by-one so that we can have fine control over each one.
startButton = UIButton(50, 300, 200, 100, "Start Game",
                       Style(padding=100, background_color=StdDraw.BOOK_LIGHT_BLUE))

settingsButton = UIButton(50, 150, 200, 100, "Settings",
                          Style(padding=100, background_color=Color(150, 150, 200),
                                border_color=Color(200, 150, 120), border_width=0.02))

end_text = UITextBox(300, 300, 120, 100, "Game Over",
                     Style(font_size=30, background_color=Color(255, 255, 255),
                           foreground_color=Color(200, 100, 0), padding=50))


# create scene objects like some lego assembly
mainMenu = Scene(startButton, settingsButton)  # add all UIBlock objects in the main menu scene
gameScene = Scene(gameGrid, isGame=True)
gameOver = Scene(end_text)

# The main container of the UI. stores Scene objects
UI = UIContainer(gameGrid, main=mainMenu, game=gameScene, end=gameOver)

startButton.onclick = lambda: UI.set_scene("game")



# This method ensures that the UI object is finalized and ready
def get_finalized_UI():
    return UI
