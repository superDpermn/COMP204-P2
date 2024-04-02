# TODO: Implement UI and canvas logic here
from Tetris_2048_Base_Code.lib.color import Color  # for styling purposes
import lib.stddraw as StdDraw  # for drawing methods it provides


class Scene:
    def __init__(self, *actors):
        self.actors = list(actors)
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

    def update(self, deltaTime=1):
        if not self.paused:
            for actor in self.actors:
                actor.update(deltaTime)


# an object that contains the entire UI
class UIContainer:
    def __init__(self, canvas, **scenes):
        self.canvas = canvas
        self.scenes = scenes
        self.current_scene = None

        # A very, very complex way to calculate window width with fit-content logic
        # In summary, it loops through every container to reach UIBlock objects.
        # then, It takes the useful instance attribute (x,y,width,height) and calculates min/max appropriately
        scene_min_x = min([min([actor.x
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        scene_max_x = max([max([actor.x + actor.width
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        scene_min_y = min([min([actor.y
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        scene_max_y = max([max([actor.y + actor.height
                                for actor in scene_obj.actors])
                           for scene_obj in self.scenes.values()])
        # these values are not stored as they won't be used after the initial calculation
        self.window_width = scene_max_x - scene_min_x
        self.window_height = scene_max_y - scene_min_y

    def addScenes(self, **scenes):
        self.scenes.update(scenes)

    def getGridSizes(self):
        return self.canvas.grid_w, self.canvas.grid_h

    def getWindowSize(self):
        return self.window_width, self.window_height

    def load_scene(self, scene: Scene):
        self.current_scene = scene
        self.current_scene.unpause()

    def set_scene(self, identifier="main"):
        if self.scenes.get(identifier, None) is not None:
            if self.current_scene is not None:
                self.current_scene.pause()
            self.load_scene(self.scenes.get(identifier))
            return True
        return False

    def draw(self, delta_time):  # call this method each frame
        if self.current_scene is not None:
            self.current_scene.update(delta_time)
            self.current_scene.draw()

    def launch(self, starting_scene_name="main"):
        if self.set_scene(starting_scene_name):
            StdDraw.setCanvasSize(self.window_width, self.window_height)
        else:
            print("Error: Couldn't find starting scene, launch cancelled")


class Style:
    # Maintain this syntax for the keyword arguments:
    # * all lowercase characters
    # * multiple words separated by an underscore
    # * no whitespace
    def __init__(self, **kwargs):
        self.background_color = kwargs.get("background_color", Color(255, 255, 255))
        self.foreground_color = kwargs.get("foreground_color", Color(0, 0, 0))
        self.border_color = kwargs.get("border_color", Color())
        self.border_width = kwargs.get("border_width", 0)
        self.padding = kwargs.get("padding", 0)
        self.font_size = kwargs.get("font_size", 16)


# superclass for all UI elements, including the game grid
class UIBlock:
    # The idea is having a "fit-content" approach to window sizing
    # Every instance of a subclass should invoke the resize() method
    # and that method should update the window size.

    def __init__(self, x, y, box_width, box_height, style=Style(), isAnimated=False):
        self.x = x
        self.y = y
        self.box_width = box_width
        self.box_height = box_height
        self.width = box_width + 2 * style.padding
        self.height = box_height + 2 * style.padding
        self.style = Style()
        self.center_x = self.x + self.style.padding + self.box_width / 2
        self.center_y = self.y + self.style.padding + self.box_height / 2
        self.is_animated = isAnimated

    def draw(self):
        # Drawing the background
        StdDraw.setPenColor(self.style.background_color)
        StdDraw.filledRectangle(self.center_x, self.center_y, self.box_width, self.box_height)
        StdDraw.setPenColor(self.style.border_color)

        # Drawing the border
        StdDraw.setPenRadius(self.style.border_width)
        StdDraw.rectangle(self.center_x, self.center_y, self.box_width, self.box_height)

        # Drawing the contents (overridden by subclasses)

    def update(self, delta_time):  # Implement animations for appropriate classes
        pass
