# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import datetime

from queue import PriorityQueue

from gl_const import *
from logger import get_logger
from node import Node


class NodeSet(object):
    def __init__(self):
        self.storage = dict()

    def insert(self, node):
        self.storage[hash(node)] = node

    def empty(self):
        return len(self.storage) == 0

    def get(self, node):
        return self.storage.get(hash(node), None)

    def pop(self, node):
        return self.storage.pop(hash(node), None)


class NodeQueue(object):
    def __init__(self, breakingties):
        self.breakingties = breakingties
        self.storage = PriorityQueue()

    def insert(self, node):
        if self.breakingties == G_MIN:
            self.storage.put((node.f, node.g, node))
        else:
            self.storage.put((node.f, -node.g, node))

    def pop(self):
        if self.storage.empty():
            return None

        f, g, node = self.storage.get()
        return node


class SearchResult(object):
    def __init__(self):
        self.pathfound = False
        self.numberofsteps = 0
        self.pathtime = None
        self.pathlength = None
        self.pathlength_scaled = None
        self.lppath = []
        self.hppath = []
        self.time = None


class Search(object):
    logger = get_logger(__name__)

    TIME_TO_STOP = 1000

    def __init__(self, map, options):
        self.map = map
        self.options = options
        self.reservations = set()

    def compute_h_from_cell_to_cell(self, node, successor):
        i1, j1 = node.i, node.j
        i2, j2 = successor.i, successor.j
        hweight = self.options.hweight
        if self.options.metrictype == EUCL:
            return hweight * (((i1 - i2) * (i1 - i2) + (j1 - j2) * (j1 - j2)) ** 0.5)
        if self.options.metrictype == DIAG:
            return hweight * ((abs(i1 - i2) + abs(j1 - j2)) + (SQRT_TWO - 2) * min(abs(i1 - i2), abs(j1 - j2)))
        if self.options.metrictype == MANH:
            return hweight * (abs(i1 - i2) + abs(j1 - j2))
        if self.options.metrictype == CHEB:
            return hweight * max(abs(i1 - i2), abs(j1 - j2))
        return 0

    def find_successors(self, node):
        for i, j in [
            (node.i, node.j),
            (node.i, node.j - 1),
            (node.i, node.j + 1),
            (node.i - 1, node.j),
            (node.i + 1, node.j)
        ]:
            if not self.map.is_available(node, Node(i, j)):
                continue

            successor = Node(i, j)
            successor.g = node.g + 1
            successor.h = self.compute_h_from_cell_to_cell(node, successor)
            successor.f = successor.g + successor.h
            successor.t = node.t + 1

            if (i, j, successor.t) in self.reservations:
                continue

            if (i, j, node.t) in self.reservations and (node.i, node.j, successor.t) in self.reservations:
                continue

            if successor.t >= self.TIME_TO_STOP:
                continue

            yield successor

    def make_lppath(self, current_node):
        for t in range(current_node.t, self.TIME_TO_STOP):
            self.reservations.add((current_node.i, current_node.j, t))
        lppath = []
        while current_node.parent is not None:
            self.reservations.add((current_node.i, current_node.j, current_node.t))
            lppath.append(current_node)
            current_node = current_node.parent
        self.reservations.add((current_node.i, current_node.j, current_node.t))
        lppath.append(current_node)
        lppath.reverse()
        return lppath

    def make_hppath(self, lppath):
        hppath = []
        previous_direction = -1
        previous_node = lppath[0]
        current_direction = -1
        for current_node in lppath:
            if current_node == previous_node:
                continue
            if current_node.j < previous_node.j:
                current_direction = 0
            elif current_node.j > previous_node.j:
                current_direction = 1
            elif current_node.i < previous_node.i:
                current_direction = 2
            else:
                current_direction = 3
            if current_direction != previous_direction:
                hppath.append(previous_node)
            previous_node = current_node
            previous_direction = current_direction
        hppath.append(lppath[len(lppath) - 1])
        return hppath

    def compute(self, start, goal):
        search_result = SearchResult()

        start_time = datetime.datetime.now()

        opened = NodeSet()
        closed = NodeSet()

        sorted_opened = NodeQueue(self.options.breakingties)

        opened.insert(start)
        sorted_opened.insert(start)

        while not opened.empty() and not search_result.pathfound:
            current_node = sorted_opened.pop()
            if opened.get(current_node) is None:
                continue

            search_result.numberofsteps += 1

            if current_node == goal:
                search_result.pathfound = True

                search_result.lppath = self.make_lppath(current_node)
                search_result.hppath = self.make_hppath(search_result.lppath)
                search_result.pathtime = len(search_result.lppath)
                search_result.pathlength = len(set((node.i, node.j) for node in search_result.lppath))
                search_result.pathlength_scaled = search_result.pathlength * self.map.cellsize

                break

            opened.pop(current_node)
            closed.insert(current_node)

            successors = self.find_successors(current_node)
            for successor in successors:
                if closed.get(successor) is not None:
                    continue

                current_successor = opened.get(successor)
                if current_successor is None or successor.g < current_successor.g:
                    successor.parent = current_node

                    opened.insert(successor)
                    sorted_opened.insert(successor)

        finish_time = datetime.datetime.now()
        search_result.time = (finish_time - start_time).total_seconds()

        return search_result
