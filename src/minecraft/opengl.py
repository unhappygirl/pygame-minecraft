from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyglm import glm
import numpy as np
import math


# BASIS for the 3D euclidean space
BASIS = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def flatten(l: list):
    return [item for sublist in l for item in sublist]


class Camera:
    def __init__(self, fov, pos, aspect, far=100.0, near=0.1):
        self.fov = math.radians(fov)
        self.aspect = aspect
        self.pos = np.array(pos).astype(np.float32)
        self.axes = [np.array(BASIS[i]).astype(np.float32) for i in range(3)]  
        self.look_dir = self.axes[2]       
        self.twist = np.array([0.0, 1.0, 0.0]).astype(np.float32)
        self.far = far
        self.near = near

    def translate(self, tvec):
        self.pos += tvec

    def ascend(self, units):
        self.pos += np.array([0, units, 0])

    def rotate(self, axis, angle):
        self.look_dir = glm.rotate(self.look_dir, angle, axis)
        self.axes = [glm.rotate(ax, angle, axis) for ax in self.axes]

    def yaw(self, angle):
        self.rotate(self.axes[1], angle=angle)

    def pitch(self, angle):
        self.rotate(self.axes[0], angle=angle)

    def view(self):
        return glm.lookAt(
            self.pos.tolist(),
            (self.pos + self.look_dir).tolist(),
            self.twist.tolist(),
        )

    def perspective(self):
        return glm.perspective(self.fov, self.aspect, self.near, self.far)


class OpenGLController:
    vertex_shader = """

        #version 330 core

        layout(location = 0) in vec3 position;

        uniform mat4 mvp;
        out vec3 vertexPos;

        void main() {
            gl_Position = mvp * vec4(position, 1.0);
            vertexPos = position;
        }
    """
    
    geometry_shader = """
    
        #version 330 core
        
        layout (triangles) in;
        layout(triangle_strip, max_vertices = 3) out;
        
        in vec3 vertexPos[];
        out vec3 fNormal;
        
        void main() {
            vec3 edge1 = vertexPos[1] - vertexPos[0];
            vec3 edge2 = vertexPos[0] - vertexPos[2];
            vec3 normal = normalize(cross(edge1, edge2));
            for (int i = 0; i < 3; i++) {
                fNormal = normal;
                gl_Position = gl_in[i].gl_Position;
                EmitVertex();
            }
            EndPrimitive();
        }
    """

    fragment_shader = """
        
        #version 330 core

        out vec4 FragColor;
        in vec3 fNormal;
        
        uniform vec3 lightDir;
        
        float diffuse;
        float ambience = 0.2;
        
        void main() {
            diffuse = max(dot(-normalize(lightDir), fNormal), 0.0);
            FragColor = (ambience + diffuse) * vec4(1.0, 1.0, 0.0, 1.0); 
        }
    """

    def __init__(self, camera, dimensions=(800, 600)):
        # glViewport(0, 0, dimensions[0], dimensions[1])
        self.init_shaders()
        self.init_program()
        self.init_buffers()
        self.camera = camera
        self.get_matrices()
        self.set_directional_light(np.array([1, -0.5, -1]))

    def init_buffers(self):
        self.vertex_buffer = glGenBuffers(1)
        self.index_buffer = glGenBuffers(1)
        self.normal_buffer = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)

    def init_shaders(self):
        self.vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertex_shader, self.__class__.vertex_shader)
        glCompileShader(self.vertex_shader)
        self.fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragment_shader, self.__class__.fragment_shader)
        glCompileShader(self.fragment_shader)
        self.geometry_shader = glCreateShader(GL_GEOMETRY_SHADER)
        glShaderSource(self.geometry_shader, self.__class__.geometry_shader)
        glCompileShader(self.geometry_shader)

    def get_matrices(self):
        self.view = self.camera.view()
        self.perspective = self.camera.perspective()

    def set_directional_light(self, direction: np.ndarray):
        glUniform3fv(glGetUniformLocation(self.program, "lightDir"), 1, direction)

    def init_program(self):
        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glAttachShader(self.program, self.geometry_shader)
        glLinkProgram(self.program)

        # Check for linking errors
        link_status = glGetProgramiv(self.program, GL_LINK_STATUS)
        if not link_status:
            info_log = glGetProgramInfoLog(self.program)
            raise RuntimeError(f"Program linking failed: {info_log}")

        glUseProgram(self.program)

    def populate_vertex_buffer(self, vertices):
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    def populate_index_buffer(self, indices):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        
    def populate_normal_buffer(self, normals):
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, normals, GL_STATIC_DRAW)

    def set_matrices(self):
        self.get_matrices()
        model = glm.identity(glm.mat4)
        mvp = self.perspective * self.view * model
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "mvp"),
            1,
            GL_FALSE,
            glm.value_ptr(mvp),
        )

    def settings(self):
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D) 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glCullFace(GL_BACK)  # Enable backface culling
        glClearColor(0.1, 0.1, 0.1, 1)

    def indexed_draw(self, mode, vertices, indices):
        self.set_matrices()
        glBindVertexArray(self.vao)
        self.populate_index_buffer(indices)
        self.populate_vertex_buffer(vertices)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawElements(mode, len(indices), GL_UNSIGNED_INT, None)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)

    def draw_arrays(self, mode, vertices, normals):
        self.set_matrices()
        self.populate_normal_buffer(normals)
        self.populate_vertex_buffer(vertices)
        glBindVertexArray(self.vao)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(mode, 0, len(vertices) // 3)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)

