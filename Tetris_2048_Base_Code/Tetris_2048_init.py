from user_interface import *
from lib.color import Color

Settings = {"EDGE_LENGTH": 30,
            "GRID_WIDTH": 12,
            "GRID_HEIGHT": 20,
            "DIFFICULTY": "NORMAL"}
# The visual edge length of each game tile (in pixels). This value is used for all relevant tasks
EDGE_LENGTH = Settings.get("EDGE_LENGTH", 30)

# -------------------------------Main Menu Scene (Components)----------------------------------
gameLogo = UIImage(38, 453, 524, 197, "TETRIS2048LOGO.png")

startButton = UIButton(200, 200, 200, 70, "Start Game",
                       Style(background_color=StdDraw.BOOK_LIGHT_BLUE))

settingsButton = UIButton(200, 100, 200, 70, "Settings",
                          Style(background_color=Color(150, 150, 200),
                                border_color=Color(150, 150, 150), border_width=0.005))
# ---------------------------------------------------------------------------------------------


# -----------------------------Settings Menu Scene (Components)--------------------------------
settingsMenuBackground = UIImage(0, 0, 600, 700, "tetris_bg.jpg")

backToMainMenuButton = UIButton(15, 635, 100, 50, "<-- Back")

settingsConfirmButton = UIButton(485, 635, 100, 50, "Confirm",
                                 Style(foreground_color=StdDraw.GREEN))

settingsMenuLabel = UITextBox(130, 635, 340, 50, "SETTINGS",
                              Style(font_size=50, background_color=StdDraw.WHITE))

grid_width_decrement = UIButton(140, 250, 50, 50, "GW--")
grid_width_display = UITextBox(200, 245, 60, 60, "12")
grid_width_increment = UIButton(270, 250, 50, 50, "GW++")

grid_height_decrement = UIButton(140, 180, 50, 50, "GH--")
grid_height_display = UITextBox(200, 175, 60, 60, "20")
grid_height_increment = UIButton(270, 180, 50, 50, "GH++")
# ---------------------------------------------------------------------------------------------


# ------------------------------In-Game Scene (Components)-------------------------------------
tetromino_view = TetrominoView(420, 515, 120, 150)

GridCanvas = GameCanvas(15, 15, 12, 20, EDGE_LENGTH,
                        Style(background_color=Color(189, 180, 120),
                              foreground_color=Color(117, 108, 51)),
                        tetromino_view)

score_label = UITextBox(390, 655, 195, 30, "Score:",
                        style=Style(font_size=20))

score_value = UITextBox(390, 600, 195, 55, "0",
                        style=Style(foreground_color=StdDraw.DARK_BLUE, font_size=30))

next_tetromino_label = UITextBox(390, 550, 195, 40, "Next",
                                 Style(background_color=Color(200, 200, 200)))

next_tetromino_bg = UIBlock(390, 390, 195, 195,
                            Style(background_color=Color(189, 180, 120)))

pauseButton = UIButton(390, 255, 195, 125,
                       style=Style(background_color=StdDraw.WHITE))

pauseSymbol = UIImage(438, 265, 64, 64, "pause_play.png", Style(padding=9))
# ---------------------------------------------------------------------------------------------


# ------------------------------Game Over Scene (Components)-----------------------------------
end_text = UITextBox(200, 300, 200, 100, "Game Over",
                     Style(font_size=30, background_color=Color(255, 255, 255),
                           border_width=0.005))

bg_pattern = UIImage(0, 0, 600, 700, "tetris_bg.jpg")
# ---------------------------------------------------------------------------------------------


# -----------------------------------Scene Assembly--------------------------------------------
mainMenu = Scene(gameLogo, startButton, settingsButton,
                 sceneBackground=Color(48, 96, 130))

settingsMenu = Scene(settingsMenuBackground, settingsMenuLabel,
                     backToMainMenuButton, settingsConfirmButton,
                     grid_width_decrement, grid_width_display, grid_width_increment,
                     grid_height_decrement, grid_height_display, grid_height_increment)

gameScene = Scene(GridCanvas, score_label, score_value, pauseButton,
                  pauseSymbol, next_tetromino_bg, next_tetromino_label, tetromino_view,
                  isGame=True, sceneBackground=Color(150, 120, 100))

gameOver = Scene(bg_pattern, end_text)
# ---------------------------------------------------------------------------------------------


# -------------------------Creating The Container For Scenes-----------------------------------
UI = UIContainer(GridCanvas, main=mainMenu, settings=settingsMenu, game=gameScene, end=gameOver)
# ---------------------------------------------------------------------------------------------


# ------------------------------Setting Button Events------------------------------------------
pauseButton.onclick = lambda: GridCanvas.togglePause()
startButton.onclick = lambda: UI.set_scene("game")
settingsButton.onclick = lambda: UI.set_scene("settings")
backToMainMenuButton.onclick = lambda: UI.set_scene("main")


def update_settings():
    if GridCanvas.grid_unset:
        return
    GridCanvas.edge_length = Settings.get("EDGE_LENGTH", 30)
    newGW = Settings.get("GRID_WIDTH", 12)
    newGH = Settings.get("GRID_HEIGHT", 20)
    GridCanvas.game_grid.grid_height, GridCanvas.game_grid.grid_width = newGH, newGW
    GridCanvas.finalize(GridCanvas.game_grid)
    GridCanvas.game_grid.difficulty = Settings.get("DIFFICULTY", "NORMAL")
    print(Settings)  # Temporary


def anyUpdate(updateType=None):
    if updateType is not None:
        if updateType == "GW+":
            Settings.update(
                {"GRID_WIDTH": Settings.get("GRID_WIDTH", 12) + 1 if Settings.get("GRID_WIDTH", 12) < 12 else 12}
            )
            grid_width_display.text = str(int(grid_width_display.text)+1 if
                                          int(grid_width_display.text) < 12 else 12)
        elif updateType == "GW-":
            Settings.update(
                {"GRID_WIDTH": Settings.get("GRID_WIDTH", 12) - 1 if Settings.get("GRID_WIDTH", 12) > 5 else 5}
            )
            grid_width_display.text = str(int(grid_width_display.text) - 1 if
                                          int(grid_width_display.text) > 5 else 5)
        elif updateType == "GH+":
            Settings.update(
                {"GRID_HEIGHT": Settings.get("GRID_HEIGHT", 20) + 1 if Settings.get("GRID_HEIGHT", 20) < 22 else 22}
            )
            grid_height_display.text = str(int(grid_height_display.text) + 1 if
                                           int(grid_height_display.text) < 22 else 22)
        elif updateType == "GH-":
            Settings.update(
                {"GRID_HEIGHT": Settings.get("GRID_HEIGHT", 20) - 1 if Settings.get("GRID_HEIGHT", 20) > 10 else 10}
            )
            grid_height_display.text = str(int(grid_height_display.text) - 1 if
                                           int(grid_height_display.text) > 10 else 10)
        else:
            return


grid_width_increment.onclick = lambda: anyUpdate("GW+")
grid_width_decrement.onclick = lambda: anyUpdate("GW-")
grid_height_increment.onclick = lambda: anyUpdate("GH+")
grid_height_decrement.onclick = lambda: anyUpdate("GH-")


settingsConfirmButton.onclick = lambda: update_settings()
# ---------------------------------------------------------------------------------------------


# TODO: remove the following line after UI design is complete
print("current window width:", UI.window_width, "current window height:", UI.window_height)


# This method ensures that the UI object is finalized and ready
def get_finalized_UI():
    return UI
