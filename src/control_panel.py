import os
import pyglet
import ConfigParser

class ControlPanelError(Exception): pass

class ControlPanelSkinError(Exception): pass

class ControlPanel(object):
    def __init__(self, skin_name):
        self.current_skin_name = skin_name

        self.cached_skins = {}
        self.last_skin_name = self.current_skin_name

        self.load_skin(self.current_skin_name)

    def load_skin(self, skin_name):
        """
        Initialize a new ControlPanelSkin object for the specified skin
        """

        loaded_skin = ControlPanelSkin(skin_name)

        self.skin = loaded_skin
        self.cached_skins[skin_name] = loaded_skin

        self.current_skin_name = skin_name

    def switch_skin(self, skin_name):
        """
        Switch the current skin of this control panel to the specified skin.

        If the specified skin is not cached, load it and cache it.
        """

        self.last_skin_name = self.current_skin_name

        if skin_name not in self.cached_skins.keys():
            self.load_skin(self, skin_name)

        self.skin = self.cached_skins[skin_name]

class ControlPanelSkin(object):
    def __init__(self, skin_name):
        # TODO: Fix path (has to be run from src dir to work in this state)
        skin_dir = os.path.join('..', 'data', 'control_panels', skin_name)

        dat_parser = ConfigParser.SafeConfigParser()

        try:
            dat_parser.readfp(open(os.path.join(skin_dir, skin_name + '.dat')))
        except IOError:
            raise ControlPanelSkinError, 'skin %s was not found' % skin_name

        image_files = dat_parser.items('Image Files')
        name_to_path = dict([(k, skin_dir + os.sep + v) for k,v in image_files])

        self.straight_img = pyglet.image.load(name_to_path['straight'])
        self.corner_img = pyglet.image.load(name_to_path['corner'])
        self.plus_img = pyglet.image.load(name_to_path['plus'])
        self.border_split_img = pyglet.image.load(name_to_path['border_split'])

if __name__ == '__main__':
    control_panel = ControlPanel('basic')
