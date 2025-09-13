from .base import BaseScenario
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config import Config

class ForestScenario(BaseScenario):
    def draw(self):
        self.draw_sky()
        self.draw_mountains()
        self.draw_ground()
        self.draw_elements()

    def draw_sky(self):
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
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glColor3f(0.2, 0.5, 0.8)
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        glEnd()
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_mountains(self):
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.4, 0.5, 0.6)  
        
        mountains = [
            [(-40, 0, -35), (-30, 8, -35), (-20, 0, -35)],
            [(-25, 0, -40), (-15, 12, -40), (-5, 0, -40)],
            [(0, 0, -38), (8, 10, -38), (16, 0, -38)],
            [(20, 0, -42), (35, 15, -42), (50, 0, -42)],
            [(-15, 0, 35), (-5, 6, 35), (5, 0, 35)],
            [(10, 0, 38), (25, 9, 38), (40, 0, 38)]
        ]
        
        for mountain in mountains:
            glBegin(GL_TRIANGLES)
            for point in mountain:
                glVertex3f(*point)
            glEnd()

    def draw_ground(self):
        if hasattr(self.renderer, 'textures') and 'grass2' in self.renderer.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.renderer.textures['grass2'])
            glColor3f(1,1,1)
            use_texture = True
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.1, 0.4, 0.1)  
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
                texture_repeat = 2.5  
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
        
        # Árvores mais próximas do campo
        trees_positions = [
            (-9, 0, -8), (10, 0, -10), (-12, 0, 7), 
            (11, 0, 9), (-8, 0, 13), (8, 0, 12),
            (-7, 0, -13), (13, 0, -9), (-10, 0, -11),
            (9, 0, 14), (12, 0, -12), (-11, 0, 8)
        ]
        
        for x, y, z in trees_positions:
            # Culling simples - só desenha árvores que estão relativamente próximas
            distance_to_ball = ((x - self.game.ball.pos.x)**2 + (z - self.game.ball.pos.z)**2)**0.5
            if distance_to_ball > 25:  # Reduzido de 40 para 25
                continue
                
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Tronco
            glColor3f(0.4, 0.2, 0.1)  # Marrom
            glPushMatrix()
            glTranslatef(0, 1.5, 0)
            glScalef(0.3, 3.0, 0.3)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Copa (usando uma versão mais simples)
            glColor3f(0.1, 0.5, 0.1)  # Verde escuro
            glTranslatef(0, 3.5, 0)
            glutSolidSphere(1.5, 6, 4)  # Menos polígonos para melhor performance
            
            glPopMatrix()