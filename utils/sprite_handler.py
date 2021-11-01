import importlib


class SpriteAdder(object):

    def __init__(self):
        super().__init__()

        import json
        f = open("widgets/sprites.json")
        self.sprites = json.load(f)
        f.close()

    def add_all(self, level_data):
        """
        level_data: dict containing sprites with there positions and sizes.
        ___________________________________________________________________

        Adds the sprites to screen.
        """

        for i in level_data:
            sprite_data = level_data[i]
            sprite_data2 = dict(self.sprites[sprite_data["name"]])
            sprite_data2.update(sprite_data)

            self.add_one(sprite_data2)

    def add_one(self, data):
        """
        One sprite is added to the screen using its data.
        """

        class_path = data["class"]
        module, _, Class = class_path.rpartition(".")
        Sprite = getattr(importlib.import_module(module), Class)
        sprite = Sprite()

        if data["name"] == "Mario":
            self.mario = sprite

        try:
            sprite.set_attributes(data)
        except TypeError as e:
            import traceback
            traceback.print_exc()
        try:
            sprite.get_added_to_screen(self)
        except TypeError as e:
            print(e)
            traceback.print_exc()

        return sprite

    # def set_attributes(self, obj, data):
    #     for i in data:
    #         if isinstance(data[i], list):
    #             setattr(obj, i, list(data[i]))
    #         elif isinstance(data[i], dict):
    #             setattr(obj, i, dict(data[i]))
    #         else:
    #             setattr(obj, i, data[i])
