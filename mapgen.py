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


from opensimplex import OpenSimplex
import pygame

import township
import yamlui

pygame.init()

window = yamlui.generate_ui('data/ui/maptest.yaml')
ui_tree = yamlui.trees.get('maptest.yaml')
minimap = ui_tree.get('minimap-panel')

township.images.load_terrain()
township.images.load_map_resources()

map = township.map.Map(123123456574)

dx = dy = 0
xoffset = 0
yoffset = 0
tiles = True

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        window.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dx = -4
            elif event.key == pygame.K_a:
                dx = 4
            elif event.key == pygame.K_s:
                dy = -4
            elif event.key == pygame.K_w:
                dy = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                dx = 0
            elif event.key == pygame.K_s:
                dy = 0
            elif event.key == pygame.K_a:
                dx = 0
            elif event.key == pygame.K_w:
                dy = 0
            elif event.key == pygame.K_o:
                xoffset = 0
                yoffset = 0
    if dx != 0:
        xoffset += dx
    if dy != 0:
        yoffset += dy
    window.image.fill((0, 0, 0))
    map.draw(window.image, xoffset, yoffset, minimap.surface)
    window.update()
    window.draw()
    pygame.display.set_caption('%s' % clock.get_fps())
    clock.tick()
