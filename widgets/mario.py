"""
Mario (Our Hero) is here to save everyone...  Ta da...
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from widgets.walker import Walker
from time import time


class Mario(Walker):
    """
    Definition of Mario in the game.
    This class contains specifications of mario.
    It contains methods that move him and detect collisions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = "assets/mario/Mario_Small_Right_Still.png"
        self.relative_height = .1
        self.relative_width = .05

        self.tag = "mario"
        self.max_relative_velocity = [.15, .4]

        self.standing = True
        self.is_invincible = False
        self.small = True
        self.has_fire = False
        self.min_time = 0.5
        self.t = time()

        self.direction = "_Right"    # _Right or _Left
        self.state = "_Still"   # _Walk, _Jump, _Still or _Crouch
        self.dimension = "_Small"   #  _Big or _Small (Size)
        self.power = ""  # Blank string or _Fire
        
    def get_added_to_screen(self, levelscreen):
        super().get_added_to_screen(levelscreen)

        levelscreen.mario = self

    def on_collide(self, other, col):
        if other.tag == "powerup":
            return
        if col[2] == "right":
            if not other.is_static:
                self.relative_velocity[0] = 0

        elif col[2] == "left":
            if not other.is_static:
                self.relative_velocity[0] = 0

        elif col[2] == "top":
            self.relative_velocity[1] = 0
            if self.jumping:
                self.jump2()

        elif col[2] == "bottom":
            self.relative_velocity[1] *= -1

        if other.is_static:
            other.move_aside(self, col)

    def move(self, levelscreen, dt):
        # if self.position[0] > Window.height/2:
        # levelscreen.relative_screen_position[0] += (self.position[0]/Window.height - 0.5)
        # levelscreen.update_position()
        # self.relative_position[0] = self.relative_screen_position[0] + 0.5

        relative_half = Window.width / Window.height / 2
        if self.position[0] > Window.width/2 and levelscreen.right_most_sprite.right > Window.width:
            levelscreen.relative_screen_position[0] += (
                self.position[0]-Window.width/2)/Window.height
            levelscreen.update_position()
            self.relative_position[0] = self.relative_screen_position[0] + relative_half

        if levelscreen.right_most_sprite.right < Window.width:
            levelscreen.relative_screen_position[0] -= (
                Window.width-levelscreen.right_most_sprite.right)/Window.height
            levelscreen.update_position()

        if self.relative_position[0] < self.relative_screen_position[0]:
            self.relative_position[0] = self.relative_screen_position[0]

        super().move(levelscreen, dt)

    def sit(self):
        self.standing = False

        self.relative_height = self.relative_width * 4/3
        self.image = "assets/mario/Mario_Big_Crouch_Right.png"

    def stand(self):
        self.standing = True
        self.relative_height = self.relative_width * 2
        self.image = "assets/mario/Mario_Big_Right_Still.png"

    def fireball(self):
        if self.has_fire:
            if time() - self.t > self.min_time:
                self.t = time()
                levelscreen = self.parent.parent
                content = levelscreen.sprites["FireBall"]
                content["name"] = "FireBall"
                content["relative_position"] = list(self.relative_position)
                content["relative_position"][0] += self.relative_width
                content["relative_position"][1] += self.relative_height
                content["relative_screen_position"] = self.relative_screen_position
                content["relative_velocity"][0] = content["max_relative_velocity"][0]

                if self.direction == "_Left":
                    content["relative_position"][0] -= 2*self.relative_width
                    content["relative_velocity"][0] = -content["max_relative_velocity"][0]

                levelscreen.add_one(content)

    def grow(self):
        if self.small:
            self.small = False
            self.image = "assets/mario/Mario_Big_Right_Still.png"
            print(type(self.image))
            self.relative_width = 0.05
            self.relative_height = 0.1

    def be_invincible(self):
        self.is_invincible = True

    def get_fire(self):
        self.has_fire = True

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode == 79:  # Right Arrow key
            self.relative_velocity[0] = self.max_relative_velocity[0]
            self.direction = "_Right"
            if self.small:
                self.image = "assets/mario/Mario_Small_Right_Still.png"
            else:
                self.image = "assets/mario/Mario_Big_Right_Still.png"

        elif keycode == 80:  # Left Arrow key
            self.relative_velocity[0] = -self.max_relative_velocity[0]
            self.direction = "_Left"
            if self.small:
                self.image = "assets/mario/Mario_Small_Left_Still.png"
            else:
                self.image = "assets/mario/Mario_Big_Left_Still.png"

        # elif keycode == 81:  # Down Arrow Key
        #     if self.standing:
        #         self.sit()

        # elif keycode == 82:  # Up Arrow Key
        #     if not self.standing:
        #         self.stand()

        elif keycode == 44:  # Space Bar
            self.jumping = True

        elif keycode == 40:  # Enter Key
            self.fireball()

    def on_key_up(self, keyboard, keycode):
        if keycode == 79 or keycode == 80:  # Right and left Arrow keys respectively
            self.relative_velocity[0] = 0

        if keycode == 44:  # Space bar
            self.jumping = False

    def die(self):
        if self.small:
            self.parent.parent.end()

        else:
            self.small = True
            self.relative_height = 0.06
            self.relative_width = 0.04
            if self.direction == "right":
                self.image = "assets/mario/Mario_Small_Right_Still.png"
            else:
                self.image = "assets/mario/Mario_Small_Left_Still.png"

            self.invisible = True
            
            from kivy.clock import Clock
            self.blink_interval = Clock.schedule_interval(self.blink, 0.5)
            Clock.schedule_once(self.stop_blink, 5)

    def blink(self, dt):
        if self.opacity == 1:
            self.opacity = 0.5
        else:
            self.opacity = 1

    def stop_blink(self, dt):
        self.blink_interval.cancel()
        self.opacity = 1
        self.invisible = False
