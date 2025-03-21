import numpy as np
from dataclasses import dataclass
from .opengl import Camera, BASIS


class Block:
    def __init__(self, pos, attrs: dict):
        self.pos = np.array(pos)
        for key in attrs:
            setattr(self, key, attrs[key])

    def type(self):
        return getattr(self, "type")

    def __setattr__(self, name, value):
        self.__dict__[name] = value


@dataclass
class Item:
    name: str
    crafting_matrix: list


@dataclass
class Itemstack:
    type: Item
    amount: int


class Inventory:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        for item in self.items:
            yield item


class Player:
    def __init__(self, pos):
        self.pos = np.array(pos).astype(np.float32)
        self.inventory = Inventory([])
        self.camera = Camera(60, self.pos, aspect=4 / 3)
        self.speed = 0.1
        self.flying = True

    def displace(self, tvec):
        self.pos += tvec
        self.camera.translate(tvec)

    def move_right(self):
        pass

    def move_left(self):
        pass

    def move_forward(self):
        direction = (
            self.camera.look_dir if self.flying else self.camera.look_dir.dot(BASIS[1])
        )
        self.displace(direction * self.speed)

    def move_backwards(self):
        direction = (
            -self.camera.look_dir if self.flying else -self.camera.look_dir.dot(BASIS[1])
        )
        self.displace(direction * self.speed)
        
    def look(self, theta, azimuth):
        self.camera.yaw(theta)
        self.camera.pitch(azimuth)
        
    # chat is this real?
    def craft(self):
        pass
