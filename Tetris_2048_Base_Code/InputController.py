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
        return self.key+", pressed: "+self.pressed


class InputController:
    def __init__(self):
        self.pressed_keys = set()  # Set to store currently pressed keys
        self.previous_keys = set()  # Set to store previously pressed keys

        self.mouseEvent = MouseEvent(0, 0, False)
        self.mouse_x: float = 0
        self.mouse_y: float = 0
        self.lastMouseFrame = False
        self.mousePressedAtLeastOnce = False

    def update(self):
        # Clear the set of previously pressed keys
        self.previous_keys.clear()

        # Update the set of previously pressed keys with the current pressed keys
        self.previous_keys.update(self.pressed_keys)

        # Clear the set of currently pressed keys
        self.pressed_keys.clear()

        # Update the set of currently pressed keys based on the keys in the internal queue
        while StdDraw.hasNextKeyTyped():
            key = StdDraw.nextKeyTyped()
            self.pressed_keys.add(key)

        # if mouse pressed or mouse moved (ignore mouse release)
        mp = StdDraw.mousePressed()
        if mp:
            self.mousePressedAtLeastOnce = True

        # Apparently, mouse position can't be determined by StdDraw
        # if there hasn't been any clicks yet.
        if not self.mousePressedAtLeastOnce:
            return

        newMouseX, newMouseY = StdDraw.mouseX(), StdDraw.mouseY()

        if (not (newMouseX, newMouseY) == (self.mouse_x, self.mouse_y)
                or (self.lastMouseFrame and not mp)):
            self.mouseEvent = MouseEvent(newMouseX, newMouseY, mp)
        else:
            self.mouseEvent = None
        self.lastMouseFrame = mp
        self.mouse_x, self.mouse_y = newMouseX, newMouseY

    def getKeyEvents(self):
        # Determine the keys that were pressed since the last update
        keys_pressed = self.pressed_keys - self.previous_keys
        pressedEvents = tuple([KeyboardEvent(e, True) for e in keys_pressed])

        # Determine the keys that were released since the last update
        keys_released = self.previous_keys - self.pressed_keys
        releasedEvents = tuple([KeyboardEvent(e, False) for e in keys_released])

        # Return the key state changes (press/release)
        return pressedEvents, releasedEvents
