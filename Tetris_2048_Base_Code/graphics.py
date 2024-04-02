from user_interface import UIBlock, Style
import lib.stddraw as StdDraw
# In this file, there are some classes that inherit from
# the UIBlock class, they are used for creating UI elements.


class GameCanvas(UIBlock):
    def __init__(self, x=0, y=0, grid_h=20, grid_w=12, cell_edge=30, style=Style(padding=10)):
        super().__init__(x, y, grid_w*cell_edge, grid_h*cell_edge, style)
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.edge_length = cell_edge

    def draw(self):
        super().draw()  # Draws the background and border
        # TODO: implement game grid drawing here
        pass


class UIButton(UIBlock):
    def __init__(self, x=0, y=0, width=50, height=50, buttonText="", style=Style(), onclick=lambda e: None):
        super().__init__(x, y, width, height, style)
        self.text = buttonText
        self.onclick = onclick

    def check_click(self, mouse_x, mouse_y):
        return self.x < mouse_x < self.x+self.box_width and self.y < mouse_y < self.y + self.box_height

    def draw(self):
        super().draw()
        StdDraw.setFontSize(self.style.font_size)
        StdDraw.setPenColor(self.style.foreground_color)
        StdDraw.text(self.center_x, self.center_y, self.text)
