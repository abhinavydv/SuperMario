from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty


Builder.load_file("utils/controls.kv")


class CanvasButton(Button):
    """
    The button visible on the window at fixed position.
    """

    relative_width = NumericProperty(0)
    relative_height = NumericProperty(0)

    def __init__(self, relative_width=0, relative_height=0, **kwargs):
        super().__init__(**kwargs)

        self.relative_width = relative_width
        self.relative_height = relative_height
        self.opacity = 0.4

class AndroidControls(object):

    def __init__(self):
        super().__init__()

        self.mario = None
        self.buttons = {}

    def turn_on(self, mario, levelscreen):
        self.mario = mario

        #Left Button
        left_btn = CanvasButton(0.1, 0.05, pos_hint={"x": 0.1, "y": 0.1}, on_press=lambda btn: mario.left_down(), 
            on_release=lambda btn: mario.left_up(), text="<<")
        self.buttons["left_button"] = left_btn

        #Right Button
        right_btn = CanvasButton(0.1, 0.05, pos_hint={"x": 0.2, "y": 0.1}, on_press=lambda btn: mario.right_down(),
            on_release=lambda btn: mario.right_up(), text=">>")
        self.buttons["right_button"] = right_btn

        # Jump Button
        jump_btn = CanvasButton(0.1, 0.05, pos_hint={"x": 0.8, "y": 0.1}, on_press=lambda btn: mario.space_down(), 
            on_release=lambda btn: mario.space_up(), text="^")
        self.buttons["jump_button"] = jump_btn

        # Fire Button
        fire_btn = CanvasButton(0.1, 0.05, pos_hint={"x": 0.8, "y": 0.3}, on_press=lambda btn: mario.enter_down(),
            text="O")
        self.buttons["fire_button"] = fire_btn

        # Add the buttons to screen
        for i in self.buttons:
            btn = self.buttons[i]
            levelscreen.mainlayout.add_widget(btn)
