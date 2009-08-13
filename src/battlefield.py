#!/usr/bin/env python

import os
import pyglet

MAPS_PATH = os.path.join('data', 'stages')

# TODO: Clean up
tile_path = os.path.join('data', 'tiles', 'battlefield')
pngs = [fname for fname in os.listdir(tile_path) if fname[-4:] == '.png']
TILE_IMGS = dict([(f[:-4], pyglet.image.load(os.path.join(tile_path + os.sep +
                                                          f))) for f in pngs])

class Square(object):
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y

    def draw(self, x, y):
        self.image.blit(x, y)


class FloorTile(Square):
    image = TILE_IMGS['floortile']

    def __str__(self):
        return '.'


class CodeBaseTile(Square):
    def __str__(self):
        return '1'

class CodeBase(object):
    pass

class Battlefield(object):
    def __init__(self, map_name):
        self.map_name = map_name

        self.load_map_file_naively()
        self.find_codebases()

    def load_map_file_naively(self):
        map_path = os.path.join(MAPS_PATH, self.map_name)
        map_lines = [line.strip() for line in open(map_path).readlines()]

        self.tiles_wide = len(map_lines[0])
        self.tiles_high = len(map_lines)

        self.tiles = []

        for i, line in enumerate(map_lines):
            row = []

            for j, char in enumerate(line):
                if char == '.':
                    row.append(FloorTile(j, i))
                elif char == '1':
                    row.append(CodeBaseTile(j, i))
                else:
                    print 'Unrecognized tile type "%s"' % char
                    exit()

            self.tiles.append(row)

        self.tiles.reverse()

    def find_codebases(self):
        # TODO: Better way to flatten?
        tiles_linear = []

        for row in self.tiles:
            tiles_linear += row

        cb_tiles = [t for t in tiles_linear if isinstance(t, CodeBaseTile)]
        all_coords = [(t.grid_x, t.grid_y) for t in cb_tiles]

        for tile in cb_tiles:
            suffix = 'nesw'

            if (tile.grid_x, tile.grid_y - 1) in all_coords:
                suffix = suffix.replace('n', '')

            if (tile.grid_x, tile.grid_y + 1) in all_coords:
                suffix = suffix.replace('s', '')

            if (tile.grid_x + 1, tile.grid_y) in all_coords:
                suffix = suffix.replace('e', '')

            if (tile.grid_x - 1, tile.grid_y) in all_coords:
                suffix = suffix.replace('w', '')

            tile.image = TILE_IMGS['codebase_' + suffix]

    def draw(self, x, y):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                tile.draw(x + 16 * j, y + 16 * i)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        grid = Battlefield(sys.argv[1])
    else:
        grid = Battlefield('test.map')

    window = pyglet.window.Window(256, 240)

    @window.event
    def on_draw():
        window.clear()
        grid.draw(0, 0)

    pyglet.app.run()
