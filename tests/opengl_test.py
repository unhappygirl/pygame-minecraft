
import pygame
from OpenGL.GL import *
from src.minecraft.opengl import Camera, OpenGLController 
import os
import sys

print("PYOPENGL_PLATFORM:", os.environ.get("PYOPENGL_PLATFORM"))


def main():
    dimensions = (800, 600)
    pygame.display.set_mode(dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
    camera = Camera(fov=60, pos=[0, 0, 8], look_dir=[0, 0, -1], aspect=dimensions[0] / dimensions[1])
    controller = OpenGLController(camera)
    controller.settings()
    clock = pygame.time.Clock()
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL Error: {error}")
        quit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
        controller.test_draw()
        pygame.display.flip()
        #print(controller.view)
        #print(controller.perspective.tolist())
        #print(controller.camera.pos)
        #print(controller.camera.look_dir)
        #controller.camera.translate([0.1, 0, 0.01])
        clock.tick(120)


if __name__ == "__main__":
    main()