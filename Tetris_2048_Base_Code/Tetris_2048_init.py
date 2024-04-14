from user_interface import *
from lib.color import Color

Settings = {"EDGE_LENGTH": 30,
            "GRID_WIDTH": 12,
            "GRID_HEIGHT": 20,
            "DIFFICULTY": "HARD"}
# The visual edge length of each game tile (in pixels). This value is used for all relevant tasks
EDGE_LENGTH = Settings.get("EDGE_LENGTH", 30)
header_font_size = 40  # Font size for headings
content_font_size = 20

# -------------------------------Main Menu Scene (Components)----------------------------------
gameLogo = UIImage(120, 400, 360, 206, "Logo.png")

startButton = UIButton(200, 200, 200, 70, "Start Game",
                       Style(background_color=Color(102, 178, 255),
                             border_width=0.005, border_color=Color(255, 255, 255),
                             font_size=header_font_size, font="Arial Bold"))


settingsButton = UIButton(200, 100, 200, 70, "Settings",
                          Style(background_color=Color(255, 153, 51),
                                border_color=Color(255, 255, 255), border_width=0.005,
                                font_size=header_font_size, font="Arial Bold"))

mainMenuBG = UIImage(0, 0, 600, 700, "tetris_bg.jpg")
# ---------------------------------------------------------------------------------------------


# -----------------------------Settings Menu Scene (Components)--------------------------------
settingsMenuBackground = UIImage(0, 0, 600, 700, "tetris_bg.jpg")

backToMainMenuButton = UIButton(15, 635, 100, 50, "<<< Back",
                                Style(font_size=content_font_size))

settingsConfirmButton = UIButton(485, 635, 100, 50, "Confirm",
                                 Style(foreground_color=StdDraw.DARK_GREEN, font_size=content_font_size))

settingsMenuLabel = UITextBox(130, 635, 340, 50, "SETTINGS",
                              Style(background_color=StdDraw.WHITE,
                                    font_size=header_font_size, font="Arial Bold"))

grid_width_label = UITextBox(250, 485, 100, 20, "Grid Width"
                             , Style(background_color=Color(200, 200, 200)))
grid_width_decrement = UIButton(185, 440, 50, 50, "-", Style(font_size=30))
grid_width_display = UITextBox(250, 425, 100, 60, "12", Style(font_size=30))
grid_width_increment = UIButton(365, 440, 50, 50, "+", Style(font_size=30))

grid_height_label = UITextBox(250, 375, 100, 20, "Grid Height"
                              , Style(background_color=Color(200, 200, 200)))
grid_height_decrement = UIButton(185, 330, 50, 50, "-", Style(font_size=30))
grid_height_display = UITextBox(250, 315, 100, 60, "20", Style(font_size=30))
grid_height_increment = UIButton(365, 330, 50, 50, "+", Style(font_size=30))

difficulty_bg = UIBlock(120, 135, 360, 145,
                        Style(background_color=Color(150, 150, 150)))
difficulty_label = UITextBox(135, 215, 330, 50, "Difficulty")
difficultySelector_easy = UIButton(135, 150, 100, 50, "Slow",
                                   Style(font_size=30, foreground_color=StdDraw.GREEN,
                                         background_color=StdDraw.BLACK, border_color=StdDraw.YELLOW))
difficultySelector_normal = UIButton(250, 150, 100, 50, "Normal",
                                     Style(font_size=30, foreground_color=Color(200, 200, 200),
                                           background_color=StdDraw.BLACK, border_color=StdDraw.YELLOW,
                                           border_width=0.005))
difficultySelector_hard = UIButton(365, 150, 100, 50, "Fast",
                                   Style(font_size=30, foreground_color=Color(255, 100, 100),
                                         background_color=StdDraw.BLACK, border_color=StdDraw.YELLOW))
# ---------------------------------------------------------------------------------------------


# ------------------------------In-Game Scene (Components)-------------------------------------
score_label = UITextBox(390, 655, 195, 30, "Score:",
                        style=Style(font_size=content_font_size))

score_value = UITextBox(390, 600, 195, 55, "0",
                        Style(foreground_color=StdDraw.DARK_BLUE, font_size=header_font_size,
                              font="Arial Bold"))

tetromino_view = TetrominoView(420, 515, 120, 150)

GridCanvas = GameCanvas(15, 15, 12, 20, EDGE_LENGTH,
                        Style(background_color=Color(182, 150, 129),
                              foreground_color=Color(104, 85, 72),
                              border_color=Color(104, 85, 72), border_width=0.005),
                        tetromino_view, score_value)

