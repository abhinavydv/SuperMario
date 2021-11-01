from widgets.walker import Walker
from widgets.sprite import DynamicSprite, StaticSprite
from widgets.jumper import Jumper


class Collectible(object):

    def __init__(self):
        super().__init__()
        self.max_relative_velocity = [.1, .4]

    def reveal(self, dt, block):
        # print("revealed")
        from kivy.clock import Clock
        self.interval = Clock.schedule_interval(lambda dt: self.go_up(dt, block), 0.01)

    def go_up(self, dt, block):
        # print("going up")
        # print(self.pos)
        self.relative_position[1] += self.max_relative_velocity[1] * dt
        # print(self.max_relative_velocity)
        # print(self.relative_position)
        if self.y > block.top:
            self.interval.cancel()
            if self.is_static:
                block.parent.parent.static_sprites.append(self)
                print(1)
            else:
                block.parent.parent.dynamic_sprites.append(self)
                print(2)


class Mushroom(Walker, Collectible):
    """
    The magical mushroom eating which makes mario bigger.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/items/Mushroom.png"
        self.tag = "powerup"

    def mario_collided(self, mario, col):
        mario.grow()
        self.clean_up()


class FireFlower(StaticSprite, Collectible):
    """
    The flower that gives mario the power to throw fireballs.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/items/Fire_Flower.png"
        self.tag = "powerup"

    def on_collide(self, other, col):
        if other.tag == "mario":
            other.get_fire()
            self.clean_up()
        super().on_collide(other, col)


class PowerStar(Jumper, Collectible):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/items/StarPower.png"
        self.tag = "powerup"

    def mario_collided(self, mario, col):
        mario.be_invincible()
        self.clean_up()


class Coin(DynamicSprite, Collectible):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.images = ["assets/items/Coin_1.png",
                        "assets/items/Coin_2.png",
                        "assets/items/Coin_3.png",
                        "assets/items/Coin_4.png",
                        "assets/items/Coin_5.png",
                        "assets/items/Coin_6.png",
                        "assets/items/Coin_7.png",
                        "assets/items/Coin_8.png",
        ]
        self.i = 0
        self.collider = False

        from kivy.app import App
        self.gravity = App.get_running_app().settings["physics"]["gravity"]

    def reveal(self, dt, block):
        from kivy.clock import Clock
        self.interval = Clock.schedule_interval(self.go_up, 0.01)

    def go_up(self, dt):
        self.relative_position[1] += self.relative_velocity[1] * dt
        self.relative_velocity[1] += self.gravity * dt
        self.opacity -= self.relative_velocity[1] * dt

        self.image = self.images[self.i%8]

        self.i += 1

        if self.relative_velocity[1]<-self.max_relative_velocity[1]/5:
            self.interval.cancel()

            self.parent.remove_widget(self)
