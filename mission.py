# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json

from marshmallow import ValidationError

from drawer import Drawer
from logger import get_logger
from map import Map
from options import Options
from schemas import input_schema, output_schema
from search import Search


class Mission(object):
    logger = get_logger(__name__)

    def __init__(self, filename):
        self.filename = filename
        self.map = None
        self.options = None
        self.search_results = []

    def read(self):
        try:
            with open(self.filename, 'r') as f:
                config = json.loads(f.read())
        except ValueError as exc:
            self.logger.error(str(exc))
            self.logger.error('Could not open input file!')
            return 1

        try:
            config = input_schema.load(config)
        except ValidationError as exc:
            self.logger.error(str(exc))
            self.logger.error('Could not parse input file!')
            return 2

        self.map = Map(config)
        self.options = Options(config)
        return 0

    def compute(self):
        search = Search(self.map, self.options)

        found_path_counter = 0
        found_path_nos = 0
        found_path_t = 0
        found_path_l = 0
        found_path_ls = 0

        for start, goal in self.map.searches:
            search_result = search.compute(start, goal)
            if search_result.pathfound:
                found_path_counter += 1
                found_path_nos += search_result.numberofsteps
                found_path_t += search_result.pathtime
                found_path_l += search_result.pathlength
                found_path_ls += search_result.pathlength_scaled

            self.search_results.append(search_result)

        self.logger.info("Found {}/{} paths!".format(found_path_counter, len(self.map.searches)))
        self.logger.info("Average number of steps: {}".format(found_path_nos / found_path_counter))
        self.logger.info("Average path time: {}".format(found_path_t / found_path_counter))
        self.logger.info("Average path length: {}".format(found_path_l / found_path_counter))
        self.logger.info("Average scaled path length: {}".format(found_path_ls / found_path_counter))

    def write(self):
        output = json.dumps(
            output_schema.dump({
                'search_results': self.search_results
            }), indent=2, sort_keys=True
        )

        filename = (self.filename[:-5] if self.filename.endswith('.json') else self.filename) + '_output.json'
        with open(filename, 'w') as f:
            f.write(output)

        drawer = Drawer()
        drawer.write(self.map, self.search_results, self.filename)

        self.logger.info('Results saved!')
