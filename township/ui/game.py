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

"""A yamlui widget to render the game in."""


import pygame

import township
import yamlui
from yamlui.util import create_surface
from yamlui.widget import Widget


class ViewportSurface(pygame.Surface):

    """The Surface used to represent the viewport on screen."""

    def __init__(self, image):
        """Initialise the Surface.

        :params image: The original look of the surface.

        """
        dimensions = (image.get_rect().width, image.get_rect().height)
        super(ViewportSurface, self).__init__(dimensions)

        self.original = image

        self.rect = self.get_rect()
        self.set_alpha(image.get_alpha())
        self.blit(self.original, (0, 0))

    def draw(self, surface):
        """Blit the viewport onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        # TODO(SotK): Handle relative positioning
        surface.blit(self, self.rect)


class GameViewport(Widget):

    """A viewport in which to render the game.

    This viewport also handles hotkey presses and mouse input.

    Example yaml definition:

        - object: game
          properties:
            position: [0, 0]
            width: 1280
            height: 800

    """

    def __init__(self, definition, style={}):
        super(GameViewport, self).__init__(definition, style=style)

        self.surface = create_surface(self, ViewportSurface)

        # Pre-load resources
        township.images.load_terrain()
        township.images.load_map_resources()

        # TODO(SotK): Map generation shouldn't happen here
        # Should be loading a map that was pre-generated in
        # the menu screen.
        self.map = township.map.Map(123123456574)
        self.state = 'idle'
        self.selected = []
        self.selection_origin = None

        self.dx = self.dy = self.xoffset = self.yoffset = 0

    def clear_selection(self):
        for tile in self.selected:
            tile.select()
            tile.chunk.dirty = True
        self.selected = []

    def select_tile(self, x, y):
        tile = self.map.get_tile(x, y)
        tile.select()
        tile.chunk.dirty = True
        self.selection_origin = tile
        self.selected.append(tile)

    def select_to_tile(self, x, y):
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
                    tile.select()
                    tile.chunk.dirty = True
                selection.append(tile)

        for tile in self.selected:
            if tile not in selection:
                tile.select()
                tile.chunk.dirty = True
        self.selected = selection

    def handle_event(self, event):
        """Handle an event.

        This function deals with handling keypresses and mouse input.

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.dx = -4
                return True
            elif event.key == pygame.K_a:
                self.dx = 4
                return True
            elif event.key == pygame.K_s:
                self.dy = -4
                return True
            elif event.key == pygame.K_w:
                self.dy = 4
                return True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_d, pygame.K_a):
                self.dx = 0
                return True
            elif event.key in (pygame.K_s, pygame.K_w):
                self.dy = 0
                return True
            elif event.key == pygame.K_o:
                self.xoffset = 0
                self.yoffset = 0
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.state = 'selecting'
            self.clear_selection()
            position = (event.pos[0] - self.xoffset,
                        event.pos[1] - self.yoffset)
            self.select_tile(*position)
            return True
        elif event.type == pygame.MOUSEMOTION:
            if self.state == 'selecting':
                position = (event.pos[0] - self.xoffset,
                            event.pos[1] - self.yoffset)
                self.select_to_tile(*position)
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.state = 'idle'
        return False

    def update(self):
        """Update the viewport."""
        self.xoffset += self.dx
        self.yoffset += self.dy
        self.map.update(self.surface, self.xoffset, self.yoffset)

        # Redraw the game onto the viewport surface
        ui_tree = yamlui.trees.get('maptest.yaml')
        minimap = ui_tree.get('minimap-panel')
        self.map.draw(
            self.surface, self.xoffset, self.yoffset, minimap.surface)

    def draw(self, surface):
        """Draw the viewport onto the given surface.

        :param surface: The surface to draw on.

        """
        self.surface.draw(surface)
