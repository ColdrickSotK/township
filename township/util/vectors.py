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

"""Utilities for working with two-dimensional vectors."""


import math


class Vector2(object):

    """A two-dimensional vector."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector2(%f, %f)' % (self.x, self.y)

    @property
    def magnitude(self):
        return math.sqrt(self.y**2 + self.x**2)

    @property
    def normalised(self):
        mag = self.magnitude
        if mag == 0:
            raise ValueError("Can't normalise a vector with magnitude 0")
        return Vector2(self.x / mag, self.y / mag)

    @classmethod
    def from_points(cls, start, end):
        return cls(end[0] - start[0], end[1] - start[1])
