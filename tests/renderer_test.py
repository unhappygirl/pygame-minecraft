
import cProfile
import pstats
import pygame
from OpenGL.GL import *
from src.minecraft.graphics import Renderer
from src.minecraft.types_ import *
from src.minecraft.maps import MapGenerator
import math


def main():
    mapgen = MapGenerator((100, 60), octaves=3.5, scaler=20)
    
    dimensions = (800, 600)
    pygame.display.set_mode(dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
    player = Player([0, 0, 0])
    renderer = Renderer(player, 1)
    renderer.opengl.settings()
    blocks = mapgen.blocks()
    #mapgen.generate_trees(([0, 20], [0, 20]), 2)
    renderer.init_blocks(blocks)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        kevent = pygame.key.get_pressed()
                
        if kevent[pygame.K_w]:
            player.move_forward()
        
        if kevent[pygame.K_s]:
            player.move_backwards()
        
        if kevent[pygame.K_a]:
            player.displace([0.1, 0, 0])
            
        if kevent[pygame.K_d]:
            player.displace([-0.1, 0, 0])
        
        if kevent[pygame.K_SPACE]:
            player.camera.ascend(0.1)
            
        dx, dy = pygame.mouse.get_rel()
        player.look(-math.radians(dx)/3, math.radians(dy)/3)
        print(player.camera.axes)
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        renderer.render_blocks()
        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    try:
        cProfile.run("main()", sort="cumtime", filename="minecraft.prof")
    finally:
        with open("profiler.txt", "w") as f:
            stats = pstats.Stats("minecraft.prof", stream=f)
            stats.strip_dirs().sort_stats("time").print_stats()
