from widgets.sprite import DynamicSprite
from kivy.core.window import Window
from time import time


class Periodic(DynamicSprite):
    """
    A class for sprites that have a fixed area (or line) where 
        (or alobg which) they can move.
    These repeat there motion and hence the name.
    """

    def move(self, levelscreen, dt):
        # Detect collisions only with dynamic sprites.
        self.detect_collisions(levelscreen.dynamic_sprites)

        # Move the sprite. Don't consider gravity as it is a fixed motion.
        self.relative_position[0] += self.relative_velocity[0]*dt
        self.relative_position[1] += self.relative_velocity[1]*dt

        side = self.check_extreme()
        if side:
            self.on_extreme_reached(side)

    def check_extreme(self):
        """
        Method to check if extreme position has been reached.
        """

    def on_extreme_reached(self):
        """
        This method is called when the extreme position of the
        periodic motion is reached.
        """


class Piranha(Periodic):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/baddies/Piranha_1.png"
        self.pipe = None
        self.t = time()
        self.waiting = False
        self.wait_duration = 0.4
        self.mario_wait_duration = 2

        self.animate_time = 0
        self.i = 1

    def animate(self, levelscreen, dt):
        self.animate_time += dt
        if self.animate_time >= 0.5:
            self.animate_time = 0
            self.i += 1
            if self.i > 2:
                self.i = 1
            
            self.image = f"assets/images/baddies/Piranha_{self.i}.png"

    def check_extreme(self):
        if self.pipe is not None:
            if self.pos[1] >= self.pipe.top-2:
                return "top"
            if self.top <= self.pipe.top-2:
                return "bottom"
        return False

    def on_extreme_reached(self, side=""):
        if self.waiting:
            if self.mario_in_vicinity() and side == "bottom":
                self.relative_velocity[1] = 0
                self.t = time() + self.mario_wait_duration
            elif time() - self.t > self.wait_duration:
                self.waiting = False
                if side == "bottom":
                    self.relative_velocity[1] = self.max_relative_velocity[1]
                    # print(1)
                else:
                    # print(3)
                    self.relative_velocity[1] = -self.max_relative_velocity[1]
                    # print(self.relative_velocity, 2)

        else:
            # print(2)
            # print(side)
            # print(self.relative_velocity)
            if (self.relative_velocity[1] < 0 and side == "top" )or \
                (self.relative_velocity[1] > 0 and side == "bottom"):
                # print(4)
                return
            self.waiting = True
            self.t = time()
            self.relative_velocity[1] = 0
            # print(5)

    def mario_in_vicinity(self):
        mario = self.parent.parent.mario

        if self.pipe.x <= mario.right+4 and\
            self.pipe.right >= mario.x-4 and\
                self.pipe.top >= mario.y-4 and\
                    self.pipe.y <= mario.top+4:
            return True

        return False

    def on_collide(self, other, col):
        if other.tag == "mario":
            self.mario_collided(other, col)

    def mario_collided(self, mario, col):
        if self.waiting:
            return
        if mario.is_invincible:
            self.die()
        else:
            mario.die()
        