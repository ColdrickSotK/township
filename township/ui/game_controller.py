# Copyright (c) 2018 Adam Coldrick
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

"""A controller to manage game state."""


import pygame
import yamlui

import township


@yamlui.callback('game_controller')
class GameController(object):

    """A controller to contain game state and drive the GameViewport.

    This class also defines callbacks used by the user interface
    labels displayed within the viewport, to access the game state.

    """

    def __init__(self, event, widget):
        # Pre-load resources
        township.images.load_terrain()
        township.images.load_map_resources()

        # TODO(SotK): Map generation shouldn't happen here
        # Should be loading a map that was pre-generated in
        # the menu screen.
        self.map = township.map.Map(123123456574)

        self.state = 'idle'
        self.selected = []
        self.selected_items = []
        self.selected_actors = pygame.sprite.Group()
        self.selection_origin = None
        self.current_tile = None

    def clear_selection(self):
        """Deselect everything, and mark affected chunks as dirty."""
        for tile in self.selected:
            tile.select()
            tile.chunk.dirty = True
        for item in self.selected_items:
            item.select()
        for actor in self.selected_actors:
            actor.select()
        self.selected = []
        self.selected_items = []
        self.selected_actors = pygame.sprite.Group()

    def select_tile(self, x, y):
        """Select the tile at pixel (x, y).

        This method takes a pixel coordinate, with the map scrolling offset
        subtracted to convert from screen-space to map-space. It also sets
        the selection origin to the selected tile.

        :param x: x position of the pixel to select the tile at.
        :param y: y position of the pixel to select the tile at.

        """
        tile = self.map.get_tile(x, y)
        selected = tile.select()
        tile.chunk.dirty = True
        self.selection_origin = tile
        if selected is None:
            self.selected.append(tile)
            for item in self.selected_items:
                item.select()
            self.selected_items = []
        else:
            self.selected_items.append(selected)

    def select_to_tile(self, x, y):
        """Select a square of tiles starting from the selection origin.

        This method takes a pixel coordinate with the map scrolling offset
        subtracted to convert from screen-space to map-space. If there is
        a tile already selected, a square of tiles from the selection origin
        to the tile at the given coordinate is selected, otherwise the tile
        at the given coordinate alone is selected. In the latter case, the
        selection origin is set to the selected tile.

        :param x: x position of the pixel to select up to.
        :param y: y position of the pixel to select up to.

        """
        if not self.selected:
            self.select_tile(x, y)
            return
        tile = self.map.get_tile(x, y)

        x_range = range(min(self.selection_origin.x, tile.x),
                        max(self.selection_origin.x, tile.x) + 1)
        y_range = range(min(self.selection_origin.y, tile.y),
                        max(self.selection_origin.y, tile.y) + 1)

        selection = []
        for tile_x in x_range:
            for tile_y in y_range:
                tile = self.map.get_tile(tile_x * 16, tile_y * 16)
                if not tile.selected:
                    tile.select(select_items=False)
                    tile.chunk.dirty = True
                selection.append(tile)

        for tile in self.selected:
            if tile not in selection:
                tile.select()
                tile.chunk.dirty = True
        self.selected = selection

    def select_actor(self, x, y):
        handled = False
        for actor in self.map.actors:
            if actor.rect.collidepoint(x, y):
                actor.select()
                if actor in self.selected_actors:
                    self.selected_actors.remove(actor)
                else:
                    self.selected_actors.add(actor)
                handled = True
        return handled

    def move_selected(self, x, y):
        for actor in self.selected_actors:
            actor.move_to(x, y)

    def get_current_tile_info(self, event=None, widget=None, **kwargs):
        if self.current_tile is None:
            return ''
        tile_info = """Tile: (%d, %d)
    Type: %s
    Height: %dm
    Resources: %s""" % (
            self.current_tile.x,
            self.current_tile.y,
            self.current_tile.type.capitalize(),
            self.current_tile.height * 400,
            self.current_tile.get_resource())
        return tile_info

    def get_selection_info(self, event=None, widget=None, **kwargs):
        if self.selected_items:
            return str(self.selected_items[0])
        return ''

    def get_selected_actor_info(self, event=None, widget=None, **kwargs):
        if self.selected_actors:
            return str(self.selected_actors.sprites()[0])
        return ''
