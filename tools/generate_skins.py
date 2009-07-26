#!/usr/bin/env python

import os
import sys
import Image
import ConfigParser

MAPS_PATH = os.path.join('..', 'data', 'ui_maps')
SKINS_PATH = os.path.join('..', 'data', 'skins')

def render_map_with_skin(map_name, skin_name):
    map = load_map(map_name)
    skin = load_skin(skin_name)

    fname = map_name[:-4]
    out_path = os.path.join(SKINS_PATH, skin_name, fname + '.png')
    width, height = len(map[0]) * 8, len(map) * 8

    out = Image.new('RGB', (width, height))

    for i, line in enumerate(map):
        for j, tile in enumerate(line):
            if tile != None:
                out.paste(skin[tile], (j * 8, i * 8, j * 8 + 8, i * 8 + 8))

    out.save(out_path)

def load_map(map_name):
    # TODO: Fix path stuff
    map_path = os.path.join(MAPS_PATH, map_name)
    map_lines = [line.strip() for line in open(map_path).readlines()]

    width, height = len(map_lines[0]), len(map_lines)

    if not len(list(set([len(l) for l in map_lines]))) == 1:
        raise Exception, 'All lines must be of the same length'

    tile_map = []

    for i, map_line in enumerate(map_lines):
        tile_map_line = []

        for j, map_char in enumerate(map_line):
            if map_char != '.':
                north = i != 0 and map_lines[i - 1][j] != '.'
                south = i != height - 1 and map_lines[i + 1][j] != '.'
                east = j != width - 1 and map_lines[i][j + 1] != '.'
                west = j != 0 and map_lines[i][j - 1] != '.'

                if north and south and east and west:
                    tile_map_line.append('plus')
                elif north and south and west:
                    tile_map_line.append('t_e')
                elif north and south and east:
                    tile_map_line.append('t_w')
                elif north and west and east:
                    tile_map_line.append('t_s')
                elif south and west and east:
                    tile_map_line.append('t_n')
                elif south and east:
                    tile_map_line.append('corner_nw')
                elif south and west:
                    tile_map_line.append('corner_ne')
                elif north and west:
                    tile_map_line.append('corner_se')
                elif north and east:
                    tile_map_line.append('corner_sw')
                elif north or south:
                    tile_map_line.append('vertical')
                else:
                    tile_map_line.append('horizontal')
            else:
                tile_map_line.append(None)

        tile_map.append(tile_map_line)

    return tile_map

def load_skin(skin_name):
    skin_dir = os.path.join(SKINS_PATH, skin_name)
    # TODO: Fix path stuff
    dat_parser = ConfigParser.SafeConfigParser()
    dat_parser.readfp(open(os.path.join(skin_dir, skin_name + '.dat')))

    image_files = dat_parser.items('Image Files')
    name_to_path = dict([(k, skin_dir + os.sep + v) for k,v in image_files])

    skin = {}

    # Line Tiles
    skin['vertical'] = Image.open(name_to_path['straight'])
    skin['horizontal'] = skin['vertical'].rotate(90)

    # Corner tiles
    skin['corner_nw'] = Image.open(name_to_path['corner'])
    skin['corner_sw'] = skin['corner_nw'].rotate(90) 
    skin['corner_se'] = skin['corner_sw'].rotate(90) 
    skin['corner_ne'] = skin['corner_se'].rotate(90) 

    # T-shaped tiles (direction is empty space)
    skin['t_w'] = Image.open(name_to_path['t'])
    skin['t_s'] = skin['t_w'].rotate(90) 
    skin['t_e'] = skin['t_s'].rotate(90) 
    skin['t_n'] = skin['t_e'].rotate(90) 

    # Plus tile
    skin['plus'] = Image.open(name_to_path['plus'])

    return skin

if __name__ == '__main__':
    if len(sys.argv) > 1:
        skins_todo = sys.argv[1:]
    else:
        all_skins = [skin for skin in os.listdir(SKINS_PATH)]
        skins_todo = [skin for skin in all_skins if
                      os.path.isdir(os.path.join(SKINS_PATH, skin))]

    for skin_name in skins_todo:
        maps_todo = [map for map in os.listdir(MAPS_PATH)]
        maps_todo = [map for map in maps_todo if map.endswith('.map')]

        for map_name in maps_todo:
            render_map_with_skin(map_name, skin_name)
