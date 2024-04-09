import lib.stddraw as StdDraw


class InputEvent:
    def __init__(self):
        pass


class MouseEvent(InputEvent):
    def __init__(self, x, y, isClicked=False):
        super().__init__()
        self.x = x
        self.y = y
        self.isClicked = isClicked


class KeyboardEvent(InputEvent):
    def __init__(self, keycode, isPressed=False):
        super().__init__()
        self.key = keycode
        self.pressed = isPressed

    def __str__(self):
        return self.key+", pressed: "+str(self.pressed)


class InputController:
    def __init__(self):
        self.mouseEvent = MouseEvent(0, 0, False)
        self.mouse_x: float = 0
        self.mouse_y: float = 0
        self.lastMouseFrame = False
        self.mousePressedAtLeastOnce = False
        self.pressed_keycodes = set()

    def update(self):
        self.pressed_keycodes.clear()
        while StdDraw.hasNextKeyTyped():
            self.pressed_keycodes.add(StdDraw.nextKeyTyped())

        # if mouse pressed or mouse moved (ignore mouse release)
        mp = StdDraw.mousePressed()
        if mp:
            self.mousePressedAtLeastOnce = True

        # Apparently, mouse position can't be determined by StdDraw
        # if there hasn't been any clicks yet.
        if not self.mousePressedAtLeastOnce:
            return

        newMouseX, newMouseY = StdDraw.mouseX(), StdDraw.mouseY()

        if (not self.lastMouseFrame) and mp:
            self.mouseEvent = MouseEvent(newMouseX, newMouseY, True)
        else:
            self.mouseEvent = MouseEvent(newMouseX, newMouseY, False)
        self.lastMouseFrame = mp
        self.mouse_x, self.mouse_y = newMouseX, newMouseY

    def getKeyEvents(self):
        # Return the key presses
        return tuple([KeyboardEvent(key, True) for key in self.pressed_keycodes])
