"""
This is the screen inside which the game runs.
It handles the game loop, positioning of sprites and so on.
"""


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, ListProperty
from utils.sprite_handler import SpriteAdder
from kivy.uix.button import Button


Builder.load_file("screens/levelscreen.kv")


class LevelScreen(Screen, SpriteAdder):
    """
    The Screen class for the ongoing level.

    This class contains a FloatLayout in which all the sprites are positioned.
    The sprite positions are stored in a relative manner so that all window
    sizes can be supported.
    The postions are stored relative to height of the wondow.

    Only the sprites within the range 5 times window.height in front and 
    4 times window.height behind are present.
    The sprites that go behind 4 screens are destroyed.
    """

    mainlayout: FloatLayout = ObjectProperty(None)
    relative_screen_position = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from kivy.app import App
        self.app = App.get_running_app()
        self.settings = self.app.settings  # get the settings and keep a reference
        self.removed = False
        self.dynamic_sprites = list()
        self.static_sprites = list()
        
        self.mario = None
        self.paused = True
        self.right_most_sprite = None
        self.level = None
        self.update_list = []
        # self.start_position = [0, 0]

        self.images = {}

    def load(self, level):
        """
        level: The level no. to load
                The level numbers starting with P will be predefined.
                And the level numbers starting with U will be user defined.
        _______________________________________________________

        This method should be called before entering the screen
        It loads the level info for the level description file.
        Then it creates the necessary sprites.
        """

        """
        # Just a test
        from widgets.objects import Ground
        ground1 = Ground()
        ground1.relative_position = [0, 0]
        ground1.size_hint = None, None
        ground1.relative_height = .1
        ground1.relative_width = 1
        self.mainlayout.add_widget(ground1)
        self.static_sprites.append(ground1)

        ground2 = Ground()
        ground2.relative_position = [0, .1]
        ground2.size_hint = None, None
        ground2.relative_height = .1
        ground2.relative_width = .1
        self.mainlayout.add_widget(ground2)
        self.static_sprites.append(ground2)

        ground3 = Ground()
        ground3.relative_position = [.9, .1]
        ground3.size_hint = None, None
        ground3.relative_height = .1
        ground3.relative_width = .1
        self.mainlayout.add_widget(ground3)
        self.static_sprites.append(ground3)

        from widgets.walker import Goomba
        goomba1 = Goomba()
        goomba1.relative_position = [.1, .1]
        self.mainlayout.add_widget(goomba1)
        self.dynamic_sprites.append(goomba1)

        goomba2 = Goomba()
        goomba2.relative_position = [.8, .1]

        goomba2.relative_velocity[0] *= -1
        goomba1.pos = goomba1.position
        goomba2.pos = goomba2.position

        from widgets.mario import Mario
        mario = Mario()
        self.mario = mario
        self.mainlayout.add_widget(mario)
        mario.relative_position = [ground1.relative_position[0] + mario.relative_height*2,
                                   ground1.relative_position[1] + ground1.relative_height]
        self.dynamic_sprites.append(mario)

        self.mainlayout.add_widget(goomba2)
        self.dynamic_sprites.append(goomba2)
        """

        self.level = level

        import json
        f = open(f"{level}")
        level_data = json.load(f)
        self.add_all(level_data)
        # print(self.dynamic_sprites)
        # print(self.static_sprites)

        self.load_images()

    def load_images(self, path="assets/images"):
        """
        This method's name is a bit misguiding.
        The images are to be loaded only for their sizes.
        The dictionary self.images will be updated with the sizes.
        """

        import os
        from PIL import Image
        images_path = os.listdir(path)
        img_formats = ["png", "jpg", "jpeg", "gif"]

        for i in images_path:
            real_path = os.path.realpath(path + "/" + i)
            if os.path.isdir(real_path):
                self.load_images(path+"/"+i)
            else:
                if i.split(".")[-1] not in img_formats:
                    continue
                self.images[path+"/"+i] = Image.open(path+"/"+i).size

    def exit(self, btn):
        """
        Removes this class from the ScreenManager and exits.
        """
        self.removed = True
        manager = self.manager
        manager.transition.direction = "right"

        self.dynamic_sprites.clear()
        self.static_sprites.clear()

        for child in self.mainlayout.children:
            self.mainlayout.remove_widget(child)
        for child in self.children:
            self.remove_widget(child)

        manager.remove_widget(self)

    def on_enter(self):
        """
        Start the game loop as soon as the current screen is shown on
        the window.
        """
        self.run_loop()

    def run_loop(self):
        """
        Run the loop using the Clock API of kivy
        """
        self.paused = False
        from kivy.clock import Clock
        self.interval = Clock.schedule_interval(self.update, .01)

    def update_position(self):
        for i in self.dynamic_sprites + self.static_sprites + self.update_list:
            i.relative_screen_position = self.relative_screen_position

    def end(self):
        self.interval.cancel()
        restart_btn = Button(text="Restart", on_release=self.restart)
        exit_btn = Button(text="Exit", on_release=self.exit)
        restart_btn.size_hint = (0.1, 0.05)
        exit_btn.size_hint = (0.1, 0.05)
        restart_btn.pos_hint = {"x": 0.3, "y": 0.475}
        exit_btn.pos_hint = {"x": 0.6, "y": 0.475}
        self.mainlayout.add_widget(restart_btn)
        self.mainlayout.add_widget(exit_btn)
        self.paused = True
    
    def restart(self, btn):
        manager = self.manager
        self.exit(btn)
        manager.current_screen.play(btn)

    def pause(self):
        self.paused = True
        self.interval.cancel()
        self.resume_btn = Button(text="Resume", on_release=self.resume)
        self.restart_btn = Button(text="Restart", on_release=self.restart)
        self.exit_btn = Button(text="Exit", on_release=self.exit)

        self.resume_btn.size_hint = (0.1, 0.05)
        self.restart_btn.size_hint = (0.1, 0.05)
        self.exit_btn.size_hint = (0.1, 0.05)

        self.resume_btn.pos_hint = {"x": 0.2, "y": 0.475}
        self.restart_btn.pos_hint = {"x": 0.5, "y": 0.475}
        self.exit_btn.pos_hint = {"x": 0.7, "y": 0.475}

        self.mainlayout.add_widget(self.resume_btn)
        self.mainlayout.add_widget(self.restart_btn)
        self.mainlayout.add_widget(self.exit_btn)

    def resume(self, btn):
        self.mainlayout.remove_widget(self.resume_btn)
        self.mainlayout.remove_widget(self.restart_btn)
        self.mainlayout.remove_widget(self.exit_btn)
        self.run_loop()

    def update(self, dt):
        """
        dt: Time between previous and current frame.
        ______________________________________________

        The game loop starts here and the control goes to all the sprites 
        in an asynchronous way.
        """
        # for i in self.static_sprites:
        #     i.update(self, dt)

        try:
            for sprite in self.dynamic_sprites + self.update_list:
                sprite.update(self, dt)
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()

    def remove_sprite(self, sprite):
        self.remove_widget(sprite)
        if sprite.is_dynamic():
            self.dynamic_sprites.remove(sprite)
        else:
            self.static_sprites.remove(sprite)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        """
        keyboard: The physical or virtual keyboard object
        keycode: The KeyCode of the pressed key
        text: The character representation of the pressed key.
        modifiers: modifiers (shiftt, ctrl, etc.) pressed along with the key
        _____________________________________________________________________

        Handle the key down event.
        """

        if keycode == 41:   # Escape key
            if not self.paused:
                self.pause()
            return
        if self.mario is not None:
            self.mario.on_key_down(keyboard, keycode, text, modifiers)

    def on_key_up(self, keyboard, keycode):
        """
        keyboard: The physical or virtual keyboard object
        keycode: The KeyCode of the pressed key
        __________________________________________________

        Handle the key up event.
        """

        if self.mario is not None:
            self.mario.on_key_up(keyboard, keycode)

    def on_leave(self, *args):
        """
        Cancel the clock interval when leaving the screen otherwise
        there  may be errors.
        """
        if not self.removed:
            self.interval.cancel()

    # def on_touch_down(self, touch):
    #     if self.paused:
    #         self.resume()
    #     else:
    #         self.pause()

    def __del__(self):
        print("lvl screen deleted")

    def win_size_changed(self, win_sdl, size):
        pass
