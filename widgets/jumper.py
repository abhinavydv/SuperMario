"""
This module contains classes to define the sprites that move by jumping.
The jumping sprites include flying goomba, fireball fired by Mario,
the star that makes Mario invincible and others.
"""


from widgets.walker import Walker


class Jumper(Walker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jumping = True


class FlyGoomba(Jumper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/baddies/fly_gomba_1.png"
        
