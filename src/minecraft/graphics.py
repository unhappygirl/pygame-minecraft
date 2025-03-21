
from .types_ import Block, Player
from .opengl import *


class Renderer:
    block_length = 1
    cube_indices = [
            0, 1, 3,
            1, 2, 3,
            4, 0, 5,
            0, 1, 5,
            2, 6, 5,
            1, 2, 5,
            3, 7, 6,
            2, 3, 6,
            3, 0, 4,
            7, 3, 4,
            4, 7, 6,
            4, 5, 6
        ]
    def __init__(self, player, block_length):
        self.player = player
        self.block_length = block_length
        self.opengl = OpenGLController(self.player.camera)
        
    @classmethod
    def block_vertices(cls, topleft):
        l = cls.block_length
        v = [
            topleft,
            topleft + [l, 0, 0],
            topleft + [l, 0, l],
            topleft + [0, 0, l],
            topleft + [0, -l, 0],
            topleft + [l, -l, 0],
            topleft + [l, -l, l],
            topleft + [0, -l, l],
        ]
        return v
           
    @classmethod
    def block_indices(cls, offset):
        return [i + offset for i in cls.cube_indices]

                
    def init_blocks(self, blocks: list):
        bl = len(blocks)
        self.vertices = np.array(
            flatten([Renderer.block_vertices(block.pos) for block in blocks]), dtype=np.float32)
        self.indices = np.array(
            flatten([Renderer.block_indices(i * 8) for i in range(bl)]), dtype=np.uint32)
        
    
    def render_blocks(self):
        # block.pos must be top-left
        self.opengl.indexed_draw(GL_TRIANGLES, self.vertices, self.indices)
        # todo: texturing and lighting
        
    def render_sun():
        pass
    
    def render_clouds() :
        pass
    