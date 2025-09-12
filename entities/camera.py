from OpenGL.GLU import *
from OpenGL.GL import *
from math import radians, sin, cos
from entities.ball import Ball

class Camera:
    MODES = ['cenario', 'bola']

    def __init__(self):
        self.mode_index = 0
        self.h_angle = 0.0
        self.v_angle = 20.0

    def toggle_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.MODES)

    def mode(self):
        return self.MODES[self.mode_index]

    def setup(self, ball: Ball):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        if self.mode() == 'cenario':
            olho = (10.0*sin(radians(35)), 8.5, 10.0*cos(radians(35)))
            gluLookAt(olho[0], olho[1], olho[2], 0.0, 0.0, 0.0, 0,1,0)
        else:
            raio_h = 3.5
            altura_base = 2.0
            altura_offset = sin(radians(self.v_angle)) * 1.5
            rad_h = radians(self.h_angle)
            olho_x = ball.pos.x + raio_h * sin(rad_h)
            olho_z = ball.pos.z + raio_h * cos(rad_h)
            olho_y = ball.radius + altura_base + altura_offset
            gluLookAt(olho_x, olho_y, olho_z, ball.pos.x, ball.radius, ball.pos.z, 0,1,0)