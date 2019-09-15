# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging
import sys


def get_logger(name):
    formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
