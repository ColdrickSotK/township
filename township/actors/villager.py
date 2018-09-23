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
            'speed': 10
        }

        # The following attributes describe the villager's place in the
        # social hierarchy of the township
        self.role = 'chieftain'
        self.relationships = {}

        # The following attributes are implementation details for rendering
        # the villager on the screen
        self.image = Surface((16, 16), flags=SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        circle(self.image, (0, 0, 0), (8, 8), 6)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
