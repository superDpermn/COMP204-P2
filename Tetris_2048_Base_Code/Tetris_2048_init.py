from user_interface import *
from lib.color import Color

# Create new GameCanvas object to represent the visual part of the game box
# This object does not store what happens in the game, or any logic
# it is mainly for cosmetic purposes
gameGrid = GameCanvas(0, 0, 12, 20, 30, Style(padding=30))

# define all UI elements one-by-one so that we can have fine control over each one.
startButton = UIButton(50, 300, 200, 100, "Start Game",
                       Style(padding=100))
end_text = UITextBox(300, 300, 120, 100, "Game Over",
                     Style(font_size=30, background_color=Color(255, 255, 255),
                           foreground_color=Color(200, 100, 0), padding=50))


# create scene objects like some lego assembly
mainMenu = Scene(startButton)  # add all UIBlock objects in the main menu scene
gameScene = Scene(gameGrid, isGame=True)
gameOver = Scene(end_text)

# The main container of the UI. stores Scene objects
UI = UIContainer(gameGrid, main=mainMenu, game=gameScene, end=gameOver)

startButton.onclick = lambda: UI.set_scene("game")


# This method ensures that the UI object is finalized and ready
def get_finalized_UI():
    return UI
