# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import imageio
import os
import random
import shutil

from PIL import Image, ImageDraw
from collections import namedtuple
from copy import deepcopy
from enum import Enum

from gl_const import *
from logger import get_logger


class RandomColorGenerator(object):
    color_storage = [(0, 0, 0), (255, 255, 255)]

    def __init__(self, too_much=5):
        self.too_much = too_much

    def too_close(self, color):
        x, y, z = color
        for p_color in self.color_storage:
            p_x, p_y, p_z = p_color
            if abs(x - p_x) < self.too_much or abs(y - p_y) < self.too_much or abs(z - p_z) < self.too_much:
                return True
        return False

    def generate(self):
        r = lambda: random.randint(0,255)
        color = (r(), r(), r())
        while self.too_close(color):
            color = (r(), r(), r())
        self.color_storage.append(color)
        return color


class Action(Enum):
    delete = 0
    create = 1


Update = namedtuple(
    'Update',
    [
        't',
        'action',
        'i',
        'j',
        'color',
    ]
)


class Drawer(object):
    logger = get_logger(__name__)

    def __init__(self):
        self.color_generator = RandomColorGenerator()

    def create_updates(self, search_results):
        updates = []
        for search_result in search_results:
            color = self.color_generator.generate()
            for i in range(len(search_result.lppath)):
                node = search_result.lppath[i]
                updates.append(
                    Update(t=node.t, action=Action.create.value, j=node.j, i=node.i, color=color)
                )
                if i > 0:
                    p = search_result.lppath[i - 1]
                    updates.append(
                        Update(t=node.t, action=Action.delete.value, j=p.j, i=p.i, color=color)
                    )

        updates.sort(key=lambda update: (update.t, update.action))
        return updates

    @staticmethod
    def draw(field, width, height, updates):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        for j in range(width):
            for i in range(height):
                if field[i][j] == OBS:
                    draw.point((j, i), 'black')
                else:
                    draw.point((j, i), 'white')

        step = 0
        for update in updates:
            while step < update.t:
                yield deepcopy(image)
                step += 1

            if update.action == Action.create.value:
                draw.point((update.j, update.i), update.color)
            else:
                draw.point((update.j, update.i), 'white')

        yield deepcopy(image)

    @staticmethod
    def clear():
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')

    def save(self, images):
        self.clear()
        os.mkdir('tmp')
        for i, image in enumerate(images):
            with open("tmp/{i}.png".format(i=i), 'wb') as file:
                image.save(file)

    @staticmethod
    def create_gif(filename):
        frames = []
        for saved_image in sorted(os.listdir('tmp')):
            frames.append(imageio.imread(os.path.join('tmp', saved_image)))
        filename = (filename[:-5] if filename.endswith('.json') else filename) + '_output.gif'
        imageio.mimsave(filename, frames, 'GIF', duration=1)

    def write(self, m, search_results, filename):
        updates = self.create_updates(search_results)

        images = self.draw(m.grid, m.width, m.height, updates)

        self.save(images)

        self.create_gif(filename)

        self.clear()

