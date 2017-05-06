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


import random

from opensimplex import OpenSimplex
import pygame

from township import conf
from township import images
from township.resources import Rock, Tree


class NoiseGenerator(object):

    """An abstraction to create seeded OpenSimplex noise on demand."""

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)
        self.octaves = [OpenSimplex(int(random.random()*1000))
                        for i in range(0, 8)]

    def noise2d(self, x, y, octaves=1, amplitude=0.5):
        """Return noise with the given number of octaves.

        Maximum number of octaves is 8. Numbers over 8 are assumed to be
        8. More octaves produces less smooth noise, but is slower.

        :param x: The x coordinate to get noise at.
        :param y: The y coordinate to get noise at.
        :param octaves: The number of octaves of noise to use.
        
        """
        if octaves > 8:
            octaves = 8

        nx = (float(x) / (200 * amplitude)) - amplitude
        ny = (float(y) / (200 * amplitude)) - amplitude
        divisor = 0.0
        result = 0.0
        for i in range(0, octaves):
            f = 2**i
            divisor += 1.0 / f
            result += self.octaves[i].noise2d(f*nx, f*ny) / f
        result /= divisor

        return result


class Tile(object):

    """A representation of a single map tile."""

    def __init__(self, chunk, x, y, height_gen):
        """Initialize a tile, generating its metadata.

        :param chunk: The chunk which contains this tile.
        :param x: The x position of this tile in the world.
        :param y: The y position of this tile in the world.
        :param height_gen: A NoiseGenerator to generate the height of
        the tile.

        """
        self.chunk = chunk
        self.height_gen = height_gen
        self.x = x
        self.y = y

        self.height = self.height_gen.noise2d(x, y, octaves=5)
        self.get_image()

    def get_image(self):
        c = (127 * self.height) + 128
        if self.height < -0.10:
            self.colour = [0, 0, c]
            self.image = images.get_terrain('ocean')
        elif self.height < -0.088:
            self.colour = [0, 0, c]
            self.image = images.get_terrain('water-sand-75')
        elif self.height < -0.075:
            self.colour = [0, 0, c]
            self.image = images.get_terrain('water-sand-50')
        elif self.height < -0.063:
            self.colour = [0, 0, c]
            self.image = images.get_terrain('water-sand-25')
        elif self.height < -0.05:
            self.colour = [c, c, 0]
            self.image = images.get_terrain('beach')
        elif self.height < -0.035:
            self.colour = [c, c, 0]
            self.image = images.get_terrain('sand-grass-75')
        elif self.height < -0.015:
            self.colour = [c, c, 0]
            self.image = images.get_terrain('sand-grass-50') 
        elif self.height < 0:
            self.colour = [c, c, 0]
            self.image = images.get_terrain('sand-grass-25')
        elif self.height < 0.4:
            self.colour = [0, c, 0]
            ext = 'a' if random.random() > 0.1 else 'b'
            self.image = images.get_terrain('grass' + ext)
        elif self.height < 0.425:
            self.colour = [c, c, c]
            self.image = images.get_terrain('cliff-grass-25')
        elif self.height < 0.46:
            self.colour = [c, c, c]
            self.image = images.get_terrain('cliff-grass-50')
        elif self.height < 0.5:
            self.colour = [c, c, c]
            self.image = images.get_terrain('cliff-grass-75')
        else:
            self.colour = [c, c, c]
            self.image = images.get_terrain('cliffa')

    def draw(self, surface, rendermode='tiles'):
        if rendermode == 'tiles':
            surface.blit(self.image, ((self.x%16)*self.image.get_width(),
                                      (self.y%16)*self.image.get_height()))
        elif rendermode == 'pixels':
            surface.set_at((self.x % 16, self.y % 16), self.colour)
        else:
            raise Exception('Unrecognised render mode for Tile: %s' %
                            rendermode)


