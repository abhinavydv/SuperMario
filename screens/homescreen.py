"""
The first screen that appears when the app is opened.
"""


from os import name
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from screens.levelscreen import LevelScreen


Builder.load_file("screens/homescreen.kv")


class HomeScreen(Screen):
    """
    The screen class that defines the look and feel of the homescreen.

    The screen wil have following options.
    -> Play (Level **): Start the highest level reached by the user.
    -> Load Game : Strat a previously saved game.
    -> Levels : Choose from a list of levels that have been  unlocked.
                The screen that is shown will contain two tabs.
                -> User defined levels : Levels created by the user.
                -> Predefined Levels : Levels shipped with the game.
    -> Settings : The related settings for the game.
    """

    def play(self, btn):
        """
        Create a levelscreen, load the level, and display the screen.
        """

        lvl_screen = LevelScreen()
        self.manager.add_widget(lvl_screen)
        lvl_screen.load("levels/level1.json")
        self.manager.transition.direction = "left"
        self.manager.current = "LevelScreen"

    def load_game(self, btn):
        pass

    def levels(self, btn):
        pass

    def settings(self, btn):
        pass

    def on_key_down(self, keyboard, keycode, text, modifiers):
        pass

    def on_key_up(self, keyboard, keycode):
        pass

    def win_size_changed(self, win_sdl, size):
        pass

