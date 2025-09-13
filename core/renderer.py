from math import sin, cos, pi
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from PIL import Image
from config import Config
from utils import ui
from .scenarios.forest import ForestScenario
from .scenarios.snow import SnowScenario
from .scenarios.desert import DesertScenario
from .scenarios.beach import BeachScenario
 
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
        self.current_scenario = None
        self.scenarios = [
            SnowScenario,
            DesertScenario,
            BeachScenario,
            ForestScenario,
        ]
        
    def get_current_scenario(self):
        level_index = self.game.level_index
        num_scenarios = len(self.scenarios)
        
        scenario_index = level_index % num_scenarios
        scenario_class = self.scenarios[scenario_index]
        
        # Re-instancia o cenário apenas se for diferente do atual
        if not self.current_scenario or not isinstance(self.current_scenario, scenario_class):
            self.current_scenario = scenario_class(self.game, self)
            
        return self.current_scenario
    
    def get_field_texture(self):
        level_index = self.game.level_index
        num_scenarios = len(self.scenarios)
        scenario_index = level_index % num_scenarios

        texture_mapping = {
            0: 'snow',     
            1: 'sand',      
            2: 'beachSand', 
            3: 'grass2',    
        }
        
        texture_name = texture_mapping.get(scenario_index, 'grass')
        return texture_name if texture_name in self.textures else 'grass'
    
    def draw_scenario_background(self):
        scenario = self.get_current_scenario()
        scenario.draw()
        
    def initialize_textures(self):
        self.textures['grass'] = load_texture("assets/textures/grass.png")
        self.textures['snow'] = load_texture("assets/textures/snow.png")
        self.textures['sand'] = load_texture("assets/textures/sand.png")
        self.textures['beachSand'] = load_texture("assets/textures/beachSand.png")
        self.textures['grass2'] = load_texture("assets/textures/grass2.png")
        self.textures['rock'] = load_texture("assets/textures/rock.png")
        self.textures['cacto'] = load_texture("assets/textures/cacto.png")
        
    def draw_ground(self):
        # Obter a textura apropriada para o cenário atual
        field_texture = self.get_field_texture()
        
        if field_texture in self.textures:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures[field_texture]) 
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
            # Cores de fallback baseadas no cenário
            level_index = self.game.level_index
            scenario_index = level_index % len(self.scenarios)
            
            fallback_colors = {
                0: (0.92, 0.92, 0.96),  # Snow - branco acinzentado
                1: (0.9, 0.8, 0.5),     # Desert - amarelo areia
                2: (0.9, 0.85, 0.7),    # Beach - bege claro
                3: (0.1, 0.4, 0.1),     # Forest - verde escuro
            }
            
            color = fallback_colors.get(scenario_index, (0.05, 0.55, 0.15))
            glColor3f(*color)
            glBegin(GL_QUADS)
            glVertex3f(-Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glVertex3f( Config.CAMPO_METADE, 0.0, -Config.CAMPO_METADE)
            glVertex3f( Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glVertex3f(-Config.CAMPO_METADE, 0.0,  Config.CAMPO_METADE)
            glEnd()

    def draw_field_borders(self):
        """Desenha bordas temáticas criativas para delimitar a área de jogo"""
        level_index = self.game.level_index
        scenario_index = level_index % len(self.scenarios)
        
        field_size = Config.CAMPO_METADE
        border_width = 0.3
        border_height = 0.15
        
        glDisable(GL_TEXTURE_2D)
        
        if scenario_index == 0:  # Snow Scenario - Cercas de madeira com neve
            self._draw_snow_borders(field_size, border_width, border_height)
        elif scenario_index == 1:  # Desert Scenario - Muros de pedra do deserto
            self._draw_desert_borders(field_size, border_width, border_height)
        elif scenario_index == 2:  # Beach Scenario - Troncos de palmeira
            self._draw_beach_borders(field_size, border_width, border_height)
        elif scenario_index == 3:  # Forest Scenario - Cerca viva de arbustos
            self._draw_forest_borders(field_size, border_width, border_height)
    
    def _draw_snow_borders(self, field_size, width, height):
        """Cerca de madeira coberta de neve"""
        # Cor da madeira
        glColor3f(0.4, 0.2, 0.1)
        
        # Postes verticais nas bordas
        post_positions = [
            # Borda Norte
            [(-field_size, 0, field_size), (field_size, 0, field_size)],
            # Borda Sul  
            [(-field_size, 0, -field_size), (field_size, 0, -field_size)],
            # Borda Leste
            [(field_size, 0, -field_size), (field_size, 0, field_size)],
            # Borda Oeste
            [(-field_size, 0, -field_size), (-field_size, 0, field_size)]
        ]
        
        for start, end in post_positions:
            # Calcula o número de postes baseado na distância
            distance = ((end[0] - start[0])**2 + (end[2] - start[2])**2)**0.5
            num_posts = int(distance / 1.5) + 1
            
            for i in range(num_posts):
                t = i / max(1, num_posts - 1)
                x = start[0] + t * (end[0] - start[0])
                z = start[2] + t * (end[2] - start[2])
                
                # Poste de madeira
                glPushMatrix()
                glTranslatef(x, height, z)
                glScalef(0.1, height * 2, 0.1)
                glutSolidCube(1.0)
                glPopMatrix()
                
                # Neve no topo do poste
                glColor3f(0.95, 0.95, 1.0)
                glPushMatrix()
                glTranslatef(x, height * 1.8, z)
                glutSolidSphere(0.08, 6, 4)
                glPopMatrix()
                glColor3f(0.4, 0.2, 0.1)
        
        # Ripas horizontais conectando os postes
        glColor3f(0.35, 0.15, 0.05)
        self._draw_horizontal_fence_rails(field_size, height)
    
    def _draw_desert_borders(self, field_size, width, height):
        """Cactos pequenos formando a borda do deserto"""
        
        # Verifica se a textura de cacto está disponível
        use_cactus_texture = hasattr(self, 'textures') and 'cacto' in self.textures
        
        if use_cactus_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['cacto'])
            glColor3f(1.0, 1.0, 1.0)  # Branco para não alterar a textura
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.2, 0.5, 0.2)  # Cor verde escura para os cactos como fallback
        
        # Espaçamento entre cactos
        cactus_spacing = 1.2
        
        def draw_textured_cactus_cube():
            """Desenha um cubo com coordenadas de textura para cactos"""
            if use_cactus_texture:
                glBegin(GL_QUADS)
                # Face frontal
                glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f( 0.5, -0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5,  0.5)
                
                # Face traseira
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(1, 1); glVertex3f(-0.5,  0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5,  0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5, -0.5)
                
                # Face superior
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f(-0.5,  0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5, -0.5)
                
                # Face inferior
                glTexCoord2f(1, 1); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5, -0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5,  0.5)
                
                # Face direita
                glTexCoord2f(1, 0); glVertex3f( 0.5, -0.5, -0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5,  0.5)
                
                # Face esquerda
                glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f(-0.5,  0.5,  0.5)
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5, -0.5)
                glEnd()
            else:
                glutSolidCube(1.0)
        
        def draw_small_cactus(scale=1.0):
            """Desenha um cacto pequeno com corpo principal e braços laterais"""
            # Corpo principal do cacto
            glPushMatrix()
            glTranslatef(0, 0.5 * scale, 0)
            glScalef(0.15 * scale, 1.0 * scale, 0.15 * scale)
            draw_textured_cactus_cube()
            glPopMatrix()
            
            # Braço esquerdo (nem todos os cactos têm)
            if scale > 0.6:  # Só cactos maiores têm braços
                glPushMatrix()
                glTranslatef(-0.2 * scale, 0.6 * scale, 0)
                glScalef(0.1 * scale, 0.6 * scale, 0.1 * scale)
                draw_textured_cactus_cube()
                glPopMatrix()
                
                # Extensão horizontal do braço esquerdo
                glPushMatrix()
                glTranslatef(-0.35 * scale, 0.6 * scale, 0)
                glScalef(0.2 * scale, 0.1 * scale, 0.1 * scale)
                draw_textured_cactus_cube()
                glPopMatrix()
            
            # Braço direito (opcional, só em alguns cactos)
            if scale > 0.8:
                glPushMatrix()
                glTranslatef(0.18 * scale, 0.4 * scale, 0)
                glScalef(0.08 * scale, 0.4 * scale, 0.08 * scale)
                draw_textured_cactus_cube()
                glPopMatrix()
        
        # Usar semente fixa para consistência
        import random
        random.seed(123)
        
        # Borda Norte
        x = -field_size - width
        while x <= field_size + width:
            scale_factor = 0.5 + random.random() * 0.5  # Entre 0.5 e 1.0
            x_offset = (random.random() - 0.5) * 0.3
            z_offset = (random.random() - 0.5) * 0.2
            
            glPushMatrix()
            glTranslatef(x + x_offset, 0, field_size + width/2 + z_offset)
            draw_small_cactus(scale_factor)
            glPopMatrix()
            x += cactus_spacing
            
        # Borda Sul
        x = -field_size - width
        while x <= field_size + width:
            scale_factor = 0.5 + random.random() * 0.5
            x_offset = (random.random() - 0.5) * 0.3
            z_offset = (random.random() - 0.5) * 0.2
            
            glPushMatrix()
            glTranslatef(x + x_offset, 0, -field_size - width/2 + z_offset)
            draw_small_cactus(scale_factor)
            glPopMatrix()
            x += cactus_spacing
            
        # Borda Leste
        z = -field_size - width
        while z <= field_size + width:
            scale_factor = 0.5 + random.random() * 0.5
            x_offset = (random.random() - 0.5) * 0.2
            z_offset = (random.random() - 0.5) * 0.3
            
            glPushMatrix()
            glTranslatef(field_size + width/2 + x_offset, 0, z + z_offset)
            draw_small_cactus(scale_factor)
            glPopMatrix()
            z += cactus_spacing
            
        # Borda Oeste
        z = -field_size - width
        while z <= field_size + width:
            scale_factor = 0.5 + random.random() * 0.5
            x_offset = (random.random() - 0.5) * 0.2
            z_offset = (random.random() - 0.5) * 0.3
            
            glPushMatrix()
            glTranslatef(-field_size - width/2 + x_offset, 0, z + z_offset)
            draw_small_cactus(scale_factor)
            glPopMatrix()
            z += cactus_spacing
            
        # Desabilita a textura de cacto antes de desenhar as pedras
        if use_cactus_texture:
            glDisable(GL_TEXTURE_2D)
            
        # Adiciona algumas pedras do deserto espalhadas
        glColor3f(0.7, 0.6, 0.4)  # Cor de pedra do deserto
        desert_rocks = [
            (-field_size - 0.4, 0, field_size + 0.3),
            (field_size + 0.4, 0, field_size + 0.2),
            (field_size + 0.3, 0, -field_size - 0.4),
            (-field_size - 0.3, 0, -field_size - 0.3)
        ]
        
        for x, y, z in desert_rocks:
            # Cada pedra com tamanho ligeiramente diferente
            scale = 0.8 + random.random() * 0.4
            glPushMatrix()
            glTranslatef(x, 0.05 * scale, z)
            glScalef(0.2 * scale, 0.1 * scale, 0.25 * scale)
            glutSolidCube(1.0)
            glPopMatrix()
    
    def _draw_beach_borders(self, field_size, width, height):
        """Cerca simples de madeira para a praia"""
        # Cor da madeira mais clara para praia
        glColor3f(0.7, 0.5, 0.3)
        
        # Postes verticais nas bordas
        post_positions = [
            # Borda Norte
            [(-field_size, 0, field_size), (field_size, 0, field_size)],
            # Borda Sul  
            [(-field_size, 0, -field_size), (field_size, 0, -field_size)],
            # Borda Leste
            [(field_size, 0, -field_size), (field_size, 0, field_size)],
            # Borda Oeste
            [(-field_size, 0, -field_size), (-field_size, 0, field_size)]
        ]
        
        for start, end in post_positions:
            # Calcula o número de postes baseado na distância
            distance = ((end[0] - start[0])**2 + (end[2] - start[2])**2)**0.5
            num_posts = int(distance / 1.5) + 1
            
            for i in range(num_posts):
                t = i / max(1, num_posts - 1)
                x = start[0] + t * (end[0] - start[0])
                z = start[2] + t * (end[2] - start[2])
                
                # Poste de madeira
                glPushMatrix()
                glTranslatef(x, height, z)
                glScalef(0.1, height * 2, 0.1)
                glutSolidCube(1.0)
                glPopMatrix()
        
        # Ripas horizontais conectando os postes
        glColor3f(0.6, 0.4, 0.2)
        self._draw_horizontal_fence_rails(field_size, height)
    
    def _draw_forest_borders(self, field_size, width, height):
        """Pedras naturais formando a borda da floresta"""
        
        # Verifica se a textura de pedra está disponível
        use_rock_texture = hasattr(self, 'textures') and 'rock' in self.textures
        
        if use_rock_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['rock'])
            glColor3f(1.0, 1.0, 1.0)  # Branco para não alterar a textura
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.4, 0.4, 0.4)  # Cor de pedra cinza escura como fallback
        
        # Espaçamento entre as pedras
        stone_spacing = 0.9
        
        # Lista de diferentes tamanhos de pedras para variação
        import random
        random.seed(42)  # Semente fixa para consistência
        
        def draw_textured_rock_cube():
            """Desenha um cubo com coordenadas de textura para simular uma pedra"""
            if use_rock_texture:
                glBegin(GL_QUADS)
                # Face frontal
                glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f( 0.5, -0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5,  0.5)
                
                # Face traseira
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(1, 1); glVertex3f(-0.5,  0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5,  0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5, -0.5)
                
                # Face superior
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f(-0.5,  0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5, -0.5)
                
                # Face inferior
                glTexCoord2f(1, 1); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5, -0.5, -0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5,  0.5)
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5,  0.5)
                
                # Face direita
                glTexCoord2f(1, 0); glVertex3f( 0.5, -0.5, -0.5)
                glTexCoord2f(1, 1); glVertex3f( 0.5,  0.5, -0.5)
                glTexCoord2f(0, 1); glVertex3f( 0.5,  0.5,  0.5)
                glTexCoord2f(0, 0); glVertex3f( 0.5, -0.5,  0.5)
                
                # Face esquerda
                glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
                glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5,  0.5)
                glTexCoord2f(1, 1); glVertex3f(-0.5,  0.5,  0.5)
                glTexCoord2f(0, 1); glVertex3f(-0.5,  0.5, -0.5)
                glEnd()
            else:
                glutSolidCube(1.0)
        
        # Borda Norte
        x = -field_size - width
        while x <= field_size + width:
            # Variação no tamanho e posição das pedras
            scale_factor = 0.3 + random.random() * 0.4  # Entre 0.3 e 0.7
            y_offset = random.random() * 0.05  # Pequena variação na altura
            z_offset = (random.random() - 0.5) * 0.2  # Pequeno deslocamento para naturalidade
            
            glPushMatrix()
            glTranslatef(x, height * scale_factor + y_offset, field_size + width/2 + z_offset)
            glScalef(scale_factor, scale_factor * 0.8, scale_factor)
            draw_textured_rock_cube()  # Cubo com textura para formato rochoso
            glPopMatrix()
            x += stone_spacing
            
        # Borda Sul
        x = -field_size - width
        while x <= field_size + width:
            scale_factor = 0.3 + random.random() * 0.4
            y_offset = random.random() * 0.05
            z_offset = (random.random() - 0.5) * 0.2
            
            glPushMatrix()
            glTranslatef(x, height * scale_factor + y_offset, -field_size - width/2 + z_offset)
            glScalef(scale_factor, scale_factor * 0.8, scale_factor)
            draw_textured_rock_cube()
            glPopMatrix()
            x += stone_spacing
            
        # Borda Leste
        z = -field_size - width
        while z <= field_size + width:
            scale_factor = 0.3 + random.random() * 0.4
            y_offset = random.random() * 0.05
            x_offset = (random.random() - 0.5) * 0.2
            
            glPushMatrix()
            glTranslatef(field_size + width/2 + x_offset, height * scale_factor + y_offset, z)
            glScalef(scale_factor, scale_factor * 0.8, scale_factor)
            draw_textured_rock_cube()
            glPopMatrix()
            z += stone_spacing
            
        # Borda Oeste
        z = -field_size - width
        while z <= field_size + width:
            scale_factor = 0.3 + random.random() * 0.4
            y_offset = random.random() * 0.05
            x_offset = (random.random() - 0.5) * 0.2
            
            glPushMatrix()
            glTranslatef(-field_size - width/2 + x_offset, height * scale_factor + y_offset, z)
            glScalef(scale_factor, scale_factor * 0.8, scale_factor)
            draw_textured_rock_cube()
            glPopMatrix()
            z += stone_spacing
            
        # Adiciona algumas pedras maiores nos cantos como destaque
        if use_rock_texture:
            glColor3f(0.8, 0.8, 0.85)  # Cor ligeiramente mais clara para as pedras dos cantos
        else:
            glColor3f(0.3, 0.3, 0.35)  # Cor ligeiramente diferente para as pedras dos cantos
        
        corner_positions = [
            (-field_size - width*0.7, 0, field_size + width*0.7),
            (field_size + width*0.7, 0, field_size + width*0.7),
            (field_size + width*0.7, 0, -field_size - width*0.7),
            (-field_size - width*0.7, 0, -field_size - width*0.7)
        ]
        
        for x, y, z in corner_positions:
            glPushMatrix()
            glTranslatef(x, 0.15, z)
            glScalef(0.6, 0.3, 0.6)
            draw_textured_rock_cube()
            glPopMatrix()
            
        # Desabilita a textura após usar
        if use_rock_texture:
            glDisable(GL_TEXTURE_2D)
    
    def _draw_horizontal_fence_rails(self, field_size, height):
        """Desenha ripas horizontais para a cerca de neve"""
        rail_height = height * 0.7
        
        # Ripas horizontais conectando toda a volta
        glBegin(GL_QUADS)
        
        # Ripa Norte
        glVertex3f(-field_size, rail_height, field_size)
        glVertex3f(field_size, rail_height, field_size)
        glVertex3f(field_size, rail_height + 0.05, field_size)
        glVertex3f(-field_size, rail_height + 0.05, field_size)
        
        # Ripa Sul
        glVertex3f(-field_size, rail_height, -field_size)
        glVertex3f(field_size, rail_height, -field_size)
        glVertex3f(field_size, rail_height + 0.05, -field_size)
        glVertex3f(-field_size, rail_height + 0.05, -field_size)
        
        # Ripa Leste
        glVertex3f(field_size, rail_height, -field_size)
        glVertex3f(field_size, rail_height, field_size)
        glVertex3f(field_size, rail_height + 0.05, field_size)
        glVertex3f(field_size, rail_height + 0.05, -field_size)
        
        # Ripa Oeste
        glVertex3f(-field_size, rail_height, -field_size)
        glVertex3f(-field_size, rail_height, field_size)
        glVertex3f(-field_size, rail_height + 0.05, field_size)
        glVertex3f(-field_size, rail_height + 0.05, -field_size)
        
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
        for o in self.game.obstacles:
            if getattr(o, 'type', '') != 'water':
                o.draw()
        
        has_water = any(getattr(o, 'type', '') == 'water' for o in self.game.obstacles)
        if has_water:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            for o in self.game.obstacles:
                if getattr(o, 'type', '') == 'water':
                    o.draw()
            glDisable(GL_BLEND)
    
    def draw_ui(self):
        w, h = Config.WINDOW_SIZE
        glMatrixMode(GL_PROJECTION)
        glPushMatrix(); glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(); glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glColor3f(0.0, 0.0, 0.0)
        def write_text(x, y, text):
            glRasterPos2f(x, y)
            for ch in text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        
        mode = self.game.camera.mode()
        status = "VENCEU!" if self.game.won else ""
        write_text(10, h-30, f"Setas: mira/forca | Espaco: tacada | C: camera({mode}) | R: reset | ESC: MENU")
        write_text(10, h-55, f"Level: {self.game.level_index + 1} | Angulo: {self.game.aim_angle:.1f} | Tacadas: {self.game.shots} | {status}")
        
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def render_game(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configura a câmera primeiro
        self.game.camera.setup(self.game.ball)
        
        # Desenha o cenário baseado no nível atual
        self.draw_scenario_background()
        
        # Desenha os elementos principais do jogo
        self.draw_ground()
        self.draw_field_borders()  # Adiciona as bordas temáticas criativas
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

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

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

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        titulo = "CGolf"
        def text_width(txt):
            return sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in txt)

        def draw_text(x, y, txt):
            glRasterPos2f(x, y)
            for c in txt:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        tw = text_width(titulo)
        draw_text((w - tw)//2, h - 100, titulo)
        
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

        ui.draw_rect(btn_x, btn_y, btn_w, btn_h, color=(0,0,0,0.55))
        ui.draw_rect_outline(btn_x, btn_y, btn_w, btn_h, color=(1,1,1,0.9), width=2)
        label = "Iniciar Jogo"
        lw = text_width(label)
        lh = 18
        draw_text(btn_x + (btn_w - lw)//2, btn_y + (btn_h - lh)//2 + 6, label)

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
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