from user_interface import UIContainer, Scene, Style
from graphics import GameCanvas, UIButton
import lib.stddraw as StdDraw

# Create new GameCanvas object to represent the visual part of the game box
# This object does not store what happens in the game, or any logic
# it is mainly for cosmetic purposes
gameGrid = GameCanvas(0, 0, 10, 10, 30, style=Style(padding=30))

UI = UIContainer(gameGrid)

startButton = UIButton(0, 300, 200, 100, "Start Game",
                       Style(border_width=5, padding=100),
                       onclick=UI.set_scene("game"))

mainMenu = Scene(startButton)
gameScene = Scene(gameGrid)
gameOver = Scene()

UI.addScenes(main=mainMenu, game=gameScene, end=gameOver)
