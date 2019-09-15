# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from logger import get_logger


class Node(object):
    logger = get_logger(__name__)

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.g = 0
        self.h = 0
        self.f = 0
        self.t = 0
        self.parent = None

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)

    def __hash__(self):
        return hash((self.i, self.j, self.t))

    def __str__(self):
        return "Node(i: {i}, j: {j})".format(
            i=self.i,
            j=self.j
        )

    def __add__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented("unsupported operand type(s) for +: '{}' and '{}'".format(
                type(self), type(other)
            ))
        return Node(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented("unsupported operand type(s) for -: '{}' and '{}'".format(
                type(self), type(other)
            ))
        return Node(self.i - other.i, self.j - other.j)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise NotImplemented("unsupported operand type(s) for *: '{}' and '{}'".format(
                type(self), type(other)
            ))
        return Node(self.i * other, self.j * other)

    def __iadd__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented("unsupported operand type(s) for +=: '{}' and '{}'".format(
                type(self), type(other)
            ))
        self.i += other.i
        self.j += other.j
        return self

    def __isub__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented("unsupported operand type(s) for -=: '{}' and '{}'".format(
                type(self), type(other)
            ))
        self.i -= other.i
        self.j -= other.j
        return self

    def __imul__(self, other):
        if not isinstance(other, int):
            raise NotImplemented("unsupported operand type(s) for *=: '{}' and '{}'".format(
                type(self), type(other)
            ))
        self.i *= other
        self.j *= other
        return self

    def __neg__(self):
        self.i = -self.i
        self.j = -self.j
        return self
