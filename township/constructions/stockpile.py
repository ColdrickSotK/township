# Copyright (c) 2017 Adam Coldrick
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


class Stockpile(object):

    """A resource stockpile, for storing gathered wood and stone."""

    def __init__(self, tiles):
        """Initialize a stockpile, adding it to the content of each tile.

        :param tiles: The tiles covered by this stockpile.

        """
        self.selected = False
        self.tiles = tiles
        for tile in tiles:
            tile.content.append(self)
            tile.chunk.dirty = True

        # TODO(SotK): Don't hardcode the maximum contents
        self.content = [None for tile in tiles]
        self.tile_max = 100

    def __repr__(self):
        return 'Stockpile, %d spaces' % len(self.content)

    def select(self):
        """Select this stockpile."""
        self.selected = not self.selected
        for tile in self.tiles:
            tile.chunk.dirty = True
