from perlin_noise import PerlinNoise
import numpy as np
import random
from .types_ import Block


# A biome is a part of a map
class Biome:
    def __init__(self, name, tree_density, mountains):
        # tree density is tree amount per 50 blocks^2
        self.tree_density = tree_density
        self.mountains = mountains
        self.name = name

    def generation_procedure(self):
        pass


class Plain(Biome):
    def __init__(self):
        pass


# Theory: a map is an array of block objects,
# the spatial ordering is obtained by the inherent attributes of the block objects.


class Map:
    def __init__(self, blocks, hmap):
        self.blocks = blocks
        self.height_map = hmap

    def block_at(self, x, y, z):
        return


class MapGenerator:
    block_length = 1

    def __init__(self, map_dimensions, octaves=8, seed=None, scaler=20):
        self.map_dimensions = map_dimensions
        self.noise_gen = PerlinNoise(octaves=octaves, seed=seed)
        self.init_height_map(scaler)

    @classmethod
    def square_around(cls, pos, length=1):
        return [
            [
                pos + (cls.block_length * i, 0, 0),
                pos + (-cls.block_length * i, 0, 0),
                pos + (cls.block_length * i, 0, cls.block_length * i),
                pos + (-cls.block_length * i, 0, -cls.block_length * i),
                pos + (0, 0, cls.block_length * i),
                pos + (0, 0, -cls.block_length * i),
            ]
            for i in range(length)
        ]

    def init_height_map(self, scaler):
        w, h = self.map_dimensions
        self.hmap = dict()
        for x in range(1, w + 1):
            for y in range(1, h + 1):
                self.hmap[(x, y)] = np.array((x, y, self.noise_gen([x / w, y / h]) * scaler))

    def choose_terrain(self, biome, coor):
        return {}

    def blocks(self):
        blocks = list()
        w, h = self.map_dimensions
        for coor in self.hmap.values():
            x, y, height = coor
            for i in range(-h // 2, int(height)):
                # todo: add block types
                blocks.append(
                    Block(
                        [x, (i + 1) * self.block_length, y - self.block_length],
                        self.choose_terrain(None, None),
                    )
                )
        return blocks

    def generate_tree(self, height, block_pos, type_modifier=None):  # Mock
        log = [
            Block(block_pos + (0, i * self.block_length, 0), {"type": "oak_wood"})
            for i in range(1, height + 1)
        ]
        leaf_start = log[4].block_pos
        leaves = [
            Block(pos, {"type": "oak_leaf"})
            for pos in self.square_around(leaf_start, length=2)
        ] + [
            Block(pos, {"type": "oak_leaf"})
            for pos in self.square_around(leaf_start, length=1)
        ]
        return log + leaves

    def generate_trees(self, area_interval: list, density):
        xinterval, zinterval = area_interval
        for _ in range(density):
            xoffset = random.randint(0, 10)
            zoffset = random.randint(0, 10)
            for x in random.randrange(
                    xinterval[0] + xoffset, xinterval[1], 12):
                for z in random.randrange(
                    zinterval[0] + zoffset, zinterval[1], 8):
                    self.blocks += \
                        self.generate_tree(
                            random.randint(2, 8), (x, self.hmap[(x, z)], z))
                        
                    
