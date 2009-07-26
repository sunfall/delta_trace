import os
import pyglet

class ControlPanelError(Exception): pass


class ControlPanelSkinError(Exception): pass


class ControlPanel(object):
    def __init__(self, skin_name):
        self.skin_name = skin_name

        self.cached_skins = {}

        self.switch_skin(self.skin_name)

    def _cache_skin(self, skin_name):
        skin_dir = os.path.join('..', 'data', 'skins', skin_name)
        cp_image = pyglet.image.load(os.path.join(skin_dir,'control_panel.png'))

        self.cached_skins[skin_name] = cp_image

    def switch_skin(self, skin_name):
        """
        Switch the current skin of this control panel to the specified skin.

        If the specified skin is not cached, cache it.
        """

        self.last_skin_name = self.skin_name

        if skin_name not in self.cached_skins.keys():
            self._cache_skin(skin_name)

        self.skin_name = skin_name
        self.image = self.cached_skins[skin_name]

    def draw(self):
        self.image.blit(0, 0)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        control_panel = ControlPanel(sys.argv[1])
    else:
        control_panel = ControlPanel('basic')

    window = pyglet.window.Window(256, 240)

    @window.event
    def on_draw():
        window.clear()
        control_panel.draw()

    pyglet.app.run()
