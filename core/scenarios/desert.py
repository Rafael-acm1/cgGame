from .base import BaseScenario
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config import Config

class DesertScenario(BaseScenario):
    def draw(self):
        self.draw_sky()
        self.draw_dunes()
        self.draw_ground()
        self.draw_elements()

    def draw_sky(self):
        """Skybox do deserto - céu alaranjado"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        glPushMatrix()

        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        glTranslatef(cam_x, 0, cam_z)

        size = 80
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.8, 0.6)
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.4, 0.6, 0.9)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        glEnd()
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_dunes(self):
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.9, 0.8, 0.6)
        dunes = [
            [(-35, 0, -30), (-25, 4, -32), (-15, 0, -34)],
            [(-10, 0, -35), (5, 6, -37), (20, 0, -39)],
            [(25, 0, -40), (40, 8, -38), (50, 0, -36)],
        ]
        for dune in dunes:
            glBegin(GL_TRIANGLES)
            for point in dune:
                glVertex3f(*point)
            glEnd()

    def draw_ground(self):
        if hasattr(self.renderer, 'textures') and 'sand' in self.renderer.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.renderer.textures['sand'])
            glColor3f(1,1,1)  
            use_texture = True
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.9, 0.8, 0.5)  
            use_texture = False
    
        field_size = Config.CAMPO_METADE
        extended_size = 25.0

        regions = [
            # Norte
            [(-extended_size, 0, field_size), (extended_size, 0, extended_size)],
            # Sul  
            [(-extended_size, 0, -extended_size), (extended_size, 0, -field_size)],
            # Leste
            [(field_size, 0, -field_size), (extended_size, 0, field_size)],
            # Oeste
            [(-extended_size, 0, -field_size), (-field_size, 0, field_size)]
        ]

        for (x1, y1, z1), (x2, y2, z2) in regions:
            glBegin(GL_QUADS)
            if use_texture:
                texture_repeat = 3.0  # Quantas vezes a textura vai repetir (maior para mais detalhes na areia)
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
        glDisable(GL_TEXTURE_2D)
        cacti_positions = [(-10, 0, -7), (11, 0, -9), (-12, 0, 8)]
        for x, y, z in cacti_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            glColor3f(0.2, 0.6, 0.2)
            glPushMatrix()
            glTranslatef(0, 2, 0)
            glScalef(0.8, 4, 0.8)
            glutSolidCube(1.0)
            glPopMatrix()
            glPopMatrix()
