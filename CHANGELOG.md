# Changelog
## v1.0.0:
* _Added project files_
  * files in base code:
    + Tetris_2048.py
    + game_grid.py
    + tetromino.py
    + tile.py
    + point.py
  * files __not__ in base code:
    + graphics.py
    + animation.py
    + user_interface.py
    + game_settings.py

## v1.0.1:
* _coded a basic GUI library_
* added files:
  * Tetris_2048_init.py
* updated files:
    >* Tetris_2048.py: changed the start() method,
    added example usage of my UI library
    >* user_interface.py: added classes:
    >  * UIContainer: The object that manages all Scene objects
    >  * Scene: UIContainer can only show one scene at a time.
    >  * Style: an adapter object that standardizes styling
    >  * UIBlock: a component of the UI, an element
    >* graphics.py: added classes:
    >  * GameCanvas: represents the UI part of the game grid
    >  * UIButton: A button template to customize the UI.
