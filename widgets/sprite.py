"""
The base classes for creation of all kinds of sprites are defined here.

There will be two kinds of classes :
    1. Sprite: An object that is to be shown on the screen as it is.
        (For eg: Mario, Mushroom, Goomba etc.)
    2. Collection: A collection of sprites which deefines the position of each sprite.
        (For eg: Pipe (A collection of pipehead and pipebody.))
"""


from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.core.window import Window

from PIL import Image


Builder.load_file("widgets/sprite.kv")


class Sprite(Widget):
    """
    The base class from which every sprite will be created.
    It contains methods common to all the sprites.

    The sprite class has the attributes relative_position,
    relative_velocity, relative_height, etc. which are used
    to define movements and size independent of the Window size.
    All these values are defined considering the window height to be
    1 unit. These are used to support Multiple Window sizes.

    Note : All the collisions will be checked using
            sprite.position and not sprite.pos.
    """

    image = StringProperty("")
    relative_position = ListProperty([0, 0])
    relative_height = NumericProperty(0)
    relative_width = NumericProperty(0)
    relative_screen_position = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_static = True
        self.danger = False  # is the sprite dangerous for Mario
        self.tag = "sprite"
        self.center_x2 = self.center_x
        self.center_y2 = self.center_y
        self.position = [0, 0]
        self.collider = True
        self.invisible = False
        self.is_abstract = False
        self.is_fireproof = False
        self.type = "Sprite"
        self.width_fixed = False

    def update(self, levelscreen, dt):
        """
        levelscreen: The screen widget inside which the level is being played.
                        It is called here so that the sprite lists can be accessed.
        dt: The time between the previous and the current frame.
        ____________________________________________________________________________

        This function is called in every frame of the second loop(The game loop).
        It will be overridden while creating the Sprites.
        """

    def on_collide(self, other, col):
        """
        other: The other sprite which collided.
        col: Collision data. [True, (direction_x, direction_y), direction_of_collision]
        ____________________________________________

        Called when this sprite collides with any 
        other sprite in Game.
        """

    def if_collides(self, sprite):
        """
        sprite: The sprite to check collision with.
        ____________________________________________

        Return True if the sprite collides with this sprite else False.
        """

        if (self.position[0] <= sprite.position[0] + sprite.width)\
                and (self.position[1] <= sprite.position[1] + sprite.height)\
                and (sprite.position[0] <= self.position[0] + self.width)\
                and (sprite.position[1] <= self.position[1] + self.height)\
                and self.collider and sprite.collider:
            # print(sprite)
            # print(self.position[0] < sprite.position[0] + sprite.width)
            # print(self.position[1] < sprite.position[1] + sprite.height)
            # print(sprite.position[0] < self.position[0] + self.width)
            # print(sprite.position[1] < self.position[1] + self.height)
            return True
        return False

    def detect_collision(self, sprite):
        """
        sprite: The sprite to detect collision with.
        _______________________________________________

        Logic to detect collision with the passed sprite.
        The directions are: left, right, top, bottom.

        Return a list containing a bool, a list of directions, a direction.
        The bool is true if the collision is detected else false.
        The first direction in the list is the horizontal direction in which collision occured.
        The second direction is the vertical direction in which collision occured
        The third element is finalised direction in which collision occured.

        if the collision does not occur then a tuple containing False is returned.
        """

        direction = ["right", "top"]
        if self.if_collides(sprite):
            """
            dx: The width to which the sprites overlap.
            dy: The height to which the sprites overlap.
            The greater the overlap the more negative the value.
            """

            if self.center_x2 > sprite.center_x2:
                dx = self.position[0] - sprite.position[0] - sprite.width
                direction[0] = "left"
            else:
                dx = sprite.position[0] - self.position[0] - self.width

            if self.center_y2 > sprite.center_y2:
                dy = self.position[1] - sprite.position[1] - sprite.height
                direction[1] = "bottom"
            else:
                dy = sprite.position[1] - self.position[1] - self.height

            """
            The finalised direction of the collision is the 
            direction(horizontal | vertical) in which overlap is less negative.
            """
            if dy < dx:
                return [True, direction, direction[0]]
            else:
                return [True, direction, direction[1]]

        return (False,)

    def detect_collision2(self, sprite):
        """
        An attempt to make collision detection better.
        """
        if self.collide_widget(sprite):
            if self.center_x > sprite.center_x:
                if self.x < sprite.right:
                    pass

    def move_aside(self, sprite, col):
        """
        sprite: The sprite which has collided.
        col: collision data. (True, [direction_x, direction_y], direction_of_collision)
        ______________________________________________________________________________

        Move The collided sprite to a side according to the direction of collision.
        It is a part of the rectangular collider. When the sprites overlap, it separates
        them in such a way that it appears as if the have repelled each other.
        """
        direction = col[2]
        if direction == "top":
            sprite.relative_position[1] = self.relative_position[1] + \
                (self.height)/Window.height
        elif direction == "bottom":
            sprite.relative_position[1] = self.relative_position[1] - \
                (sprite.height)/Window.height
        elif direction == "left":
            sprite.relative_position[0] = self.relative_position[0] - \
                (sprite.width + 1)/Window.height
        elif direction == "right":
            sprite.relative_position[0] = self.relative_position[0] + \
                (self.width + 1)/Window.height

    def animate(self, levelscreen, dt):
        """
        levelscreen: The screen widget inside which the level is being played.
                        It is called here so that the sprite lists can be accessed.
        dt: The time between the previous and the current frame.
        __________________________________________________________________________

        The method that will be overriden to animate the sprite.
        """

    def exchange_direction(self, direction):
        """
        Return the direction opposite to the passed direction.
        """
        if direction == "left":
            return "right"
        if direction == "right":
            return "left"
        if direction == "top":
            return "bottom"
        if direction == "bottom":
            return "top"

    def set_attributes(self, data):
        """
        data: A dictionary containing (attribute: value) pairs which 
        are to be set on the current sprite.
        ____________________________________________________________

        The attributes define the state of the sprite like position and velocity.
        """
        for i in data:
            if isinstance(data[i], list):
                setattr(self, i, list(data[i]))
            elif isinstance(data[i], dict):
                setattr(self, i, dict(data[i]))
            else:
                setattr(self, i, data[i])

    def get_added_to_screen(self, levelscreen):
        if not self.width_fixed:
            width, height = levelscreen.images[self.image]
            self.relative_width = self.relative_height * width / height
        levelscreen.mainlayout.add_widget(self)