class Chunk(object):

    """A container for a 16x16 set of tiles.

    The world is divided into chunks of 16x16 tiles to allow only
    a manageable part of the world to be rendered at any given time.

    """

    def __init__(self, x, y, height_gen, rock_gen, tree_gen):
        """Initialize a chunk, generating its contents.

        :param x: The x position of this chunk.
        :param y: The y position of this chunk.
        :param height_gen: A NoiseGenerator to generate the height of
        the tiles in this chunk.
        :param rock_gen: A NoiseGenerator to generate rocks in this
        chunk.
        :param tree_gen: A NoiseGenerator to generate trees in this
        chunk.

        """
        self.x = x
        self.y = y

        sample = images.get_terrain()
        size = (sample.get_width() * 16, sample.get_height() * 16)
        self.tiled_surface = pygame.Surface(size, flags=pygame.SRCALPHA)
        self.pixel_surface = pygame.Surface((16, 16), flags=pygame.SRCALPHA)

        # Chunks are 16x16 tiles, so the x positions of tiles
        # in a given chunk are from 16 * x to (16 * x) + 16. The
        # equivalent is true for tile y positions.
        xoffset = 16 * x
        yoffset = 16 * y
        self.tiles = []
        self.rocks = []
        self.trees = []
        for u in range(xoffset, xoffset+16):
            tile_col = []
            rock_col = []
            tree_col = []
            for v in range(yoffset, yoffset+16):
                tile = Tile(self, u, v, height_gen)
                rock = rock_gen.noise2d(u, v, octaves=5, amplitude=0.025)
                if rock + tile.height > 0.75:
                    rock_col.append(Rock(self, tile, u, v, 100))
                tree = tree_gen.noise2d(u, v, octaves=5, amplitude=0.05)
                if tile.height > 0 and tile.height < 0.45 and tree > 0.3:
                    if rock + tile.height < 0.75:
                        tree_col.append(Tree(self, tile, u, v, 100))
                tile_col.append(tile)
            self.tiles.append(tile_col)
            self.rocks.append(rock_col)
            self.trees.append(tree_col)

        self.render()

    def get_tile(self, x, y):
        """Get the tile at a given (x, y) position in the chunk.

        :param x: The x position of the tile in the chunk.
        :param y: The y position of the tile in the chunk.

        """
        x += 16 * self.x
        y += 16 * self.y
        return self.tiles[x][y]

    def render(self):
        """Render the chunks tiles onto the relevant surfaces."""
        for col in self.tiles:
            for tile in col:
                tile.draw(self.tiled_surface, rendermode='tiles')
                tile.draw(self.pixel_surface, rendermode='pixels')
        # TODO(SotK): Draw rocks and trees separately in a resource
        # overlay
        for col in self.rocks:
            for rock in col:
                rock.draw(self.tiled_surface, rendermode='tiles')
                rock.draw(self.pixel_surface, rendermode='pixels')
        for col in self.trees:
            for tree in col:
                tree.draw(self.tiled_surface, rendermode='tiles')
                tree.draw(self.pixel_surface, rendermode='pixels')

    def draw(self, surface, xoffset=0, yoffset=0, rendermode='tiles'):
        """Draw the chunk onto the given surface."""
        if rendermode == 'tiles':
            pos = (self.x * self.tiled_surface.get_width() + xoffset,
                   self.y * self.tiled_surface.get_height() + yoffset)
            surface.blit(self.tiled_surface, pos)
        elif rendermode == 'pixels':
            pos = (self.x * 16 + xoffset, self.y * 16 + yoffset)
            surface.blit(self.pixel_surface, pos)
        else:
            raise Exception('Unrecognised render mode for Chunk: %s' %
                            rendermode)


class Map(object):

    """A container for a set of chunks.

    This represents all of the chunks that are currently loaded in memory.

    """

    def __init__(self, seed, x=10, y=10):
        """Initialize a Map.

        This creates a map with a given seed, and generates an
        initial set of chunks of a given size.

        :param seed: Seed to use when creating noise generators.
        :param x: How many columns of chunks to create. Default 10.
        :param y: How many rows of chunks to create. Default 10.

        """
        self._make_generators(seed)
        self.chunks = self._generate_initial_chunks(x, y)

    def _make_generators(self, seed):
        """Make the noise generators for this map.

        :param seed: The seed to use when creating the noise generators.

        """
        random.seed(seed)
        seeds = [random.random() for _ in range(0, 3)]
        self.height_noise = NoiseGenerator(seeds[0])
        self.rock_noise = NoiseGenerator(seeds[1])
        self.tree_noise = NoiseGenerator(seeds[2])

    def _generate_initial_chunks(self, x, y):
        """Generate some initial chunks for the map.

        :param x: The number of columns to generate.
        :param y: The number of rows to generate.

        """
        chunks = []
        for chunk_x in range(0, x):
            column = []
            for chunk_y in range(0, y):
                column.append(Chunk(
                    chunk_x, chunk_y,
                    self.height_noise,
                    self.rock_noise,
                    self.tree_noise))
            chunks.append(column)
        return chunks

    def draw(self, surface, xoffset, yoffset, minimap=None):
        """Draw the map onto a surface with a given offset.

        :param surface: The surface to draw on.
        :param xoffset: The x coordinate to draw in the top left.
        :param yoffset: The y coordinate to draw in the top left.
        :param minimap: Surface to render a minimap on.

        """
        if minimap is not None:
            minimap.fill((0, 0, 0))
        for column in self.chunks:
            for chunk in column:
                chunk.draw(surface, xoffset, yoffset, 'tiles')
                if minimap is not None:
                    chunk.draw(minimap, 128 + (xoffset / 16), 128 + (yoffset / 16), 'pixels')
