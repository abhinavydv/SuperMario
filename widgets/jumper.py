"""
This module contains classes to define the sprites that move by jumping.
The jumping sprites include flying goomba, fireball fired by Mario,
the star that makes Mario invincible and others.
"""


from widgets.walker import Walker, Goomba


class Jumper(Walker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jumping = True


class FlyGoomba(Goomba, Jumper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/baddies/Fly_Goomba_1.png"
        self.i = 1
        self.animate_time = 0

    def animate(self, levelscreen, dt):
        if self.jumping:
            self.animate_time += dt
            if self.animate_time >= 0.25:
                self.animate_time = 0
                self.i += 1
                if self.i > 3:
                    self.i = 1
                self.image = f"assets/images/baddies/Fly_Goomba_{self.i}.png"
                width, height = levelscreen.images[self.image]
                self.relative_height = self.relative_width * height / width
        else:
            super().animate(levelscreen, dt)

    def die(self):
        if self.jumping:
            self.jumping = False
            self.relative_height = self.relative_width
        else:
            super().die()
        
