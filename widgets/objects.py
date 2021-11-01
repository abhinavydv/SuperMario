"""
All the static objects like the ground, bricks and others will be defined here.
"""


from operator import le
from widgets.periodic import Piranha
from widgets.sprite import StaticSprite, Collection


class Ground(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/tiles/groundgreen.png"


class PipeHead(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/tiles/pipe_head_green.png"


class PipeBody(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/tiles/pipe_body_green.png"


class Pipe(Collection):
    """
    This will be a Collection type of class.
    """
    
    def __init__(self):
        super().__init__()

        head = PipeHead()
        body = PipeBody()
        self.sprites["head"] = head
        self.sprites["body"] = body
        self.hidden_level = None  # None: There is no hidden level
                                  # HiddenLevel{No} (str): The number of hidden level
        self.has_piranha = None   # The piranha like plant that comes out of pipe

    def get_added_to_screen(self, levelscreen):
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

        super().get_added_to_screen(levelscreen)

    def update(self, levelscreen, dt):
        pass


class OrangeBrick(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/tiles/brick_orange_1.png"


class QuestionBlock(StaticSprite):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/items/Question_Block_0.png"
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
        self.image = "assets/items/Question_Block_Dead.png"

        # Blow away the dynamic sprite that is present above the block
        for sprite in levelscreen.dynamic_sprites:
            if sprite.x < self.right\
                and self.x < sprite.right\
                    and -3 < sprite.y-self.top < 4:
                sprite.get_blown()

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

        self.image = "assets/items/Castle.png"


class Flag(StaticSprite):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = ""