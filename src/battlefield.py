#!/usr/bin/env python

import os
import pygame

MAPS_PATH = os.path.join('data', 'stages')
TILES_PATH = os.path.join('data', 'tiles', 'battlefield')

# TODO: Blit tiles onto battleground then render that?

# Load all tile images
pngs = [f for f in os.listdir(TILES_PATH) if f[-4:] == '.png']
loaded_images = [pygame.image.load(os.path.join(TILES_PATH, p)) for p in pngs]
TILE_IMGS = dict(zip([p[:-4] for p in pngs], loaded_images))

class Sprite(pygame.sprite.Sprite):
    group = pygame.sprite.RenderUpdates()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.group)


class Square(Sprite):
    def __init__(self, grid_x, grid_y):
        Sprite.__init__(self)

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.rect = pygame.rect.Rect((self.grid_x * 16, self.grid_y * 16,16,16))


class FloorTile(Square):
    image = TILE_IMGS['floortile']

    def __str__(self):
        return '.'


class CodeBaseTile(Square):
    def __str__(self):
        return '1'


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

if __name__ == '__main__':
    import sys
    from utils import render_sprite_groups

    if len(sys.argv) > 1:
        grid = Battlefield(sys.argv[1])
    else:
        grid = Battlefield('test.map')

    render_sprite_groups(Sprite.group)