class Collection(Sprite):

    def __init__(self):
        super().__init__()

        self.sprites = {}  # The dictionary of sprites present in this collection
        self.type = "Collection"
        self.relative_velocity = [0, 0]

    def get_added_to_screen(self, levelscreen):
        self.levelscreen = levelscreen
        for i in self.sprites:
            # sprite = self.sprites[i]

            # levelscreen.mainlayout.add_widget(sprite)
            # if sprite.is_static:
            #     levelscreen.static_sprites.append(sprite)
            # else:
            #     levelscreen.dynamic_sprites.append(sprite)

            self.sprites[i].get_added_to_screen(levelscreen)

    def update(self, levelscreen, dt):
        """
        levelscreen: The screen widget inside which the level is being played.
        dt: The time between the previous and the current frame.
        ____________________________________________________________________________

        This function is called in every frame of the second loop(The game loop).
        """

    def set_attributes(self, data):
        """
        data: A dictionary containing (attribute: value) pairs which are to be
                set on the current collection.
        _______________________________________________________________________

        The attributes define the state of the collection like position and velocity.
        """
        for i in data:
            if isinstance(data[i], list):
                setattr(self, i, list(data[i]))
            elif isinstance(data[i], dict):
                setattr(self, i, dict(data[i]))
            else:
                setattr(self, i, data[i])

    def clean_up(self):
        try:
            self.levelscreen
        except:
            raise Exception("Cannot clean up. The sprite is not added to screen.")
        
        for i in self.sprites:
            sprite = self.sprites[i]

            self.levelscreen.mainlayout.remove_widget(sprite)
            if sprite.is_static:
                self.levelscreen.static_sprites.remove(sprite)
            else:
                self.levelscreen.dynamic_sprites.remove(sprite)

        self.sprites.clear()


