from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    """
    The class to manage the in-app settings.

    The settings screen will be shown when the settings 
    button from homescreen will be pressed.

    All the settings are to be loaded from and saved to settings.json.

    ```LOGIC```
    Corresponding to each key in the key: value pair a widget will be created
    corresponding to the value type as given in the table.

    +-------------+---------------------------------------------------------+
    |  value type |      Widget type and Description                        |
    +-------------+---------------------------------------------------------+
    |    dict     | When the button is clicked a new screen will be opened  |
    |             | which will contain button coresponding to the keys and  |
    |             | values in the dict.                                     |
    |             |                                                         |
    |    list     | Multiple fields corresponding to each element in list   |
    |             | will be created. If the list consistes of two elements  |
    |             | out of which second element is a list[some data type]   |
    |             | and the first element has the data type as that present |
    |             | in the list then a drop down containing the list        |
    |             | elements as option and the first element as chosen      |
    |             | option will be created.                                 |
    |             |                                                         |
    |    bool     | A checkbox                                              |
    |             |                                                         |
    |     int     | A textfield. The value entered will be checked for its  |
    |             | type before saving                                      |
    |             |                                                         |
    |    string   | A textfield.                                            |
    +-------------+---------------------------------------------------------+

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self):
        import json
        f = open("settings.json")
        settings = self.settings = json.load(f)
        f.close()

        for i in settings:
            pass
