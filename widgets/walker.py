"""
Classes for the creation of sprites that walk on the ground.

Walker: The base class for all walking creatures.

"""

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

        from kivy.app import App
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

        self.relative_position[0] += self.relative_velocity[0] * dt
        self.relative_position[1] += self.relative_velocity[1] * dt

        if self.use_gravity:
            self.relative_velocity[1] += self.app.settings["physics"]["gravity"] * dt

    def on_collide(self, other, col):
        if other.is_abstract:
            return
        if col[2] == "right":
            if self.direction == "Right":
                self.direction = "Left"
            else:
                self.direction = "Right"
            self.relative_velocity[0] *= -1

        elif col[2] == "left":
            if self.direction == "Right":
                self.direction = "Left"
            else:
                self.direction = "Right"
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

        # if other.is_static:
        #     other.move_aside(self, col)
        other.move_aside(self, col)

    def jump(self, multiplier=1):
        levelscreen = self.parent.parent
        for sprite in levelscreen.static_sprites + levelscreen.dynamic_sprites:
            if (sprite.x < self.x + self.width)\
                and (self.x < sprite.x + sprite.width)\
                    and (-3/Window.height <= self.y - (
                        sprite.y + sprite.height) <= 1/Window.height):

                self.relative_position[1] += 3/Window.height
                self.relative_velocity[1] = self.max_relative_velocity[1] * multiplier

    def jump2(self, multiplier=1):
        self.relative_velocity[1] = self.max_relative_velocity[1] * multiplier

    def mario_collided(self, mario, col):
        if mario.is_invincible:
            self.get_blown()
        
        elif col[2] == "bottom":
            if mario.jumping:
                mario.jump2()
            else:
                mario.jump2(0.5)
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

        self.image = "assets/images/baddies/Goomba_Normal_1.png"
        self.i = 1
        self.animate_time = 0
        self.dead = False

    def animate(self, levelscreen, dt):
        if self.dead:
            self.animate_time += dt
            if self.animate_time >= 2:
                self.clean_up()
            return
        self.animate_time += dt
        if self.animate_time >= 0.25:
            self.animate_time = 0
            self.i += 1
            if self.i > 2:
                self.i = 1
            self.image = f"assets/images/baddies/Goomba_Normal_{self.i}.png"

    def die(self):
        if not self.dead:
            self.dead = True
            self.animate_time = 0
            self.relative_velocity = [0, 0]
            self.image = "assets/images/baddies/Goomba_Dead.png"
            self.relative_height /= 2

    def mario_collided(self, mario, col):
        if not self.dead:
            super().mario_collided(mario, col)

    def get_blown(self):
        if not self.dead:
            self.dead = True
            self.animate_time = 0
            self.image = "assets/images/baddies/Goomba_Flip.png"
            self.relative_velocity[0] = 0
            self.collider = False
            self.jump2()


class Koopa(Walker):
    """
    The turtle like creature with its head like a duck.
    When mario hits it from up side it goes inside its shell,
    and when again hit from the side, it starts sliding very
    fast and destroys every creature that comes in its way.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/baddies/Koopa_Green_Right_1.png"
        
        self.i = 1
        self.animate_time = 0
        self.in_shell = False
        self.color = "Green"
        self.dead = False
        
    def animate(self, levelscreen, dt):
        if self.dead:
            return
        self.animate_time += dt
        if self.in_shell:
            self.image = "assets/images/baddies/Shell_Green_Still.png"
            self.relative_height = self.relative_width
            if self.animate_time >= 15 and self.relative_velocity[0] == 0:
                self.in_shell = False
                self.relative_width /= 0.8
                self.relative_height = self.relative_width * 1.4
                if self.direction == "Right":
                    self.relative_velocity[0] = self.max_relative_velocity[0] / 2
                else:
                    self.relative_velocity[0] = -self.max_relative_velocity[0] / 2
            elif self.animate_time >= 10 and self.relative_velocity[0] == 0:
                self.image = "assets/images/baddies/Shell_Green_Legs.png"
            return

        if self.animate_time >= 0.25:
            self.animate_time = 0
            self.i += 1
            if self.i > 2:
                self.i = 1
            self.image = f"assets/images/baddies/Koopa_{self.color}_{self.direction}_{self.i}.png"

    def mario_collided(self, mario, col):
        self.animate_time = 0
        if mario.is_invincible:
            self.get_blown()

        elif col[2] == "bottom":
            if mario.jumping:
                mario.jump2()
            else:
                mario.jump2(0.5)
            if self.in_shell:
                self.relative_velocity[0] = 0
            else:
                self.in_shell = True
                self.relative_velocity[0] = 0
                self.relative_width *= 0.8

        else:
            if self.relative_velocity[0] != 0:
                mario.die()
            else:
                if col[2] == "right":
                    self.relative_position[0] += 0.01
                    self.relative_velocity[0] = self.max_relative_velocity[0]*2
                elif col[2] == "left":
                    print(col)
                    self.relative_position[0] -= 0.01
                    self.relative_velocity[0] = -self.max_relative_velocity[0]*2

    def on_collide(self, other, col):
        if not other.is_static and self.in_shell and self.relative_velocity[0] != 0:
            if other.tag == "mario" and other.is_invincible:
                self.get_blown()
            else:
                other.get_blown()
            return
        super().on_collide(other, col)

    def get_blown(self):
        self.dead = True
        self.animate_time = 0
        if not self.in_shell:
            self.relative_width *= 0.8
        self.relative_height = self.relative_width
        self.image = "assets/images/baddies/Shell_Green_Flip.png"
        self.relative_velocity[0] = 0
        self.collider = False
        self.jump2()
