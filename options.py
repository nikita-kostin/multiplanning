# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function


class Options(object):
    def __init__(self, config):
        self.searchtype = config['options']['searchtype']
        self.metrictype = config['options']['metrictype']
        self.hweight = config['options']['hweight']
        self.breakingties = config['options']['breakingties']
