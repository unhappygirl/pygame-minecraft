# from ..minecraft.opengl import *
from PIL import Image
import os
import sys

NAME = os.path.basename(sys.modules[__name__].__file__)

TEXTURES = {
    "grassblock": (),
    "dirt": [],
    "stone": [],
    "dirt_block": [],
    "dirt_block": [],
    "wood_oak": [],
}

def index_to_atlas(x, y):
    return (16*x, 16*y)


class TextureLoader:
    image_formats = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]

    def __init__(self, directory="."):
        self.directory = directory
        self.images = dict()
        self.load()
        self.block_atlas = self.images["block_atlas.png"]

    def load(self):
        for entry in os.scandir(self.directory):
            if entry.name == NAME:
                continue
            absolute = os.path.join(self.directory, entry.name)
            _, ext = os.path.splitext(entry.name)
            if self.__class__.valid_ext(ext):
                im = Image.open(absolute)
                self.images[entry.name] = im
                
    def scale_to(self, size):
        pass
        

    @classmethod
    def valid_ext(cls, ext):
        return ext in cls.image_formats


def main():
    myloader = TextureLoader()
    myloader.load()
    start = index_to_atlas(11, 11)
    end = (start[0] + 16, start[1] + 16)
    myloader.block_atlas.crop((*start, *end)).save(open("cus.png", "wb"))


if __name__ == "__main__":
    main()
