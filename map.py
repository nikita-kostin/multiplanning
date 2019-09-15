# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from gl_const import *
from logger import get_logger
from node import Node


class Map(object):
    logger = get_logger(__name__)

    def __init__(self, config):
        self.cellsize = config['map']['cellsize']
        self.height = config['map']['height']
        self.width = config['map']['width']
        self.grid = config['map']['grid']
        self.searches = [
            (
                Node(search['start']['i'], search['start']['j']),
                Node(search['goal']['i'], search['goal']['j'])
            ) for search in config['map']['searches']
        ]

    def is_obstacle(self, node):
        return self.grid[node.i][node.j] == OBS

    def is_traversable(self, node):
        return self.grid[node.i][node.j] == NO_OBS

    def is_on_grid(self, node):
        return -1 < node.i < self.height and -1 < node.j < self.width

    def is_available(self, node, successor):
        return self.is_on_grid(successor) and self.is_traversable(successor)
