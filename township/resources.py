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


from township import images


class Resource(object):

    """Base class for resources that appear on the map."""

    def __init__(self, chunk, tile, x, y, value):
        """Initialise the resource.

        :param chunk: The chunk this resource is in.
        :param tile: The tile this resource is in.
        :param x: The x position of the resource in the world.
        :param y: The y position of the resource in the world.
        :param value: The amount of resource this resource gives.

        """
        self.chunk = chunk
        self.tile = tile
        self.x = x
        self.y = y
        self.value = value

        self.type = None
        self.image = None
        self.colour = [255, 255, 255]

    def draw(self, surface, rendermode='tiles'):
        """Draw the resource onto the given surface.

        :param surface: The surface to draw onto.
        :param rendermode: The mode to render using. `tiles` for the full
        image representation, `pixels` for a single pixel.

        """
        if rendermode == 'tiles':
            if not self.image:
                raise Exception('No image for resource, cannot render in'
                                '`tiles` render mode.')
            surface.blit(self.image, ((self.x%16)*self.image.get_width(),
                                      (self.y%16)*self.image.get_height()))
        elif rendermode == 'pixels':
            surface.set_at((self.x%16, self.y%16), self.colour)
        else:
            raise Exception('Unrecognised render mode for Resource: %s' %
                            rendermode)


class Rock(Resource):

    """Representation of a Rock resource node."""

    def __init__(self, chunk, tile, x, y, value):
        """Initialise the rock.

        :param chunk: The chunk this rock is in.
        :param tile: The tile this rock is in.
        :param x: The x position of the rock in the world.
        :param y: The y position of the rock in the world.
        :param value: The amount of stone this rock provides.

        """
        super(Rock, self).__init__(chunk, tile, x, y, value)

        self.type = 'rock'
        self.image = images.get_map_resource('rock')
        self.colour = [100, 100, 100]


class Tree(Resource):

    """Representation of a Tree resource node."""

    def __init__(self, chunk, tile, x, y, value):
        """Initialise the tree.

        :param chunk: The chunk this tree is in.
        :param tile: The tile this tree is in.
        :param x: The x position of the tree in the world.
        :param y: The y position of the tree in the world.
        :param value: The amount of wood this tree provides.

        """
        super(Tree, self).__init__(chunk, tile, x, y, value)

        self.type = 'tree'
        self.image = images.get_map_resource('tree')
        self.colour = [26, 109, 26]

    def draw(self, surface, rendermode='tiles'):
        """Draw the tree onto the given surface.

        :param surface: The surface to draw onto.
        :param rendermode: The mode to render using. `tiles` for the full
        image representation, `pixels` for a single pixel.

        """
        if rendermode == 'tiles':
            if not self.image:
                raise Exception('No image for resource, cannot render in'
                                '`tiles` render mode.')
            tile_size = self.tile.image.get_size()
            tile_x = (self.x % 16) * tile_size[0]
            tile_y = (self.y % 16) * tile_size[1]
            pos = (
                tile_x - (self.image.get_width() / 2) + (tile_size[0] / 2),
                tile_y - (self.image.get_height() / 2) + (tile_size[1] / 2)
            )
            surface.blit(self.image, pos)
        elif rendermode == 'pixels':
            surface.set_at((self.x%16, self.y%16), self.colour)
        else:
            raise Exception('Unrecognised render mode for Tree: %s' %
                            rendermode)
