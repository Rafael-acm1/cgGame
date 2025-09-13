from .base import BaseScenario
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from config import Config

class SnowScenario(BaseScenario):
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
        
        # Céu nevado - tons de cinza e branco
        # Face Norte
        glColor3f(0.9, 0.9, 0.95)  # Branco acinzentado
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.7, 0.7, 0.8)   # Cinza claro
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        # Outras faces iguais
        glColor3f(0.9, 0.9, 0.95)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.7, 0.7, 0.8)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        glColor3f(0.9, 0.9, 0.95)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.7, 0.7, 0.8)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        glColor3f(0.9, 0.9, 0.95)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.7, 0.7, 0.8)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        # Topo
        glColor3f(0.6, 0.6, 0.7)
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
        glColor3f(0.95, 0.95, 1.0)  # Branco com leve azul
        
        mountains = [
            [(-30, 0, -25), (-20, 12, -27), (-10, 0, -29)],
            [(-5, 0, -30), (8, 15, -32), (20, 0, -34)],
            [(25, 0, -35), (40, 18, -33), (50, 0, -31)],
            [(-15, 0, 28), (-3, 8, 26), (10, 0, 24)],
            [(15, 0, 30), (32, 14, 28), (45, 0, 26)]
        ]
        
        for mountain in mountains:
            glBegin(GL_TRIANGLES)
            for point in mountain:
                glVertex3f(*point)
            glEnd()

    def draw_ground(self):
        glColor3f(0.92, 0.92, 0.96)  # Branco neve
        
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
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y1, z1) 
            glVertex3f(x2, y2, z2)
            glVertex3f(x1, y2, z2)
            glEnd()

    def draw_elements(self):
        glDisable(GL_TEXTURE_2D)
        
        # Posições misturadas para diferentes elementos
        element_positions = [
            (-10, 0, -8), (12, 0, -10), (-15, 0, 9), 
            (14, 0, 8), (-8, 0, 15), (9, 0, 13),
            (-6, 0, -12), (16, 0, -6), (-12, 0, -14),
            (11, 0, -12), (8, 0, -9), (-9, 0, 11)
        ]
        
        for i, (x, y, z) in enumerate(element_positions):
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Alterna entre diferentes elementos baseado no índice
            element_type = i % 3
            
            if element_type == 0:  # Boneco de neve
                self.draw_snowman()
            elif element_type == 1:  # Pinheiro nevado
                self.draw_snowy_pine()
            else:  # Urso polar ou iglu
                if i % 6 == 2:  # Urso polar
                    self.draw_polar_bear()
                else:  # Iglu
                    self.draw_igloo()
            
            glPopMatrix()

    def draw_snowman(self):
        """Desenha um boneco de neve completo"""
        # Corpo (3 esferas)
        glColor3f(0.95, 0.95, 1.0)  # Branco neve
        
        # Base (maior)
        glPushMatrix()
        glTranslatef(0, 0.8, 0)
        glutSolidSphere(0.8, 8, 6)
        glPopMatrix()
        
        # Meio
        glPushMatrix()
        glTranslatef(0, 2.2, 0)
        glutSolidSphere(0.6, 8, 6)
        glPopMatrix()
        
        # Cabeça
        glPushMatrix()
        glTranslatef(0, 3.4, 0)
        glutSolidSphere(0.5, 8, 6)
        glPopMatrix()
        
        # Chapéu
        glColor3f(0.1, 0.1, 0.1)  # Preto
        glPushMatrix()
        glTranslatef(0, 3.9, 0)
        glScalef(0.8, 0.6, 0.8)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Cenoura (nariz)
        glColor3f(1.0, 0.5, 0.0)  # Laranja
        glPushMatrix()
        glTranslatef(0, 3.4, 0.5)
        glRotatef(90, 1, 0, 0)
        glutSolidCone(0.1, 0.4, 4, 1)
        glPopMatrix()
        
        # Botões
        glColor3f(0.1, 0.1, 0.1)  # Preto
        button_positions = [(0, 2.4, 0.6), (0, 2.0, 0.6), (0, 1.6, 0.6)]
        for bx, by, bz in button_positions:
            glPushMatrix()
            glTranslatef(bx, by, bz)
            glutSolidSphere(0.08, 4, 3)
            glPopMatrix()
            
    def draw_snowy_pine(self):
        """Desenha pinheiro coberto de neve"""
        # Tronco marrom
        glColor3f(0.4, 0.2, 0.1)
        glPushMatrix()
        glTranslatef(0, 1, 0)
        glScalef(0.3, 2, 0.3)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # 3 níveis de copa com neve
        for level in range(3):
            # Copa verde escura (base)
            glColor3f(0.05, 0.2, 0.05)  # Verde bem escuro
            glPushMatrix()
            glTranslatef(0, 2.5 + level * 0.8, 0)
            scale = 1.5 - (level * 0.3)
            glScalef(scale, 0.8, scale)
            glutSolidCone(1.0, 1.0, 6, 1)
            glPopMatrix()
            
            # Neve por cima
            glColor3f(0.95, 0.95, 1.0)  # Branco neve
            glPushMatrix()
            glTranslatef(0, 2.9 + level * 0.8, 0)
            scale_snow = (1.5 - (level * 0.3)) * 0.8
            glScalef(scale_snow, 0.3, scale_snow)
            glutSolidCone(1.0, 1.0, 6, 1)
            glPopMatrix()

    def draw_polar_bear(self):
        """Desenha um urso polar simples"""
        glColor3f(0.95, 0.95, 0.98)  # Branco levemente amarelado
        
        # Corpo principal
        glPushMatrix()
        glTranslatef(0, 0.8, 0)
        glScalef(1.2, 0.8, 2.0)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Cabeça
        glPushMatrix()
        glTranslatef(0, 1.2, 1.2)
        glScalef(0.8, 0.7, 0.8)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Orelhas
        ear_positions = [(-0.3, 1.5, 1.2), (0.3, 1.5, 1.2)]
        for ex, ey, ez in ear_positions:
            glPushMatrix()
            glTranslatef(ex, ey, ez)
            glutSolidSphere(0.15, 4, 3)
            glPopMatrix()
        
        # Patas
        paw_positions = [(-0.4, 0.2, 0.6), (0.4, 0.2, 0.6), (-0.4, 0.2, -0.6), (0.4, 0.2, -0.6)]
        for px, py, pz in paw_positions:
            glPushMatrix()
            glTranslatef(px, py, pz)
            glScalef(0.3, 0.4, 0.3)
            glutSolidCube(1.0)
            glPopMatrix()

    def draw_igloo(self):
        """Desenha um iglu simples"""
        glColor3f(0.9, 0.9, 0.95)  # Branco gelo
        
        # Dome principal
        glPushMatrix()
        glTranslatef(0, 0.8, 0)
        glScalef(1.0, 0.8, 1.0)
        glutSolidSphere(1.0, 8, 6)
        glPopMatrix()
        
        # Entrada (buraco escuro)
        glColor3f(0.1, 0.1, 0.2)  # Azul muito escuro
        glPushMatrix()
        glTranslatef(0, 0.4, 0.9)
        glScalef(0.4, 0.6, 0.2)
        glutSolidCube(1.0)
        glPopMatrix()
