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


from pygame import SRCALPHA
from pygame import Surface
from pygame.sprite import Sprite
from pygame.draw import circle

from township.util.vectors import Vector2


class Villager(Sprite):

    """A villager, the basic member of a township."""

    def __init__(self):
        Sprite.__init__(self)

        # TODO(SotK): Generate names and stats
        self.name = 'Riofaal the Magnificent'
        self.stats = {
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 10,
            'wisdom': 10,
            'charisma': 10,
            'speed': 10.0
        }

        # The following attributes describe what the villager is currently
        # doing, and how fast they're doing it.
        self.state = 'idle'
        self.velocity = Vector2(0, 0)

        # The following attributes describe the villager's place in the
        # social hierarchy of the township.
        self.role = 'chieftain'
        self.relationships = {}

        # The following attributes describe aspects of the villager's state
        # which directly affect how it is rendered.
        self.selected = False

        # The following attributes are implementation details for rendering
        # the villager on the screen.
        self.dirty = False
        self.image = Surface((16, 16), flags=SRCALPHA)
        self._redraw()
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
        self.position = [500, 500]
        self.target = self.position

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        circle(self.image, (0, 0, 0), (8, 8), 6)
        if self.selected:
            circle(self.image, (255, 255, 255), (8, 8), 8, 1)

    def update(self, xoffset, yoffset):
        if self.dirty:
            self._redraw()
            self.dirty = False
        if self.state == 'moving':
            self.position[0] += self.velocity.x
            self.position[1] += self.velocity.y

            distance = Vector2.from_points(self.position, self.target)
            if distance.magnitude <= 4:
                self.state = 'idle'
                self.target = self.position

        # Move the sprite into position, accounting for viewport offset
        self.rect.x = self.position[0] + xoffset
        self.rect.y = self.position[1] + yoffset

    def select(self):
        self.selected = not self.selected
        self.dirty = True

    def move_to(self, x, y):
        self.state = 'moving'
        self.target = [x, y]
        self.velocity = Vector2.from_points(self.position, (x, y)).normalised
