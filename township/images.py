# Copyright (c) 2016 Adam Coldrick
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

import pygame
import six


terrain = {}
map_resources = {}

def load_terrain():
    terraindir = os.path.join('images', 'map')
    for name in os.listdir(terraindir):
        path = os.path.join(terraindir, name)
        if path.endswith('.png'):
            tile = pygame.image.load(path).convert_alpha()
            name = name.rstrip('.png')
            terrain[name] = tile


def load_map_resources():
    map_resources_dir = os.path.join('images', 'map', 'resources')
    for name in os.listdir(map_resources_dir):
        path = os.path.join(map_resources_dir, name)
        if path.endswith('.png'):
            image = pygame.image.load(path).convert_alpha()
            name = name.rstrip('.png')
            map_resources[name] = image


def get_terrain(terraintype='grass'):
    for key in six.iterkeys(terrain):
        if terraintype in key:
            return terrain[key]
    return None


def get_map_resource(type='rock'):
    for key in six.iterkeys(map_resources):
        if type in key:
            return map_resources[key]
    return None
