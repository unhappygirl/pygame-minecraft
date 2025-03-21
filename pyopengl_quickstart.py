import glfw
import numpy as np
import glm
from OpenGL.GL import *

# Vertex Shader
VERTEX_SHADER_SRC = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 vertexColor;

uniform mat4 mvp;

void main() {
    gl_Position = mvp * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""

# Fragment Shader
FRAGMENT_SHADER_SRC = """
#version 330 core
in vec3 vertexColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(vertexColor, 1.0);
}
"""

# Cube vertex data (positions + colors)
vertices = np.array([
    # Positions       # Colors
    -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
     0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
     0.5,  0.5, -0.5,  0.0, 0.0, 1.0,
    -0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
    -0.5, -0.5,  0.5,  1.0, 0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 0.0, 0.0,
], dtype=np.float32)

# Index buffer (EBO) for drawing a cube using GL_TRIANGLES
indices = np.array([
    0, 1, 2, 2, 3, 0,  # Back face
    4, 5, 6, 6, 7, 4,  # Front face
    0, 1, 5, 5, 4, 0,  # Bottom face
    3, 2, 6, 6, 7, 3,  # Top face
    0, 3, 7, 7, 4, 0,  # Left face
    1, 2, 6, 6, 5, 1,  # Right face
], dtype=np.uint32)


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader)
        raise RuntimeError(f"Shader compilation failed: {error.decode()}")

    return shader


def create_shader_program():
    vertex_shader = compile_shader(VERTEX_SHADER_SRC, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(FRAGMENT_SHADER_SRC, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program)
        raise RuntimeError(f"Shader linking failed: {error.decode()}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def main():
    # Initialize GLFW and create a GLX window
    if not glfw.init():
        raise RuntimeError("GLFW initialization failed")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "GLX Modern OpenGL", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("GLFW window creation failed")

    glfw.make_context_current(window)

    # Create VAO, VBO, and EBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    # Bind and fill VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Bind and fill EBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Enable vertex attributes (position + color)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    # Create shader program
    shader_program = create_shader_program()

    # Enable depth test
    glEnable(GL_DEPTH_TEST)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Clear screen
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Compute MVP matrix
        model = glm.rotate(glm.mat4(1.0), glfw.get_time(), glm.vec3(0.0, 1.0, 0.0))
        view = glm.lookAt(glm.vec3(2, 2, 2), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 10.0)
        mvp = projection * view * model

        # Use shader and set uniform
        glUseProgram(shader_program)
        mvp_location = glGetUniformLocation(shader_program, "mvp")
        glUniformMatrix4fv(mvp_location, 1, GL_FALSE, glm.value_ptr(mvp))

        # Bind VAO and draw
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    # Cleanup
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader_program)

    glfw.terminate()


if __name__ == "__main__":
    main()
