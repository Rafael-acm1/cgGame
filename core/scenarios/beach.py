from .base import BaseScenario
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config import Config

class BeachScenario(BaseScenario):
    def draw(self):
        self.draw_sky()
        self.draw_horizon()
        self.draw_ground()
        self.draw_elements()

    def draw_sky(self):
        """Skybox tropical"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        
        glPushMatrix()
        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        glTranslatef(cam_x, 0, cam_z)
        
        size = 80
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.7, 1.0)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        glEnd()
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_horizon(self):
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.2, 0.5, 0.8)
        glBegin(GL_QUADS)
        glVertex3f(-50, 0, 30)
        glVertex3f(50, 0, 30)
        glVertex3f(50, 5, 50)
        glVertex3f(-50, 5, 50)
        glEnd()

    def draw_ground(self):
        if hasattr(self.renderer, 'textures') and 'beachSand' in self.renderer.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.renderer.textures['beachSand'])
            glColor3f(1,1,1)
            use_texture = True
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.9, 0.85, 0.7)  
            use_texture = False

        field_size = Config.CAMPO_METADE
        extended_size = 20.0

        regions = [
            [(-extended_size, 0, field_size), (extended_size, 0, extended_size)],
            [(-extended_size, 0, -extended_size), (extended_size, 0, -field_size)],
            [(field_size, 0, -field_size), (extended_size, 0, field_size)],
            [(-extended_size, 0, -field_size), (-field_size, 0, field_size)]
        ]

        for (x1, y1, z1), (x2, y2, z2) in regions:
            glBegin(GL_QUADS)
            if use_texture:
                texture_repeat = 2.8
                glTexCoord2f(0, 0); glVertex3f(x1, y1, z1)
                glTexCoord2f(texture_repeat, 0); glVertex3f(x2, y1, z1) 
                glTexCoord2f(texture_repeat, texture_repeat); glVertex3f(x2, y2, z2)
                glTexCoord2f(0, texture_repeat); glVertex3f(x1, y2, z2)
            else:
                glVertex3f(x1, y1, z1)
                glVertex3f(x2, y1, z1) 
                glVertex3f(x2, y2, z2)
                glVertex3f(x1, y2, z2)
            glEnd()

        if use_texture:
            glDisable(GL_TEXTURE_2D)

    def draw_elements(self):
        """Palmeiras"""
        glDisable(GL_TEXTURE_2D)
        palm_positions = [(-9, 0, -6), (10, 0, -8), (-11, 0, 8)]
        for x, y, z in palm_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            glColor3f(0.6, 0.4, 0.2)
            glPushMatrix()
            glTranslatef(0, 3, 0)
            glScalef(0.4, 6, 0.4)
            glutSolidCube(1.0)
            glPopMatrix()
            glPopMatrix()
