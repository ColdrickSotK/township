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

height_noise = township.map.NoiseGenerator(123123456574)
rock_noise = township.map.NoiseGenerator(1231247542)
tree_noise = township.map.NoiseGenerator(123128)
chunks = []
dx = dy = 0
xoffset = 0
yoffset = 0
tiles = True
for x in range(-8, 8):
    row = []
    for y in range(-8, 8):
        row.append(township.map.Chunk(x, y, height_noise, rock_noise, tree_noise))
    chunks.append(row)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        window.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dx = -2
            elif event.key == pygame.K_a:
                dx = 2
            elif event.key == pygame.K_s:
                dy = -2
            elif event.key == pygame.K_w:
                dy = 2
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
    for row in chunks:
        for chunk in row:
            chunk.draw(window.image, xoffset, yoffset, 'tiles')
            chunk.draw(minimap.surface, 128, 128, 'pixels')
    window.update()
    window.draw()
    pygame.display.set_caption('%s' % clock.get_fps())
    clock.tick()
