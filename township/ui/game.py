# Copyright (c) 2017-2018 Adam Coldrick
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
import yamlui
from yamlui.parsing import parse_children
from yamlui.util import create_surface
from yamlui.widget import Widget

import township


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


@yamlui.widget('game')
class GameViewport(Widget):

    """A viewport in which to render the game.

    This viewport also handles hotkey presses and mouse input. It only works
    correctly when an instance of ``township.ui.GameController`` is bound to
    it using the bind-object callback.

    Example YAML definition:

        - object: game
          bind-object: my_controller
          properties:
            position: [0, 0]
            width: 1280
            height: 800

    """

    def __init__(self, definition, style={}, parent=None):
        super(GameViewport, self).__init__(definition, style=style)
        self.children = parse_children(definition, widget=self, style=style)

        # `self.game` is set by the superclass constructor, assuming
        # that `bind-object` is set in the YAML definition of the viewport.
        # We make `self.game` an alias to it here, so that the code makes more
        # sense to avoid lots of mentions of bound objects.
        self.game = self.bound_object

        self.surface = create_surface(self, ViewportSurface)
        self.dx = self.dy = self.xoffset = self.yoffset = 0

    def handle_event(self, event):
        """Handle an event.

        This function deals with handling keypresses and mouse input.

        """
        handled = False
        for child in reversed(self.children):
            handled = child.handle_event(event)
            if handled:
                return handled

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.dx = -4
                handled = True
            elif event.key == pygame.K_LEFT:
                self.dx = 4
                handled = True
            elif event.key == pygame.K_DOWN:
                self.dy = -4
                handled = True
            elif event.key == pygame.K_UP:
                self.dy = 4
                handled = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.dx = 0
                handled = True
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                self.dy = 0
                handled = True
            elif event.key == pygame.K_o:
                self.xoffset = 0
                self.yoffset = 0
                handled = True
            elif event.key == pygame.K_s and self.game.selected:
                stockpile = township.constructions.Stockpile(
                    self.game.selected)
                self.game.map.stockpiles.append(stockpile)
                for tile in self.game.selected:
                    tile.select()
                    tile.chunk.dirty = True
                self.game.selected = []
                handled = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # TODO(SotK): Make this 1 a constant. It is the left mouse button.
            if event.button == 1:
                # First, check if the click is on an actor like a Villager. If
                # so then select the actor and skip tile-based selection.
                self.game.clear_selection()
                handled = self.game.select_actor(
                    event.pos[0], event.pos[1])

                # If an actor wasn't selected, then move onto tile-based
                # selection.
                if not handled:
                    self.game.state = 'selecting'
                    position = (event.pos[0] - self.xoffset,
                                event.pos[1] - self.yoffset)
                    self.game.select_tile(*position)
                    handled = True
        elif event.type == pygame.MOUSEMOTION:
            if self.game.state == 'selecting':
                position = (event.pos[0] - self.xoffset,
                            event.pos[1] - self.yoffset)
                self.game.select_to_tile(*position)
                handled = True
            elif self.game.state == 'idle':
                position = (event.pos[0] - self.xoffset,
                            event.pos[1] - self.yoffset)
                self.game.current_tile = (
                    self.game.map.get_tile(*position))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.game.state = 'idle'
            # TODO(SotK): Make this 3 a constant. It is the right mouse button.
            if event.button == 3:
                if self.game.selected_actors:
                    # If one or more actors are selected, right click is a
                    # command for them to move.
                    position = (event.pos[0] - self.xoffset,
                                event.pos[1] - self.yoffset)
                    self.game.move_selected(*position)
                else:
                    self.game.clear_selection()

                handled = True

        return handled

    def update(self):
        """Update the viewport."""
        self.xoffset += self.dx
        self.yoffset += self.dy
        self.game.map.update(self.surface, self.xoffset, self.yoffset)

        # Redraw the game onto the viewport surface
        ui_tree = yamlui.trees.get('maptest.yaml')
        minimap = ui_tree.get('minimap-panel')
        self.game.map.draw(
            self.surface, self.xoffset, self.yoffset, minimap.surface)

        for child in self.children:
            child.update()

    def draw(self, surface):
        """Draw the viewport onto the given surface.

        :param surface: The surface to draw on.

        """
        self.surface.draw(surface)

        for child in self.children:
            child.draw(surface)
