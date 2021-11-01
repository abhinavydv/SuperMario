"""
Classes for the creation of sprites that walk on the ground.

Walker: The base class for all walking creatures.

"""


from kivy.app import App
from widgets.sprite import DynamicSprite
from kivy.core.window import Window


class Walker(DynamicSprite):
    """
    The base class for all walking creatures. They all
    inherit from this class.
    It defines functions for their motion, change of direction
    and similar kind of stuff.
    """
    # relative_velocity = [0,0]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        # load the settings and keep a reference to them.
        self.settings = self.app.settings

        self.relative_velocity = list(self.relative_velocity)
        self.jumping = False
        self.tag = "walker"

    def move(self, levelscreen, dt):
        """
        Logic for moving the Walker.

        First detect collisions
        and then change the position of the Walker.
        """

        if not self.moving:
            if self.x <= Window.width:
                self.moving = True
            return

        super().move(levelscreen, dt)

        self.detect_collisions(levelscreen.dynamic_sprites)
        self.detect_collisions(levelscreen.static_sprites)

        try:
            self.relative_position[0] += self.relative_velocity[0] * dt
            self.relative_position[1] += self.relative_velocity[1] * dt
        except:
            print(self, self.relative_position, self.relative_velocity)

        if self.use_gravity:
            self.relative_velocity[1] += self.app.settings["physics"]["gravity"] * dt

    def on_collide(self, other, col):
        if other.is_abstract:
            return
        if col[2] == "right":
            self.relative_velocity[0] *= -1

        elif col[2] == "left":
            self.relative_velocity[0] *= -1

        elif col[2] == "top":
            if not self.is_static:
                other.move_aside(self, col)
            self.relative_velocity[1] = 0
            if self.jumping:
                self.jump2()


        elif col[2] == "bottom":
            # if self.jumping:
            #     self.jump2()
            self.relative_velocity[1] *= -1
            if not self.is_static:
                other.move_aside(self, col)

        if other.tag == "mario":
            self.mario_collided(other, col)

        if other.is_static:
            other.move_aside(self, col)

    def jump(self, multiplier=1):
        current_screen = App.get_running_app().manager.current_screen
        # print(current_screen.name)
        if current_screen.name == "LevelScreen":
            for sprite in current_screen.static_sprites + current_screen.dynamic_sprites:
                if (sprite.x < self.x + self.width)\
                    and (self.x < sprite.x + sprite.width)\
                        and (-3/Window.height <= self.y - (
                            sprite.y + sprite.height) <= 1/Window.height):

                    self.relative_position[1] += 3/Window.height
                    self.relative_velocity[1] = self.max_relative_velocity[1] * multiplier

    def jump2(self, multiplier=1):
        current_screen = App.get_running_app().manager.current_screen
        if current_screen.name == "LevelScreen":
            # self.relative_position[1] += 3/Window.height
            self.relative_velocity[1] = self.max_relative_velocity[1] * multiplier

    def mario_collided(self, mario, col):
        if mario.is_invincible or col[2] == "bottom":
            if mario.jumping:
                mario.jump()
            else:
                mario.jump(0.5)
            self.die()
        else:
            mario.die()


class Goomba(Walker):
    """
    The small creature that walks on two legs.
    Has a big angry face and flat legs a bit like Humpty Dumpty.
    Does not have much brain and falls easily in the well (The empty space
    where there is no ground).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/baddies/Goomba_Normal_1.png"


class Koopa(Walker):
    """
    The turtle like creature with its head like a duck.
    When mario hits it from up side it goes inside its shell,
    and when again hit from the side, it starts sliding very
    fast and destroys every creature that comes in its way.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/baddies/koopa_green_right_1.png"
