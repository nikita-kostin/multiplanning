# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import argparse

from mission import Mission
from logger import get_logger

parser = argparse.ArgumentParser()
parser.add_argument(
    'filenames',
    metavar='<str>',
    type=str,
    nargs=True,
    help='Files to process.'
)

logger = get_logger(__name__)


if __name__ == '__main__':
    logger.info('Starting...')

    args = parser.parse_args()

    for filename in args.filenames:
        logger.info("Processing file, filename = {}".format(filename))
        mission = Mission(filename)

        return_code = mission.read()
        if return_code != 0:
            logger.info('Skipping...')
            continue

        mission.compute()

        mission.write()

    logger.info('Terminating...')
