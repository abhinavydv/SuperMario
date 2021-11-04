"""
Mario (Our Hero) is here to save everyone...  Ta da...
"""


from kivy.core.window import Window

from widgets.walker import Walker
from time import time
from PIL import Image


class Mario(Walker):
    """
    Definition of Mario in the game.
    This class contains specifications of mario.
    It contains methods that move him and detect collisions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = "assets/images/mario/Mario_Small_Right_Still.png"
        self.relative_height = .1
        self.relative_width = .05

        self.tag = "mario"
        self.max_relative_velocity = [.15, .4]

        self.standing = True
        self.is_invincible = False
        self.invincible_time = 0
        self.max_invincible_time = 20
        self.small = True
        self.has_fire = False
        self.min_time = 0.5
        self.fire_time = time()
        self.animate_time = time()

        self.direction = "_Right"    # _Right or _Left
        self.state = "_Still"   # _Walk, _Jump, _Still or _Crouch
        self.dimension = "_Small"  # _Big or _Small (Size)
        self.power = ""  # <Blank string> or _Fire

        self.dying = False

        self.img_no = 1

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
            elif self.state != "_Walk":
                self.state = "_Still"
                if self.relative_velocity[0] != 0:
                    self.state = "_Walk"

        elif col[2] == "bottom":
            self.relative_velocity[1] *= -1

        if other.is_static:
            other.move_aside(self, col)

    def move(self, levelscreen, dt):
        # if self.position[0] > Window.height/2:
        # levelscreen.relative_screen_position[0] += (self.position[0]/Window.height - 0.5)
        # levelscreen.update_position()
        # self.relative_position[0] = self.relative_screen_position[0] + 0.5

        if self.is_invincible:
            self.invincible_time += dt
            if self.invincible_time > self.max_invincible_time:
                self.is_invincible = False

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
        self.relative_height = self.relative_width * 4/3
        self.state = "_Crouch"

    def stand(self):
        self.standing = True
        self.relative_height = self.relative_width * 2
        if self.state != "_Jump":
            self.state = "_Still"

    def fireball(self):
        if self.has_fire:
            if time() - self.fire_time > self.min_time:
                self.fire_time = time()
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
                    content["relative_velocity"][0] = - \
                        content["max_relative_velocity"][0]

                levelscreen.add_one(content)

    def jump2(self, multiplier=1):
        self.state = "_Jump"
        super().jump2(multiplier)

    def grow(self):
        if self.small:
            self.small = False
            self.dimension = "_Big"
            self.relative_height = 0.1
        else:
            self.get_fire()

    def be_invincible(self):
        self.is_invincible = True
        self.invincible_time = 0

    def get_fire(self):
        if self.small:
            self.grow()
        else:
            self.power = "_Fire"
            self.has_fire = True

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if self.dying:
            return
        if keycode == 79:  # Right Arrow key
            self.relative_velocity[0] = self.max_relative_velocity[0]
            self.direction = "_Right"
            if self.state != "_Jump":
                self.state = "_Walk"

        elif keycode == 80:  # Left Arrow key
            self.relative_velocity[0] = -self.max_relative_velocity[0]
            self.direction = "_Left"
            if self.state != "_Jump":
                self.state = "_Walk"

        # elif keycode == 81:  # Down Arrow Key
        #     self.sit()

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
            if self.state != "_Jump":
                self.state = "_Still"

        # if keycode == 81:   # Down Arrow key
        #     if self.state != "_Jump":
        #         self.state = "_Still"
        #         self.standing = True

        if keycode == 44:  # Space bar
            self.jumping = False

    def die(self):
        if self.dying:
            self.parent.parent.end()
        if self.small:
            self.dying = True
            self.jump2()
            self.collider = False

        else:
            self.small = True
            self.has_fire = False
            self.power = ""
            self.relative_height = 0.06
            self.relative_width = 0.04
            self.dimension = "_Small"

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

    def animate(self, levelscreen, dt):
        images = 2 if self.dimension == "_Big" else 3
        interval = 0.15 if self.dimension == "_Big" else 0.1
        self.animate_time += dt
        if self.animate_time > interval:
            self.animate_time = 0
            self.img_no += 1
            if self.img_no > images:
                self.img_no = 1

        if self.dying:
            image = "assets/images/mario/Mario_Flip.png"
        elif self.state == "_Walk":
            image = f"assets/images/mario/Mario{self.dimension}{self.direction}{self.state}_{self.img_no}{self.power}.png"
        else:
            image = f"assets/images/mario/Mario{self.dimension}{self.direction}{self.state}{self.power}.png"

        # width, height = Image.open(image).size
        width, height = levelscreen.images[image]

        self.relative_width = self.relative_height * width / height
        self.image = image
