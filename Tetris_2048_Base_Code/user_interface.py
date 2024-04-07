import lib.stddraw as StdDraw  # for drawing methods it provides


class Scene:
    # To be clear, in this context, "actor" means any object that has a noticeable presence in the scene
    def __init__(self, *actors, isGame=False):
        self.is_game_scene = isGame
        self.actors: list[UIBlock] = list(actors)
        self.paused = True  # scenes are paused by default, to prevent unexpected behavior

    def draw_scene_effects(self):  # use this method if different scenes have different effects.
        pass

    def draw(self):
        if not self.paused:
            for actor in self.actors:
                actor.draw()
            self.draw_scene_effects()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def update(self, keyEvents, mouseEvent, deltaTime=1):
        if not self.paused:
            for actor in self.actors:
                if actor.listens_to_key_events:
                    actor.onKeyInput(keyEvents)
                if actor.listens_to_mouse_events:
                    actor.onMouseInput(mouseEvent)
                actor.update(deltaTime)


# an object that contains the entire UI
class UIContainer:
    def __init__(self, canvas, **scenes):
        self.tetromino = canvas.tetromino
        self.canvas: GameCanvas = canvas
        self.scenes = scenes
        self.current_scene = scenes.get("main", Scene(canvas))
        self.in_game = False

        # A very, very complex way to calculate window width with fit-content logic
        # In summary, it loops through every container to reach UIBlock objects.
        # then, It takes the useful instance attribute (x,y,width,height) and calculates max appropriately
        # min values are not needed as they should always be 0 (zero)
        if scenes is not None:
            scene_max_x = max([max([actor.x + actor.width
                                    for actor in scene_obj.actors])
                               for scene_obj in self.scenes.values()])
            scene_max_y = max([max([actor.y + actor.height
                                    for actor in scene_obj.actors])
                               for scene_obj in self.scenes.values()])
            self.window_width = scene_max_x
            self.window_height = scene_max_y
        else:
            self.window_width = self.canvas.width
            self.window_height = self.canvas.height

    def addScenes(self, **scenes):
        self.scenes.update(scenes)

        scene_max_x = max([max([actor.x + actor.width
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        scene_max_y = max([max([actor.y + actor.height
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        self.window_width = scene_max_x
        self.window_height = scene_max_y

    def getGridSizes(self):
        return self.canvas.grid_w, self.canvas.grid_h

    def getWindowSize(self):
        return self.window_width, self.window_height

    def load_scene(self, scene: Scene):
        self.current_scene = scene
        self.in_game = scene.is_game_scene
        self.current_scene.unpause()

    def set_scene(self, identifier="main"):
        if self.scenes.get(identifier, None) is not None:
            if self.current_scene is not None:
                self.current_scene.pause()
            self.load_scene(self.scenes.get(identifier))
            return True
        return False

    def draw(self, key_events, mouse_events, delta_time=1):  # call this method each frame
        # If a scene is loaded:
        if self.current_scene is not None:
            self.current_scene.update(key_events, mouse_events, delta_time)

            # draw the frame AFTER updating, to show the user the latest state of the program
            self.current_scene.draw()

    def launch(self, starting_scene_name="main"):
        if self.set_scene(starting_scene_name):
            StdDraw.setCanvasSize(self.window_width, self.window_height)
            StdDraw.setXscale(0, self.window_width)
            StdDraw.setYscale(0, self.window_height)
        else:
            print("Error: Couldn't find starting scene, launch cancelled")

    def reset(self):
        pass

    def askPlayAgain(self):
        return False


class Style:
    # Maintain this syntax for the keyword arguments:
    # * all lowercase characters
    # * multiple words separated by an underscore
    # * no whitespace and no numbers
    def __init__(self, **kwargs):
        self.background_color = kwargs.get("background_color", StdDraw.WHITE)
        self.foreground_color = kwargs.get("foreground_color", StdDraw.BLACK)
        self.border_color = kwargs.get("border_color", StdDraw.BLACK)
        self.border_width = kwargs.get("border_width", 0)
        self.padding = kwargs.get("padding", 0)
        self.font_size = kwargs.get("font_size", 16)


# superclass for all UI elements, including the game grid
class UIBlock:
    # The idea is having a "fit-content" approach to window sizing
    # Every instance of a subclass should invoke the resize() method
    # and that method should update the window size.

    def __init__(self, x, y, box_width, box_height, style=Style(), isAnimated=False):
        self.x = x if x > 0 else 0
        self.y = y if y > 0 else 0
        self.box_width = box_width if box_width > 0 else 0
        self.box_height = box_height if box_height > 0 else 0
        self.width = box_width + 2 * style.padding if box_width + 2 * style.padding > 0 else 0
        self.height = box_height + 2 * style.padding if box_height + 2 * style.padding > 0 else 0
        self.style = style if isinstance(style, Style) else Style()
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2
        self.is_animated = isAnimated
        self.listens_to_key_events = False
        self.listens_to_mouse_events = False

    def draw(self):
        # Drawing the background
        StdDraw.setPenColor(self.style.background_color)
        StdDraw.filledRectangle(self.x+self.style.padding, self.y+self.style.padding, self.box_width, self.box_height)

        # Drawing the border
        if self.style.border_width > 0:
            StdDraw.setPenRadius(self.style.border_width)
            StdDraw.setPenColor(self.style.border_color)
            StdDraw.rectangle(self.x+self.style.padding, self.y+self.style.padding, self.box_width, self.box_height)

        # Drawing the contents (implemented by subclasses)

    def update(self, delta_time):  # Implement animations for appropriate classes
        pass

    def onKeyInput(self, events):
        pass

    def onMouseInput(self, mouseEvent):
        pass


class GameCanvas(UIBlock):
    def __init__(self, x=0, y=0, grid_w=20, grid_h=12, cell_edge=30, style=Style(padding=10)):
        super().__init__(x, y, grid_w*cell_edge, grid_h*cell_edge, style)
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.edge_length = cell_edge
        self.listens_to_key_events = True
        self.grid_unset = True
        self.game_grid = None
        self.tetromino = None

    def finalize(self, grid):
        self.game_grid = grid
        self.tetromino = self.game_grid.current_tetromino
        self.grid_unset = False

    def draw(self):
        super().draw()  # Draws the background and border
        if not self.grid_unset:
            self.game_grid.current_tetromino.draw()

            for row in range(len(self.game_grid.tile_matrix)):
                for col in range(len(self.game_grid.tile_matrix[row])):
                    t = self.game_grid.tile_matrix[row][col]
                    if t is not None:
                        t.draw(row, col)

    def update(self, delta_time):
        if self.tetromino is not None:
            self.game_grid.current_tetromino.animation_update(delta_time)

    def on_tetromino_change(self):
        self.tetromino = self.game_grid.current_tetromino

    def onKeyInput(self, events=()):
        if not self.grid_unset:
            for event in events:
                if event.key == "up" or event.key == "w":
                    self.game_grid.rotate()
                elif event.key == "left" or event.key == "a":
                    self.game_grid.move_LEFT()
                elif event.key == "right" or event.key == "d":
                    self.game_grid.move_RIGHT()
                elif event.key == "down" or event.key == "s":
                    self.game_grid.move_DOWN()
                elif event.key == "space":
                    # implement hard fall here
                    pass


class UIButton(UIBlock):
    def __init__(self, x=0, y=0, width=50, height=50, buttonText="", style=Style(), onclick=lambda: None):
        super().__init__(x, y, width, height, style)
        self.text = buttonText
        self.onclick = onclick
        self.listens_to_mouse_events = True

    def check_click(self, mouse_x, mouse_y):
        return (self.x+self.style.padding < mouse_x < self.x+self.style.padding+self.box_width
                and self.y+self.style.padding < mouse_y < self.y+self.style.padding+self.box_height)

    def draw(self):
        super().draw()
        StdDraw.setFontSize(self.style.font_size)
        StdDraw.setPenColor(self.style.foreground_color)
        StdDraw.text(self.center_x, self.center_y, self.text)

    def onMouseInput(self, mouseEvent):
        if mouseEvent is not None:
            if mouseEvent.isClicked and self.check_click(mouseEvent.x, mouseEvent.y):
                self.onclick()


class UITextBox(UIBlock):
    def __init__(self, x, y, width, height, text="", style=Style(padding=10)):
        super().__init__(x, y, width, height, style)
        self.text = text

    def draw(self):
        super().draw()
        StdDraw.setFontSize(self.style.font_size)
        StdDraw.setPenColor(self.style.foreground_color)
        StdDraw.text(self.center_x, self.center_y, self.text)