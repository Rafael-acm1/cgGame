from math import sin, cos, pi
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
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
            ForestScenario,
            BeachScenario,
            DesertScenario,
            SnowScenario,
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
    
    def draw_scenario_background(self):
        scenario = self.get_current_scenario()
        scenario.draw()
        
    def initialize_textures(self):
        self.textures['grass'] = load_texture("assets/textures/grass.png")
        self.textures['grass2'] = load_texture("assets/textures/grass2.png")
        self.textures['snow'] = load_texture("assets/textures/snow.png")
        self.textures['sand'] = load_texture("assets/textures/sand.png")
        self.textures['beach_sand'] = load_texture("assets/textures/beach_sand.png")
        
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
        glRotatef(-self.game.angle_vertical, 1.0, 0.0, 0.0)
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
            for obstacle in self.game.obstacles:
                if getattr(obstacle, 'type', '') == 'water':
                    obstacle.draw()
            glDisable(GL_BLEND)
    
    def draw_ui(self):
        w, h = Config.WINDOW_SIZE
        ui.begin_2d(w, h)
        
        status = "VENCEU!" if self.game.won else ""
        commands = f"Setas: mira/forca | Espaco: tacada | C: camera({self.game.camera.mode()}) | R: reset | ESC: MENU"
        infos = f"Level: {self.game.level_index + 1} | Angulo: {self.game.aim_angle:.1f} | Tacadas: {self.game.shots} | {status}"

        ui.draw_text(10, h-30, commands)
        ui.draw_text(10, h-55, infos)       
        ui.end_2d()

    def render_game(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.game.camera.setup(self.game.ball)
        self.draw_scenario_background()
        self.draw_ground()
        self.draw_hole()
        self.draw_obstacles()
        self.draw_ball()

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
        if not self.game.isShooting:
            return

        pw_min = Config.FORCA_MINIMA
        pw_max = Config.FORCA_MAXIMA
        ratio = (self.game.shot_power - pw_min) / (pw_max - pw_min)
        ratio = max(0.0, min(1.0, ratio))

        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)

        bar_w = int(w * 0.30)
        bar_h = 18
        margin = 15
        x = (w - bar_w) // 2
        y = margin

        ui.begin_2d(w, h)
        ui.draw_rect_outline(x, y, bar_w, bar_h, color=(1,1,1,0.9), width=2)
        fill_w = int(bar_w * ratio)
        ui.draw_rect(x+1, y+1, fill_w-2 if fill_w>2 else 0, bar_h-2, color=(ratio, 1 - ratio / 5, 0.2, 0.9))
        ui.end_2d()

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        w = glutGet(GLUT_WINDOW_WIDTH)
        h = glutGet(GLUT_WINDOW_HEIGHT)

        ui.begin_2d(w, h)
        titulo = "Mini Golf 3D"
        tw = ui.text_width(titulo)
        ui.draw_text((w - tw)//2, h - 100, titulo, color=(1,1,1,1))
        
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

        ui.draw_button(btn_x, btn_y, btn_w, btn_h, "Iniciar Jogo")
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