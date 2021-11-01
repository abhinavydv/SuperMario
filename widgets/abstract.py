"""
Module for abstract materials like fireball.
"""


from widgets.jumper import Jumper


class FireBall(Jumper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/items/Fire_Ball_2.png"
        self.is_abstract = True
        self.relative_velocity = [0, 0]

    def on_collide(self, other, col):
        if other.is_static:
            if col[2] == "top":
                self.jump2()
            elif col[2] == "bottom":
                self.relative_velocity[1] *= -1
            else:
                self.clean_up()

        else:
            if not other.is_fireproof and not other.tag == "mario":
                other.get_blown()
                self.clean_up()