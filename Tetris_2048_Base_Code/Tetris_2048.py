################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
from Tetris2048_init import UI


# The main function where this program starts execution
def start():
    gridSizes = UI.getGridSizes()
    # set the game grid dimension values stored and used in the Tetromino class
    Tetromino.grid_width, Tetromino.grid_height = gridSizes

    # create the game grid
    # TODO: modify GameGrid class, following the guidelines. It should be the central container for game data.

    grid = GameGrid(gridSizes[1], gridSizes[0])  # reverse order on purpose
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino

    # sets the current scene to be the starting window
    UI.set_scene("main")

    # creates the program window
    UI.launch()

    # the main game loop
    while True:

        UI.draw()
        stddraw.show(17)  # 17ms frame gap ~= 59 frames/second

        break  # to remove the annoying IDE warning temporarily

        # if grid.is_game_over():  # when the game is over
        #     UI.set_scene("end")
        #     UI.draw()
        #     stddraw.show()
        #     break
        # TODO: Implement the game functionality in a cleaner way than below
        # # check for any user interaction via the keyboard
        # if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
        #     key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
        #     # if the left arrow key has been pressed
        #     if key_typed == "left":
        #         # move the active tetromino left by one
        #         current_tetromino.move(key_typed, grid)
        #     # if the right arrow key has been pressed
        #     elif key_typed == "right":
        #         # move the active tetromino right by one
        #         current_tetromino.move(key_typed, grid)
        #     # if the down arrow key has been pressed
        #     elif key_typed == "down":
        #         # move the active tetromino down by one
        #         # (soft drop: causes the tetromino to fall down faster)
        #         current_tetromino.move(key_typed, grid)
        #     # clear the queue of the pressed keys for a smoother interaction
        #     stddraw.clearKeysTyped()
        #
        # # move the active tetromino down by one at each iteration (auto fall)
        # success = current_tetromino.move("down", grid)
        # # lock the active tetromino onto the grid when it cannot go down anymore
        # if not success:
        #     # get the tile matrix of the tetromino without empty rows and columns
        #     # and the position of the bottom left cell in this matrix
        #     tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
        #     # update the game grid by locking the tiles of the landed tetromino
        #     game_over = grid.update_grid(tiles, pos)
        #     # end the main game loop if the game is over
        #     if game_over:
        #         break
        #     # create the next tetromino to enter the game grid
        #     # by using the create_tetromino function defined below
        #     current_tetromino = create_tetromino()
        #     grid.current_tetromino = current_tetromino
        #
        # # display the game grid with the current tetromino
        # grid.display()

    # on program end
    print("Thanks for playing!")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # the dimensions for the start game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # add the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # the user interaction loop for the simple menu
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the start game button
        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
