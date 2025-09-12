from math import sin, cos, pi
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from PIL import Image
from config import Config

from utils import ui
 
def load_texture(filepath):      
    img = Image.open(filepath).convert("RGB")
    img_data = img.tobytes("raw", "RGB", 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id
    

class Renderer:
    def __init__(self, game):
        self.game = game
        self.textures = {}
        self.quadric = gluNewQuadric()
        self.menu_buttons = []
        self._ui_prev_depth = None
        
        
        self.scenarios = {
            0: "forest",   
            1: "stadium",  
            2: "desert",   
            3: "snow",     
            4: "volcano",  
            5: "space",   
            6: "beach",     
            7: "city",      
        }
        
    def get_current_scenario(self):
      
        level_index = self.game.level_index
        return self.scenarios.get(level_index, "forest") 

    def initialize_textures(self):
        self.textures['grass'] = load_texture("assets/textures/grass.png")
        

        try:
            self.textures['lava'] = load_texture("assets/textures/lava.png")
            self.textures['volcanic_rock'] = load_texture("assets/textures/volcanic_rock.png")
            self.textures['obsidian'] = load_texture("assets/textures/obsidian.png")
            self.textures['molten_rock'] = load_texture("assets/textures/molten_rock.png")
            print("Texturas carregadas com sucesso!")
        except Exception as e:
            print(f"Algumas texturas não foram encontradas: {e}")

        
    def draw_ground(self):
        if 'grass' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['grass']) 
            glColor3f(1,1,1)
            glBegin(GL_QUADS)
            s = Config.CAMPO_METADE / 2.0
            glTexCoord2f(0,0); glVertex3f(-Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glTexCoord2f(s,0); glVertex3f( Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glTexCoord2f(s,s); glVertex3f( Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glTexCoord2f(0,s); glVertex3f(-Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else: 
            glColor3f(0.05, 0.55, 0.15)
            glBegin(GL_QUADS)
            glVertex3f(-Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glVertex3f( Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glVertex3f( Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glVertex3f(-Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glEnd()

    def draw_hole(self):
        glPushMatrix()
        glTranslatef(self.game.hole_position[0], 0.002, self.game.hole_position[1])
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)
        n = 40
        for i in range(n + 1):
            ang = 2.0 * pi * i / n
            glVertex3f(Config.RAIO_BURACO * cos(ang), 0.0, Config.RAIO_BURACO * sin(ang))
        glEnd()
        glPopMatrix()

    def draw_ball(self):
        b = self.game.ball
        glPushMatrix()
        glTranslatef(b.pos.x, b.pos.y, b.pos.z)
        glColor3f(1.0, 1.0, 1.0)
        glutSolidSphere(b.radius, 24, 24)
        glPopMatrix()
        
    def draw_aim(self):
        b = self.game.ball
        glPushMatrix()
        glTranslatef(b.pos.x, b.radius + 0.05, b.pos.z)
        glRotatef(self.game.aim_angle, 0.0, 1.0, 0.0)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.8)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.05, 0.0, 0.8)
        glVertex3f( 0.05, 0.0, 0.8)
        glVertex3f( 0.0, 0.0, 0.95)
        glEnd()
        glPopMatrix()

    def draw_obstacles(self):
        # Primeiro desenha obstáculos sólidos
        for o in self.game.obstacles:
            if getattr(o, 'type', '') != 'water':
                o.draw()
        
        # Depois desenha obstáculos de água com transparência
        has_water = any(getattr(o, 'type', '') == 'water' for o in self.game.obstacles)
        if has_water:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            for o in self.game.obstacles:
                if getattr(o, 'type', '') == 'water':
                    o.draw()
            glDisable(GL_BLEND)

    def draw_scenario_background(self):
        """Desenha o cenário de fundo baseado no nível atual"""
        scenario = self.get_current_scenario()
        
        if scenario == "forest":
            self.draw_forest_background()
        elif scenario == "stadium":
            self.draw_stadium_background()
        elif scenario == "desert":
            self.draw_desert_background()
        elif scenario == "snow":
            self.draw_snow_background()
        elif scenario == "volcano":
            self.draw_volcano_background()
        elif scenario == "space":
            self.draw_space_background()
        elif scenario == "beach":
            self.draw_beach_background()
        elif scenario == "city":
            self.draw_city_background()
        else:
            # Fallback para floresta se cenário não encontrado
            self.draw_forest_background()
    
    def draw_forest_background(self):
        """Desenha cenário de floresta (original)"""
        self.draw_forest_sky()
        self.draw_mountains()
        self.draw_extended_ground()
        self.draw_trees()
    
    def draw_stadium_background(self):
        """Desenha cenário de estádio de golf"""
        self.draw_stadium_sky()
        self.draw_stadium_stands()
        self.draw_stadium_ground()
        self.draw_stadium_elements()

    def draw_forest_sky(self):
        """Skybox da floresta (atual)"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)  # Céu não deve ter fog
        
        glPushMatrix()
        
        # Pega a posição atual da câmera para centralizar o skybox
        # O skybox deve sempre estar "infinitamente distante"
        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        
        glTranslatef(cam_x, 0, cam_z)  # Centraliza na posição da câmera
        
        size = 80  # Tamanho do skybox
        
        glBegin(GL_QUADS)
        
        # Face Norte (frente)
        glColor3f(0.7, 0.9, 1.0)  # Azul claro no horizonte
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.6, 0.9)   # Azul mais escuro no topo
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        # Face Sul (trás)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        # Face Oeste (esquerda)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        # Face Leste (direita)
        glColor3f(0.7, 0.9, 1.0)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.3, 0.6, 0.9)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        # Topo
        glColor3f(0.2, 0.5, 0.8)  # Azul bem escuro no topo
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        glPopMatrix()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_mountains(self):
        """Desenha montanhas distantes no horizonte"""
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.4, 0.5, 0.6)  # Cor cinza-azulada para montanhas distantes
        
        # Montanhas ao fundo (mais distantes)
        mountains = [
            # Montanha 1 - esquerda
            [(-40, 0, -35), (-30, 8, -35), (-20, 0, -35)],
            # Montanha 2 - centro-esquerda  
            [(-25, 0, -40), (-15, 12, -40), (-5, 0, -40)],
            # Montanha 3 - centro
            [(0, 0, -38), (8, 10, -38), (16, 0, -38)],
            # Montanha 4 - direita
            [(20, 0, -42), (35, 15, -42), (50, 0, -42)],
            # Montanhas de trás
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

    # ===== CENÁRIO ESTÁDIO =====
    def draw_stadium_sky(self):
        """Skybox do estádio - céu mais claro e urbano"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        
        glPushMatrix()
        
        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        glTranslatef(cam_x, 0, cam_z)
        
        size = 80
        
        glBegin(GL_QUADS)
        
        # Céu do estádio - mais claro e limpo para ambiente esportivo
        # Face Norte
        glColor3f(0.85, 0.92, 0.98)  # Azul bem claro, quase branco
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.5, 0.75, 0.95)   # Azul médio-claro
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        # Face Sul
        glColor3f(0.85, 0.92, 0.98)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.5, 0.75, 0.95)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        # Face Oeste
        glColor3f(0.85, 0.92, 0.98)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.5, 0.75, 0.95)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        # Face Leste
        glColor3f(0.85, 0.92, 0.98)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.5, 0.75, 0.95)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        # Topo
        glColor3f(0.4, 0.7, 0.9)  # Azul médio
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        glPopMatrix()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_stadium_stands(self):
        """Desenha arquibancadas modernas do estádio"""
        glDisable(GL_TEXTURE_2D)
        
        # Arquibancadas em formato mais realista com múltiplos níveis
        stand_radius = 28
        stand_height_base = 3
        
        # 4 seções de arquibancadas (Norte, Sul, Leste, Oeste)
        sections = [
            {"center": (0, 0, -stand_radius), "width": 35, "depth": 8},  # Norte
            {"center": (0, 0, stand_radius), "width": 35, "depth": 8},   # Sul
            {"center": (stand_radius, 0, 0), "width": 8, "depth": 35},   # Leste
            {"center": (-stand_radius, 0, 0), "width": 8, "depth": 35}   # Oeste
        ]
        
        for section in sections:
            cx, cy, cz = section["center"]
            width, depth = section["width"], section["depth"]
            
            # Base das arquibancadas (concreto)
            glColor3f(0.85, 0.85, 0.9)  # Cinza claro
            glPushMatrix()
            glTranslatef(cx, stand_height_base, cz)
            glScalef(width, stand_height_base * 2, depth)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Degraus das arquibancadas (3 níveis)
            glColor3f(0.7, 0.7, 0.8)  # Cinza médio para degraus
            for level in range(3):
                step_height = stand_height_base + (level * 1.5)
                step_depth = depth - (level * 1.2)
                
                glPushMatrix()
                glTranslatef(cx, step_height, cz)
                glScalef(width - (level * 2), 0.3, step_depth)
                glutSolidCube(1.0)
                glPopMatrix()
            
            # Cobertura das arquibancadas
            glColor3f(0.2, 0.3, 0.6)  # Azul escuro para teto
            glPushMatrix()
            glTranslatef(cx, stand_height_base + 5, cz)
            glScalef(width + 2, 0.5, depth + 2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Pilares de suporte
            glColor3f(0.6, 0.6, 0.65)  # Cinza para pilares
            pillar_positions = [
                (cx - width//3, 0, cz - depth//3),
                (cx + width//3, 0, cz - depth//3),
                (cx - width//3, 0, cz + depth//3),
                (cx + width//3, 0, cz + depth//3)
            ]
            
            for px, py, pz in pillar_positions:
                if abs(px) < 15 and abs(pz) < 15:  # Não coloca pilares muito próximos do campo
                    continue
                glPushMatrix()
                glTranslatef(px, stand_height_base + 2.5, pz)
                glScalef(1, 5, 1)
                glutSolidCube(1.0)
                glPopMatrix()

    def draw_stadium_ground(self):
        """Desenha piso decorativo do estádio"""
        field_size = Config.CAMPO_METADE
        
        # Pista de corrida ao redor do campo (marrom avermelhado)
        glColor3f(0.6, 0.3, 0.2)  # Marrom avermelhado para pista
        track_inner = field_size + 1
        track_outer = field_size + 3
        
        # Pista circular simplificada (4 retângulos)
        track_regions = [
            # Norte
            [(-track_outer, 0, track_inner), (track_outer, 0, track_outer)],
            # Sul  
            [(-track_outer, 0, -track_outer), (track_outer, 0, -track_inner)],
            # Leste
            [(track_inner, 0, -track_inner), (track_outer, 0, track_inner)],
            # Oeste
            [(-track_outer, 0, -track_inner), (-track_inner, 0, track_inner)]
        ]
        
        for (x1, y1, z1), (x2, y2, z2) in track_regions:
            glBegin(GL_QUADS)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y1, z1) 
            glVertex3f(x2, y2, z2)
            glVertex3f(x1, y2, z2)
            glEnd()
        
        # Área de concreto externa (cinza claro)
        glColor3f(0.75, 0.75, 0.8)  # Cinza claro
        extended_size = 25.0
        
        concrete_regions = [
            # Norte
            [(-extended_size, 0, track_outer), (extended_size, 0, extended_size)],
            # Sul  
            [(-extended_size, 0, -extended_size), (extended_size, 0, -track_outer)],
            # Leste
            [(track_outer, 0, -track_outer), (extended_size, 0, track_outer)],
            # Oeste
            [(-extended_size, 0, -track_outer), (-track_outer, 0, track_outer)]
        ]
        
        for (x1, y1, z1), (x2, y2, z2) in concrete_regions:
            glBegin(GL_QUADS)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y1, z1) 
            glVertex3f(x2, y2, z2)
            glVertex3f(x1, y2, z2)
            glEnd()
            
        # Linhas decorativas na pista
        glColor3f(1.0, 1.0, 1.0)  # Branco para linhas
        glLineWidth(2.0)
        
        # Linhas da pista (simplificadas)
        track_mid = (track_inner + track_outer) / 2
        glBegin(GL_LINES)
        # Linha norte
        glVertex3f(-field_size, 0.01, track_mid)
        glVertex3f(field_size, 0.01, track_mid)
        # Linha sul
        glVertex3f(-field_size, 0.01, -track_mid)
        glVertex3f(field_size, 0.01, -track_mid)
        glEnd()

    def draw_stadium_elements(self):
        """Desenha elementos decorativos modernos do estádio"""
        glDisable(GL_TEXTURE_2D)
        
        # Torres de iluminação modernas nos cantos
        light_towers = [(-22, 0, -22), (22, 0, -22), (-22, 0, 22), (22, 0, 22)]
        
        for x, y, z in light_towers:
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Base da torre (mais larga)
            glColor3f(0.4, 0.4, 0.5)  # Cinza escuro
            glPushMatrix()
            glTranslatef(0, 1, 0)
            glScalef(2, 2, 2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Torre principal (mais alta e elegante)
            glColor3f(0.5, 0.5, 0.6)
            glPushMatrix()
            glTranslatef(0, 8, 0)
            glScalef(0.8, 14, 0.8)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Estrutura de suporte em X
            glColor3f(0.4, 0.4, 0.5)
            glPushMatrix()
            glTranslatef(0, 5, 0)
            glRotatef(45, 0, 0, 1)
            glScalef(3, 0.2, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(0, 5, 0)
            glRotatef(-45, 0, 0, 1)
            glScalef(3, 0.2, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Holofotes no topo
            light_positions = [(-1, 15, 0), (1, 15, 0), (0, 15, -1), (0, 15, 1)]
            glColor3f(1.0, 1.0, 0.9)  # Branco amarelado
            for lx, ly, lz in light_positions:
                glPushMatrix()
                glTranslatef(lx, ly, lz)
                glutSolidSphere(0.8, 6, 4)
                glPopMatrix()
            
            glPopMatrix()
        
        # Placar eletrônico moderno
        glPushMatrix()
        glTranslatef(0, 12, -32)
        
        # Estrutura do placar
        glColor3f(0.1, 0.1, 0.1)  # Preto
        glScalef(12, 6, 1)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Suporte do placar
        glPushMatrix()
        glTranslatef(0, 6, -32)
        glColor3f(0.5, 0.5, 0.6)
        glScalef(2, 12, 2)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Bandeiras decorativas
        flag_positions = [(-15, 0, -26), (-5, 0, -26), (5, 0, -26), (15, 0, -26)]
        
        for fx, fy, fz in flag_positions:
            # Mastro
            glPushMatrix()
            glTranslatef(fx, fy, fz)
            glColor3f(0.6, 0.6, 0.7)
            glPushMatrix()
            glTranslatef(0, 4, 0)
            glScalef(0.2, 8, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Bandeira
            glColor3f(0.8, 0.1, 0.1)  # Vermelha
            glPushMatrix()
            glTranslatef(1, 6, 0)
            glScalef(2, 1.5, 0.1)
            glutSolidCube(1.0)
            glPopMatrix()
            glPopMatrix()
        
        # Entrada principal do estádio
        glPushMatrix()
        glTranslatef(0, 0, 30)
        
        # Estrutura da entrada
        glColor3f(0.6, 0.6, 0.7)
        glPushMatrix()
        glTranslatef(0, 4, 0)
        glScalef(8, 8, 3)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Arco da entrada
        glColor3f(0.4, 0.4, 0.5)
        glPushMatrix()
        glTranslatef(0, 3, 1)
        glScalef(5, 6, 1)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPopMatrix()

    # ===== CENÁRIO DESERTO =====
    def draw_desert_background(self):
        """Desenha cenário de deserto"""
        self.draw_desert_sky()
        self.draw_desert_dunes()
        self.draw_desert_ground()
        self.draw_desert_elements()

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

    # ===== CENÁRIO NEVE =====
    def draw_snow_background(self):
        """Desenha cenário de neve"""
        self.draw_snow_sky()
        self.draw_snow_mountains()
        self.draw_snow_ground()
        self.draw_snow_elements()

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

    # ===== CENÁRIO VULCÃO =====
    def draw_volcano_background(self):
        """Desenha cenário vulcânico"""
        self.draw_volcano_sky()
        self.draw_volcano_mountains()
        self.draw_volcano_ground()
        self.draw_volcano_elements()

    def draw_volcano_sky(self):
        """Skybox vulcânico - céu avermelhado"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        
        glPushMatrix()
        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        glTranslatef(cam_x, 0, cam_z)
        
        size = 80
        glBegin(GL_QUADS)
        
        # Céu vulcânico - vermelho/laranja
        glColor3f(0.8, 0.3, 0.1)  # Vermelho alaranjado
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glColor3f(0.4, 0.1, 0.1)   # Vermelho escuro
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        glColor3f(0.8, 0.3, 0.1)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glColor3f(0.4, 0.1, 0.1)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        glColor3f(0.8, 0.3, 0.1)
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glColor3f(0.4, 0.1, 0.1)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        glColor3f(0.8, 0.3, 0.1)
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glColor3f(0.4, 0.1, 0.1)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        glColor3f(0.3, 0.1, 0.1)
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_volcano_mountains(self):
        """Vulcões ao fundo"""
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.3, 0.2, 0.2)  # Cinza escuro vulcânico
        
        volcanoes = [
            [(-35, 0, -28), (-20, 20, -30), (-5, 0, -32)],  # Vulcão grande
            [(10, 0, -35), (25, 16, -37), (40, 0, -39)],
            [(45, 0, -25), (55, 12, -27), (65, 0, -29)],
            [(-25, 0, 30), (-10, 14, 28), (5, 0, 26)],
        ]
        
        for volcano in volcanoes:
            glBegin(GL_TRIANGLES)
            for point in volcano:
                glVertex3f(*point)
            glEnd()
            
        # Lava no topo dos vulcões
        glColor3f(1.0, 0.3, 0.0)  # Laranja/vermelho para lava
        lava_tops = [(-20, 20, -30), (25, 16, -37), (55, 12, -27), (-10, 14, 28)]
        for x, y, z in lava_tops:
            glPushMatrix()
            glTranslatef(x, y, z)
            glutSolidSphere(1.5, 6, 4)
            glPopMatrix()

    def draw_volcano_ground(self):
        """Solo vulcânico"""
        glColor3f(0.4, 0.2, 0.1)  # Marrom escuro rochoso
        
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

    def draw_volcano_elements(self):
        """Elementos vulcânicos variados e reconhecíveis - MAIS PRÓXIMOS"""
        
        # Posições mistas para diferentes elementos
        element_positions = [
            (-9, 0, -7), (10, 0, -9), (-12, 0, 8), 
            (11, 0, 10), (-7, 0, 12), (8, 0, 14),
            (-8, 0, -11), (13, 0, -8), (-10, 0, -12),
            (9, 0, -10), (7, 0, 13), (-11, 0, 9)
        ]
        
        for i, (x, y, z) in enumerate(element_positions):
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Alterna entre diferentes elementos vulcânicos
            element_type = i % 4
            
            if element_type == 0:  # Poça de lava
                self.draw_lava_pool()
            elif element_type == 1:  # Rocha vulcânica pontuda
                self.draw_volcanic_spire()
            elif element_type == 2:  # Cristal de obsidiana
                self.draw_obsidian_crystal()
            else:  # Gêiser de vapor
                self.draw_volcanic_geyser()
            
            glPopMatrix()

    def draw_lava_pool(self):
        """Desenha uma poça de lava brilhante"""
        # Aplicar textura de lava se disponível
        if 'lava' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['lava'])
        else:
            glDisable(GL_TEXTURE_2D)
        
        # Cor brilhante da lava (laranja-vermelho)
        glColor3f(1.0, 0.3, 0.1)
        
        # Poça circular achatada
        glPushMatrix()
        glTranslatef(0, 0.1, 0)
        glScalef(2.0, 0.2, 2.0)
        
        # Desenha círculo de lava
        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, 0, 0)
        
        for i in range(17):  # 16 segmentos + 1 para fechar
            angle = i * 2 * pi / 16
            glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle))
            glVertex3f(cos(angle), 0, sin(angle))
        glEnd()
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def draw_volcanic_spire(self):
        """Desenha uma rocha vulcânica pontuda"""
        # Aplicar textura de rocha vulcânica se disponível
        if 'volcanic_rock' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['volcanic_rock'])
        else:
            glDisable(GL_TEXTURE_2D)
        
        # Cor escura da rocha vulcânica
        glColor3f(0.15, 0.1, 0.08)
        
        # Base da rocha (cubo deformado)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glScalef(1.2, 1.0, 1.1)
        glutSolidCube(1.0)
        glPopMatrix()
        
        # Ponta pontuda (cone)
        glPushMatrix()
        glTranslatef(0, 1.2, 0)
        glRotatef(180, 1, 0, 0)  # Inverte para ficar pontiagudo para cima
        glutSolidCone(0.8, 1.5, 6, 1)
        glPopMatrix()
        
        # Pequenas pontas laterais
        for angle in [0, 120, 240]:
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(0.6, 0.8, 0)
            glRotatef(45, 1, 0, 0)
            glutSolidCone(0.2, 0.6, 4, 1)
            glPopMatrix()
        
        glDisable(GL_TEXTURE_2D)

    def draw_obsidian_crystal(self):
        """Desenha cristal de obsidiana brilhante"""
        # Aplicar textura de obsidiana se disponível
        if 'obsidian' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['obsidian'])
        else:
            glDisable(GL_TEXTURE_2D)
        
        # Cor preta brilhante
        glColor3f(0.05, 0.05, 0.15)
        
        # Cristal principal (prisma alongado)
        glPushMatrix()
        glTranslatef(0, 1.5, 0)
        glRotatef(15, 0, 1, 0)  # Rotação para parecer mais natural
        glRotatef(10, 1, 0, 0)
        glScalef(0.4, 3.0, 0.4)
        glutSolidOctahedron()
        glPopMatrix()
        
        # Cristais menores ao redor
        small_crystal_positions = [
            (0.8, 0.6, 0.2, 20), (-0.6, 0.8, -0.3, -15), 
            (0.3, 0.4, 0.9, 45), (-0.4, 0.5, -0.7, -30)
        ]
        
        for cx, cy, cz, rotation in small_crystal_positions:
            glPushMatrix()
            glTranslatef(cx, cy, cz)
            glRotatef(rotation, 0, 1, 0)
            glScalef(0.2, 1.2, 0.2)
            glutSolidOctahedron()
            glPopMatrix()
        
        glDisable(GL_TEXTURE_2D)

    def draw_volcanic_geyser(self):
        """Desenha gêiser vulcânico com vapor"""
        # Base rochosa do gêiser
        if 'molten_rock' in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['molten_rock'])
        else:
            glDisable(GL_TEXTURE_2D)
        
        # Cor da rocha quente
        glColor3f(0.3, 0.15, 0.1)
        
        # Base do gêiser
        glPushMatrix()
        glTranslatef(0, 0.3, 0)
        glScalef(1.5, 0.6, 1.5)
        glutSolidSphere(1.0, 8, 6)
        glPopMatrix()
        
        glDisable(GL_TEXTURE_2D)
        
        # "Vapor" (cilindros semi-transparentes subindo)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.9, 0.9, 0.9, 0.3)  # Branco semi-transparente
        
        # Colunas de vapor de diferentes alturas
        vapor_heights = [2.5, 3.0, 2.8, 3.2, 2.6]
        for i, height in enumerate(vapor_heights):
            glPushMatrix()
            glTranslatef(sin(i * 0.8) * 0.3, height/2 + 0.6, cos(i * 0.8) * 0.3)
            scale = 0.3 - (i * 0.05)
            glScalef(scale, height, scale)
            glutSolidCube(1.0)
            glPopMatrix()
        
        glDisable(GL_BLEND)

    # ===== CENÁRIO ESPACIAL =====
    def draw_space_background(self):
        """Desenha cenário espacial"""
        self.draw_space_sky()
        self.draw_space_structures()
        self.draw_space_ground()
        self.draw_space_elements()

    def draw_space_sky(self):
        """Skybox espacial - preto com estrelas"""
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        
        glPushMatrix()
        cam_x = self.game.ball.pos.x if hasattr(self.game, 'ball') else 0
        cam_z = self.game.ball.pos.z if hasattr(self.game, 'ball') else 0
        glTranslatef(cam_x, 0, cam_z)
        
        size = 80
        
        # Céu preto do espaço
        glColor3f(0.05, 0.05, 0.15)  # Azul muito escuro
        glBegin(GL_QUADS)
        
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        
        glVertex3f(-size, 0, -size)
        glVertex3f(-size, 0, size)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        glVertex3f(size, 0, size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glEnd()
        
        # Estrelas
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(2.0)
        glBegin(GL_POINTS)
        import random
        random.seed(42)  # Seed fixo para estrelas consistentes
        for _ in range(200):
            x = random.uniform(-size, size)
            y = random.uniform(0, size)
            z = random.uniform(-size, size)
            glVertex3f(x, y, z)
        glEnd()
        
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FOG)

    def draw_space_structures(self):
        """Estruturas espaciais distantes"""
        glDisable(GL_TEXTURE_2D)
        
        # Estações espaciais
        stations = [(-30, 15, -25), (35, 12, -30), (-25, 20, 30), (40, 18, 25)]
        
        glColor3f(0.6, 0.6, 0.7)  # Metálico
        for x, y, z in stations:
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Estrutura principal
            glScalef(4, 2, 8)
            glutSolidCube(1.0)
            
            # Painéis solares
            glColor3f(0.1, 0.1, 0.3)
            glPushMatrix()
            glTranslatef(0, 0, 5)
            glScalef(6, 0.2, 2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            glPopMatrix()

    def draw_space_ground(self):
        """Superfície metálica da estação"""
        glColor3f(0.4, 0.4, 0.5)  # Cinza metálico
        
        field_size = Config.CAMPO_METADE
        extended_size = 18.0
        
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

    def draw_space_elements(self):
        """Elementos futurísticos - PRÓXIMOS"""
        glDisable(GL_TEXTURE_2D)
        
        # Antenas e estruturas próximas
        antenna_positions = [
            (-8, 0, -6), (9, 0, -8), (-10, 0, 7), 
            (8, 0, 9), (-6, 0, 11), (7, 0, 12),
            (-9, 0, -9), (10, 0, -7)
        ]
        
        for x, y, z in antenna_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Base
            glColor3f(0.3, 0.3, 0.4)
            glPushMatrix()
            glTranslatef(0, 0.5, 0)
            glScalef(1, 1, 1)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Antena
            glColor3f(0.6, 0.6, 0.7)
            glPushMatrix()
            glTranslatef(0, 3, 0)
            glScalef(0.2, 5, 0.2)
            glutSolidCube(1.0)
            glPopMatrix()
            
            # Luz no topo
            glColor3f(0.0, 1.0, 1.0)  # Ciano
            glTranslatef(0, 5.5, 0)
            glutSolidSphere(0.3, 6, 4)
            
            glPopMatrix()

    # ===== CENÁRIO PRAIA =====
    def draw_beach_background(self):
        """Desenha cenário de praia"""
        self.draw_beach_sky()
        self.draw_beach_horizon()
        self.draw_beach_ground()
        self.draw_beach_elements()

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

    def draw_ui(self):
        w, h = Config.WINDOW_SIZE
        mode = self.game.camera.mode()
        status = "VENCEU!" if self.game.won else ""
        commands = f"Mouse: mira | Espaco: tacada | C: camera({mode}) | R: reset | ESC: MENU"
        infos = f"Level: {self.game.level_index + 1} | Angulo: {self.game.aim_angle:.1f} | Tacadas: {self.game.shots} | {status}"

        ui.begin_2d(w, h) # Prepara o modo 2D
        ui.draw_text(10, h-30, commands, color=(0,0,0,1))
        ui.draw_text(10, h-55, infos, color=(0,0,0,1))
        ui.end_2d() # Restaura o modo 3D

    def render_game(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configura a câmera primeiro
        self.game.camera.setup(self.game.ball)
        
        # Desenha o cenário baseado no nível atual
        self.draw_scenario_background()
        
        # Desenha os elementos principais do jogo
        self.draw_ground()
        self.draw_hole()
        self.draw_obstacles()
        self.draw_ball()
        # AJUSTE: Usa horizontal_speed() para decidir se mostra a mira
        if not self.game.won and self.game.ball.horizontal_speed() < 0.01:
            self.draw_aim()
        self.draw_ui()
        self.draw_power_bar()
        glutSwapBuffers()

    def render(self):
        if self.game.SCREEN_STATE == Config.SCREEN_STATE['PLAYING']:
            self.render_game()
        elif self.game.SCREEN_STATE == Config.SCREEN_STATE['MENU']:
            self.render_menu()

    def draw_power_bar(self):
        game = self.game
        if not game.isShooting:
            return

        pw_min = Config.FORCA_MINIMA
        pw_max = Config.FORCA_MAXIMA
        ratio = (game.shot_power - pw_min) / (pw_max - pw_min)
        ratio = max(0.0, min(1.0, ratio))

        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)

        bar_w = int(w * 0.30)
        bar_h = 18
        margin = 15
        x = (w - bar_w) // 2
        y = margin

        ui.begin_2d(w, h)
        ui.draw_rect(x, y, bar_w, bar_h, color=(0,0,0,0.65))
        ui.draw_rect_outline(x, y, bar_w, bar_h, color=(1,1,1,0.9), width=2)

        fill_w = int(bar_w * ratio)
        ui.draw_rect(x+1, y+1, fill_w-2 if fill_w>2 else 0, bar_h-2, color=(ratio, 1 - ratio / 5, 0.2, 0.9))

        mid_x = x + bar_w // 2
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        glVertex2f(mid_x, y)
        glVertex2f(mid_x, y + bar_h)
        glEnd()

        ui.end_2d()

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)

        ui.begin_2d(w, h)
        titulo = "Mini Golf 3D"
        tw = ui.text_width(titulo)
        ui.draw_text((w - tw)//2, h - 100, titulo)
        
        btn_w, btn_h = 220, 60
        btn_x = (w - btn_w)//2
        btn_y = h//2 - btn_h//2

        self.menu_buttons = [{
            "id": "start",
            "label": "Iniciar Jogo",
            "x": btn_x,
            "y": btn_y,
            "w": btn_w,
            "h": btn_h
        }]

        button = self.menu_buttons[0]
        ui.draw_button(button['x'], button['y'], button['w'], button['h'], button['label'])
        ui.end_2d()
        glutSwapBuffers()

    def on_mouse(self, button, state, x, y):
        if self.game.SCREEN_STATE != Config.SCREEN_STATE['MENU']:
            return
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            h = glutGet(GLUT_WINDOW_HEIGHT)
            y_gl = h - y
            for b in self.menu_buttons:
                if (x >= b['x'] and x <= b['x'] + b['w'] and
                    y_gl >= b['y'] and y_gl <= b['y'] + b['h']):
                    if b['id'] == 'start':
                        self.game.SCREEN_STATE = Config.SCREEN_STATE['PLAYING']
                    break