next_tetromino_label = UITextBox(390, 550, 195, 40, "Next",
                                 Style(background_color=Color(200, 200, 200)))

next_tetromino_bg = UIBlock(390, 390, 195, 195,
                            Style(background_color=Color(182, 150, 129),
                                  border_color=Color(104, 85, 72), border_width=0.005))

pauseButton = UIButton(390, 255, 195, 125,
                       style=Style(background_color=StdDraw.WHITE, border_color=StdDraw.GRAY))

pauseSymbol = UIImage(438, 265, 64, 64, "pause_play.png", Style(padding=9))

InGameBG = UIImage(0, 0, 600, 700, "tetris_bg.jpg")
# ---------------------------------------------------------------------------------------------


# ------------------------------Game Over Scene (Components)-----------------------------------
end_text = UITextBox(120, 400, 360, 200, "Game Over",
                     Style(font_size=50, background_color=Color(139, 142, 214),
                           border_width=0.005, border_color=StdDraw.WHITE))

bg_pattern = UIImage(0, 0, 600, 700, "tetris_bg.jpg")
# ---------------------------------------------------------------------------------------------


# -----------------------------------Scene Assembly--------------------------------------------
mainMenu = Scene(mainMenuBG, gameLogo, startButton, settingsButton)

settingsMenu = Scene(settingsMenuBackground, settingsMenuLabel,
                     backToMainMenuButton, settingsConfirmButton,
                     grid_width_decrement, grid_width_display, grid_width_increment,
                     grid_height_decrement, grid_height_display, grid_height_increment,
                     grid_height_label, grid_width_label, difficulty_bg,
                     difficultySelector_easy, difficultySelector_normal, difficultySelector_hard,
                     difficulty_label)

gameScene = Scene(InGameBG, GridCanvas, score_label, score_value, pauseButton,
                  pauseSymbol, next_tetromino_bg, next_tetromino_label, tetromino_view,
                  isGame=True)

gameOver = Scene(bg_pattern, end_text)
# ---------------------------------------------------------------------------------------------


# -------------------------Creating The Container For Scenes-----------------------------------
UI = UIContainer(GridCanvas, main=mainMenu, settings=settingsMenu, game=gameScene, end=gameOver)
# ---------------------------------------------------------------------------------------------


# ------------------------------Setting Button Events------------------------------------------


def togglePauseWithEffect():
    GridCanvas.togglePause()
    if GridCanvas.paused:
        pauseButton.style.border_width = 0.03
    else:
        pauseButton.style.border_width = 0


pauseButton.onclick = lambda: togglePauseWithEffect()
startButton.onclick = lambda: UI.set_scene("game")
settingsButton.onclick = lambda: UI.set_scene("settings")
backToMainMenuButton.onclick = lambda: UI.set_scene("main")


def difficultyUpdate(newDiff: str):
    if newDiff in ("EASY", "NORMAL", "HARD"):
        difficultySelector_easy.style.border_width = 0
        difficultySelector_normal.style.border_width = 0
        difficultySelector_hard.style.border_width = 0
        if newDiff == "EASY":
            Settings.update({"DIFFICULTY": "EASY"})
            difficultySelector_easy.style.border_width = 0.005
        elif newDiff == "NORMAL":
            Settings.update({"DIFFICULTY": "Normal"})
            difficultySelector_normal.style.border_width = 0.005
        elif newDiff == "HARD":
            Settings.update({"DIFFICULTY": "HARD"})
            difficultySelector_hard.style.border_width = 0.005


difficultySelector_easy.onclick = lambda: difficultyUpdate("EASY")
difficultySelector_normal.onclick = lambda: difficultyUpdate("NORMAL")
difficultySelector_hard.onclick = lambda: difficultyUpdate("HARD")


def update_settings():
    if GridCanvas.grid_unset:
        return
    GridCanvas.edge_length = Settings.get("EDGE_LENGTH", 30)
    newGW = Settings.get("GRID_WIDTH", 12)
    newGH = Settings.get("GRID_HEIGHT", 20)
    GridCanvas.game_grid.grid_height, GridCanvas.game_grid.grid_width = newGH, newGW
    GridCanvas.game_grid.set_difficulty(Settings.get("DIFFICULTY", "NORMAL"))
    GridCanvas.finalize(GridCanvas.game_grid)
    print("Settings saved successfully")


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


# This method ensures that the UI object is finalized and ready
def get_finalized_UI():
    return UI
