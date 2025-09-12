import sys
import pygame
from functools import partial
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from config import Config
from core.game import Game
import utils.inputs as inputs
import utils.audio as audio_manager

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.6, 0.85, 1.0, 1.0)
    glShadeModel(GL_SMOOTH)
    
    # Configuração básica do fog
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)
    glFogfv(GL_FOG_COLOR, (0.6, 0.85, 1.0, 1.0))

def reshape(w, h):
    Config.WINDOW_SIZE = (w, h)
    glViewport(0, 0, w, h if h>0 else 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w/float(h if h>0 else 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    # Inicializa Pygame (para som) e GLUT
    pygame.init()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(*Config.WINDOW_SIZE)
    glutCreateWindow(b"Mini Golf 3D")

    # Inicializa componentes do jogo
    init_gl()
    sounds = audio_manager.init_sounds()
    game = Game(sounds)

    # Funções de display e timer
    def display():
        game.renderer.render()

    def timer(v=0):
        game.update_physics()
        glutPostRedisplay()
        glutTimerFunc(16, timer, 0)

    # Registra callbacks, passando o objeto 'game' quando necessário
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(16, timer, 0)

    def mouse_combined(button, state, x, y):
        game.renderer.on_mouse(button, state, x, y)  # menu
        inputs.mouse(button, state, x, y)            # outras lógicas (se precisar)

    glutMouseFunc(mouse_combined)
    
    # Usamos 'partial' para "pré-preencher" o argumento 'game' nas funções de input
    glutKeyboardFunc(partial(inputs.keyboard, game=game))
    glutSpecialFunc(partial(inputs.special_keys, game=game))
    glutKeyboardUpFunc(partial(inputs.keyboard_up, game=game, sounds=sounds))
    glutMotionFunc(partial(inputs.motion, game=game))
    # controla o movimento do mouse para ajustar o ângulo de mira
    glutPassiveMotionFunc(partial(inputs.passive_motion, game=game))
    
    glutMainLoop()

if __name__ == '__main__':
    main()