class StaticSprite(Sprite):
    """
    The base class for Static Sprites i.e. the sprites with no 
    move method. The sprites that inherit from this class include
    ground, pipes, etc.
    """
    danger = False

    def detect_collisions(self, dynamic_sprites):
        """
        dynamic_sprites: The list of dynamic sprites to detect collisions with.
        ____________________________________________________________________

        This method detects collisions with all of the dynamic sprites in the list.
        And also calls some methods based on the collisions.

        !!! This method is to be removed as static sprites don't detect collisions now.
        """
        # print(dynamic_sprites)
        for sprite in dynamic_sprites:
            col = self.detect_collision(sprite)
            if col[0]:
                sprite.on_collide(self, col)
                self.move_aside(sprite, col)

    def on_collide(self, other: object, col):
        """
        The overridden method of the widgets.sprite.Sprite class.
        ________________________________________________________

        When a dynamic sprites collides with this sprite, it calles this method.
        Then this method calls the on_collide method of the dynamic sprite so that
        it performs necessary actions.
        """

        col[2] = self.exchange_direction(col[2])
        col[1][0] = self.exchange_direction(col[1][0])
        col[1][1] = self.exchange_direction(col[1][1])

        other.on_collide(self, col)

    def clean_up(self):
        self.parent.parent.static_sprites.remove(self)
        self.parent.remove_widget(self)

    def get_added_to_screen(self, levelscreen):
        super().get_added_to_screen(levelscreen)
        levelscreen.static_sprites.append(self)
        if levelscreen.right_most_sprite is None or self.right>levelscreen.right_most_sprite.right:
            levelscreen.right_most_sprite = self


class DynamicSprite(Sprite):
    """
    The base class for dynamic sprites i.e. the sprites that will be able to move.
    The sprites that inherit from this class include Enemies, Mario and moving power ups.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_static = False
        self.relative_velocity = [0, 0]
        self.max_relative_velocity = [0, 0]
        self.moving = False
        self.direction = "Right"
        self.use_gravity = True

    def update(self, levelscreen, dt):
        """
        Overriden method of widgets.sprite.Sprite Class
        """
        self.move(levelscreen, dt)
        self.animate(levelscreen, dt)

    def if_collides(self, sprite):
        if not sprite.is_static and sprite.tag != "powerup":
            if self.invisible or sprite.invisible:
                return False
        return super().if_collides(sprite)

    def move(self, levelscreen, dt):
        """
        levelscreen: The screen widget inside which the level is being played.
                        It is called here so that the sprite lists can be accessed.
        dt: The time between the previous and the current frame.
        __________________________________________________________________________

        This method is called in the update method.
        It is to be overriden in order to define sprite movement.
        """

        if self.top < 0:
            self.die()

    def detect_collisions(self, sprite_list: list):
        """
        sprite_list: The list of dynamic sprites to detect collisions with.
        ____________________________________________________________________

        This method detects collisions with all of the sprites in the list.
        And also calls some methods based on the collisions.
        """
        sprite: DynamicSprite
        for sprite in sprite_list:
            if sprite == self:
                continue
            col = self.detect_collision(sprite)
            if col[0]:
                sprite.on_collide(self, col)

    def mario_collided(self, mario, col):
        """
        mario: The widgets.mario.Mario object
        col: collision data
        ___________________________________________________

        This method defines what happens when mario collides with
        this sprite.
        """

    def die(self):
        """
        Called when the sprite dies.
        It will animate itself as dying and will eventually remove 
        itself from the game.

        This method is to be overriden to define what to do when dying.
        """

        self.clean_up()

    def get_blown(self):
        """
        It's a kind of dying in which the sprite jumps, gets inverted and
        falls below the screen.
        """
        self.die()

    def clean_up(self):
        self.parent.parent.dynamic_sprites.remove(self)
        self.parent.remove_widget(self)

    def get_added_to_screen(self, levelscreen):
        super().get_added_to_screen(levelscreen)

        levelscreen.dynamic_sprites.append(self)
