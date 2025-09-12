from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos, pi
import random
from config import Config

def draw_forest_sky(self):
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
def draw_extended_ground(self):
    """Desenha terreno estendido ao redor do campo jogável"""
    # Terreno mais escuro ao redor do campo principal
    glColor3f(0.1, 0.4, 0.1)  # Verde mais escuro
    
    field_size = Config.CAMPO_METADE
    extended_size = 25.0
    
    # Terreno estendido - 4 retângulos ao redor do campo principal
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
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y1, z1) 
        glVertex3f(x2, y2, z2)
        glVertex3f(x1, y2, z2)
        glEnd()
def draw_trees(self):
    """Desenha árvores decorativas (cenário floresta) - MAIS PRÓXIMAS"""
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

def draw_snow_sky(self):
        """Skybox nevado - céu cinzento"""
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

def draw_snow_mountains(self):
    """Montanhas nevadas"""
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
def draw_snow_ground(self):
    """Chão nevado"""
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
def draw_snow_elements(self):
    """Bonecos de neve, pinheiros nevados e ursos polares - MAIS PRÓXIMOS"""
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
            draw_snowman(self)
        elif element_type == 1:  # Pinheiro nevado
            draw_snowy_pine(self)
        else:  # Urso polar ou iglu
            if i % 6 == 2:  # Urso polar
                draw_polar_bear(self)
            else:  # Iglu
                draw_igloo(self)
        
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


def draw_beach_sky(self):
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
        
        # Céu tropical - azul claro
        glColor3f(0.7, 0.9, 1.0)  # Azul tropical
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.7, 1.0)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.7, 1.0)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.7, 1.0)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.7, 1.0)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        glColor3f(0.2, 0.6, 0.9)
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

def draw_beach_horizon(self):
    """Mar ao fundo"""
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.2, 0.5, 0.8)  # Azul oceano
    
    # Oceano ao fundo
    ocean_distance = 30
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, ocean_distance)
    glVertex3f(50, 0, ocean_distance)
    glVertex3f(50, 5, ocean_distance + 20)
    glVertex3f(-50, 5, ocean_distance + 20)
    glEnd()
def draw_beach_ground(self):
    """Areia da praia"""
    glColor3f(0.9, 0.85, 0.7)  # Areia clara
    
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
def draw_beach_elements(self):
    """Palmeiras e elementos tropicais - PRÓXIMOS"""
    glDisable(GL_TEXTURE_2D)
    
    # Palmeiras mais próximas
    palm_positions = [
        (-9, 0, -6), (10, 0, -8), (-11, 0, 8), 
        (9, 0, 10), (-7, 0, 12), (8, 0, 11),
        (-8, 0, -10), (11, 0, -9), (7, 0, 13)
    ]
    
    for x, y, z in palm_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Tronco curvado
        glColor3f(0.6, 0.4, 0.2)  # Marrom claro
        glPushMatrix()
        glTranslatef(0, 3, 0)
        glRotatef(15, 1, 0, 0)  # Curva leve
        glScalef(0.4, 6, 0.4)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Folhas no topo
        glColor3f(0.2, 0.7, 0.2)  # Verde tropical
        leaf_angles = [0, 60, 120, 180, 240, 300]
        for angle in leaf_angles:
            glPushMatrix()
            glTranslatef(0, 6, 0)
            glRotatef(angle, 0, 1, 0)
            glTranslatef(1.5, 0, 0)
            glScalef(3, 0.2, 0.8)
            glutSolidCube(1.0)
            glPopMatrix()
        
        glPopMatrix()

def draw_desert_ground(self):
    """Desenha areia ao redor do campo"""
    glColor3f(0.9, 0.8, 0.5)  # Areia mais clara
    
    field_size = Config.CAMPO_METADE
    extended_size = 25.0
    
    # Areia ao redor do campo
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
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y1, z1) 
        glVertex3f(x2, y2, z2)
        glVertex3f(x1, y2, z2)
        glEnd()


def draw_desert_sky(self):
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
        
        # Céu do deserto - tons de laranja/amarelo
        # Face Norte
        glColor3f(1.0, 0.8, 0.6)  # Laranja claro no horizonte
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.4, 0.6, 0.9)   # Azul no topo
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        # Face Sul
        glColor3f(1.0, 0.8, 0.6)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.4, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        # Face Oeste
        glColor3f(1.0, 0.8, 0.6)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.4, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        # Face Leste
        glColor3f(1.0, 0.8, 0.6)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.4, 0.6, 0.9)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        # Topo
        glColor3f(0.3, 0.6, 0.8)
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        glPopMatrix()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

def draw_desert_dunes(self):
    """Desenha dunas de areia no horizonte"""
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.9, 0.8, 0.6)  # Cor de areia
    
    # Dunas no horizonte (formato mais suave que montanhas)
    dunes = [
        # Duna 1
        [(-35, 0, -30), (-25, 4, -32), (-15, 0, -34)],
        # Duna 2
        [(-10, 0, -35), (5, 6, -37), (20, 0, -39)],
        # Duna 3  
        [(25, 0, -40), (40, 8, -38), (50, 0, -36)],
        # Dunas de trás
        [(-20, 0, 32), (-5, 3, 30), (10, 0, 28)],
        [(15, 0, 35), (30, 5, 33), (45, 0, 31)]
    ]
    
    for dune in dunes:
        glBegin(GL_TRIANGLES)
        for point in dune:
            glVertex3f(*point)
        glEnd()

def draw_desert_elements(self):
    """Desenha cactos e elementos do deserto - MAIS PRÓXIMOS"""
    glDisable(GL_TEXTURE_2D)
    
    # Cactos mais próximos do campo
    cacti_positions = [
        (-10, 0, -7), (11, 0, -9), (-12, 0, 8), 
        (13, 0, 6), (-8, 0, 14), (9, 0, 12),
        (-7, 0, -12), (15, 0, -8), (-9, 0, -10),
        (8, 0, 15), (12, 0, -11), (-11, 0, 10)
    ]
    
    for x, y, z in cacti_positions:
        # Culling simples
        distance_to_ball = ((x - self.game.ball.pos.x)**2 + (z - self.game.ball.pos.z)**2)**0.5
        if distance_to_ball > 25:  # Reduzido de 40 para 25
            continue
            
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Corpo principal do cacto
        glColor3f(0.2, 0.6, 0.2)  # Verde escuro
        glPushMatrix()
        glTranslatef(0, 2, 0)
        glScalef(0.8, 4, 0.8)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Braços do cacto
        glPushMatrix()
        glTranslatef(-1.2, 2.5, 0)
        glScalef(0.5, 2, 0.5)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(1.2, 1.8, 0)
        glScalef(0.5, 1.5, 0.5)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPopMatrix()