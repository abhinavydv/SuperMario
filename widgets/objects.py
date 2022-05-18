"""
All the static objects like the ground, bricks and others will be defined here.
"""


from widgets.periodic import Piranha
from widgets.sprite import DynamicSprite, StaticSprite, Collection
from kivy.clock import Clock


class GroundCenter(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/Ground_Green_Center.png"


class GroundLeft(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/Ground_Green_Left.png"


class GroundRight(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/Ground_Green_Right.png"


# class Ground(StaticSprite):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.image = "assets/images/tiles/groundgreen.png"


class Ground(Collection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_added_to_screen(self, levelscreen):

        # GroundLeft
        left = GroundLeft()
        self.sprites["GroundLeft"] = left
        left.relative_height = self.relative_height
        left.relative_position = self.relative_position
        width, height = levelscreen.images[left.image]
        left.relative_width = left.relative_height * width / height

        # GroundCenter
        width, height = levelscreen.images["assets/images/tiles/Ground_Green_Center.png"]
        num_centers = int((self.relative_width - left.relative_width) / (self.relative_height * width / height))

        for i in range(num_centers):
            center = GroundCenter()
            self.sprites[f"GroundCenter{i}"] = center
            center.relative_height = self.relative_height
            center.relative_width = center.relative_height * width / height
            center.relative_position[1] = self.relative_position[1]
            center.relative_position[0] = self.relative_position[0] + left.relative_width + i * center.relative_width

        # GroundRight
        right = GroundRight()
        self.sprites["GroundRight"] = right
        right.relative_position[1] = self.relative_position[1]
        right.relative_height = self.relative_height
        width, height = levelscreen.images[right.image]
        right.relative_width = right.relative_height * width / height
        right.relative_position[0] = self.relative_position[0] + self.relative_width - right.relative_width
        # right.relative_position[0] = self.relative_position[0] + self.relative_width 

        super().get_added_to_screen(levelscreen)


class PipeHead(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/pipe_head_green.png"


class PipeBody(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/pipe_body_green.png"


class Pipe(Collection):
    """
    This will be a Collection type of class.
    """
    
    def __init__(self):
        super().__init__()
        self.hidden_level = None  # None: There is no hidden level
                                  # HiddenLevel{No} (str): The number of hidden level
        self.has_piranha = None   # The piranha like plant that comes out of pipe

    def get_added_to_screen(self, levelscreen):
        if self.has_piranha:
            piranha = Piranha()
            self.sprites["piranha"] = piranha
            piranha.pipe = self

            piranha.relative_width = self.relative_width / 2
            piranha.relative_height = piranha.relative_width * 1.5
            piranha.relative_screen_position = self.relative_screen_position
            piranha.relative_position  = self.relative_position
            piranha.relative_position[0] += (self.relative_width - piranha.relative_width)/2
            piranha.relative_position[1] += (self.relative_height - piranha.relative_height)
            piranha.relative_velocity = list(levelscreen.sprites["Piranha"]["relative_velocity"])
            piranha.max_relative_velocity = list(levelscreen.sprites["Piranha"]["max_relative_velocity"])

        head = PipeHead()
        body = PipeBody()
        self.sprites["head"] = head
        self.sprites["body"] = body
        head.width_fixed = body.width_fixed = True

        self.sprites["head"].relative_width = self.relative_width
        self.sprites["head"].relative_height = self.relative_width / 2
        self.sprites["head"].relative_position = list(self.relative_position)
        self.sprites["head"].relative_position[1] += self.relative_height - \
            self.sprites["head"].relative_height

        self.sprites["body"].relative_width = self.relative_width * 5/6
        self.sprites["body"].relative_height = self.relative_height - \
            self.sprites["head"].relative_height
        self.sprites["body"].relative_position = list(self.relative_position)
        self.sprites["body"].relative_position[0] += (self.relative_width - 
            self.sprites["body"].relative_width)/2

        levelscreen.update_list.append(self)

        super().get_added_to_screen(levelscreen)

    def update(self, levelscreen, dt):
        pass


class BrokenOrangeBrick(DynamicSprite):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.collider = False
        self.image = "assets/images/tiles/brick_orange_1.png"
        self.max_time = 2
        self.elapsed = 0

        from kivy.app import App
        self.app = App.get_running_app()

    def move(self, levelscreen, dt):
        self.elapsed += dt
        if self.elapsed > self.max_time:
            self.clean_up()
        self.relative_position[0] += self.relative_velocity[0] * dt
        self.relative_position[1] += self.relative_velocity[1] * dt
        self.relative_velocity[1] += self.app.settings["physics"]["gravity"] * dt


class OrangeBrick(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/tiles/brick_orange_1.png"

    def on_collide(self, other: object, col):
        super().on_collide(other, col)

        if other.tag == "mario":
            if col[2] == "bottom":
                if other.small:
                    self.relative_position[1]+=0.01
                    Clock.schedule_once(lambda dt: self.fix_position(), 0.1)
                else:
                    self.breaks()

    def fix_position(self):
        self.relative_position[1] -= 0.01

    def breaks(self):
        from math import sin, cos, pi
        # self.clean_up()
        for i in range(4):
            particle = BrokenOrangeBrick()
            particle.relative_height = self.relative_height/2
            particle.relative_width = self.relative_width/2
            particle.relative_position = [self.relative_position[0] + particle.relative_width*(i//2),
                                        self.relative_position[1] + particle.relative_height*(i%2)]

            angle = (135-30*i)*pi/180
            particle.relative_velocity = [0.5*cos(angle), 0.5*sin(angle)]
            particle.relative_screen_position = self.relative_screen_position
            particle.get_added_to_screen(self.parent.parent)
        self.clean_up()


class QuestionBlock(StaticSprite):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/Question_Block_0.png"
        self.content = "Coin"  # Coin, Mushroom, Fireflower or Star
        self.is_dead = False

    def on_collide(self, other: object, col):
        super().on_collide(other, col)
        if not self.is_dead:
            if col[2] == "bottom" and other.tag == "mario":
                self.is_dead = True
                self.activate()

    def activate(self):
        levelscreen = self.parent.parent
        self.image = "assets/images/items/Question_Block_Dead.png"

        # Blow away the dynamic sprite that is present above the block
        for sprite in levelscreen.dynamic_sprites:
            if sprite.tag == "powerup":
                sprite.relative_velocity[1] = 0.1
                continue
            if sprite.x < self.right\
                and self.x < sprite.right\
                    and -3 < sprite.y-self.top < 4:
                sprite.get_blown()

        # If the hidden item is mushroom and mario is small then
        # leave the hidden item as mushroom. But if mario is big, convert 
        # hidden item to FireFlower
        if self.content == "Mushroom":
            if not levelscreen.mario.small:
                self.content = "FireFlower"

        # Show the hidden item
        content = levelscreen.sprites[self.content]
        content["name"] = self.content
        content["relative_position"] = list(self.relative_position)
        content["relative_position"][0] += (self.relative_width-content["relative_width"])/2
        content["relative_position"][1] += (self.relative_height-content["relative_height"])/2
        content["relative_screen_position"] = self.relative_screen_position

        import importlib
        Collectible = getattr(importlib.import_module("widgets.collectibles"), self.content)

        collectible = Collectible()
        collectible.set_attributes(content)
        self.parent.add_widget(collectible)

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: collectible.reveal(dt, self))


class Castle(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/Castle.png"


class Flag(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = ""