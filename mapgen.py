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


import pygame

import township
import yamlui


def register_widgets():
    """Add custom ui widgets to the yamlui class mapping."""
    # TODO(SotK): Minimap widget
    yamlui.class_mapping.update({
        'game': township.ui.game.GameViewport
    })

def register_controllers():
    """Add custom controllers to the yamlui callback dictionary."""
    yamlui.callbacks.update({
        'game_controller': township.ui.GameController
    })


pygame.init()

register_widgets()
register_controllers()
window = yamlui.generate_ui('data/ui/maptest.yaml')

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        window.handle_event(event)
    window.image.fill((0, 0, 0))
    window.update()
    window.draw()
    pygame.display.set_caption('%s' % clock.get_fps())
    clock.tick()
