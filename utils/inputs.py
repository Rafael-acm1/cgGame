import sys
from OpenGL.GLUT import *
from math import atan2, degrees
from OpenGL.GLU import gluUnProject
from OpenGL.GL import (
    glGetDoublev,
    glGetIntegerv,
    GL_MODELVIEW_MATRIX,
    GL_PROJECTION_MATRIX,
    GL_VIEWPORT,
)
from config import Config

mouse_pressed = False
mouse_last_x = 0
mouse_last_y = 0
mouse_sensitivity = 0.3
aim_mouse_sensitivity = 0.3

def keyboard(key, x, y, game):
    """Lida com eventos de tecla PRESSIONADA."""
    k = key.decode('utf-8') if isinstance(key, bytes) else key

    if k == '\x1b':  # ESC
        if game.SCREEN_STATE != Config.SCREEN_STATE['MENU']:
            game.SCREEN_STATE = Config.SCREEN_STATE['MENU']
        else:
            sys.exit(0)
    elif k in ('c', 'C'):
        game.camera.toggle_mode()
    elif k in ('r', 'R'):
        game.reset()
    elif k == ' ':
        canShoot = not game.won and game.ball.horizontal_speed() < 0.01
        if canShoot and not game.isShooting:
            game.start_shooting()

def keyboard_up(key, x, y, game, sounds):
    """Lida com eventos de tecla SOLTA."""
    k = key.decode('utf-8') if isinstance(key, bytes) else key
    
    if k == ' ':
        game.shoot()

def special_keys(key, x, y, game):
    if game.SCREEN_STATE != 1: return
    if key == GLUT_KEY_LEFT:
        game.aim_angle = (game.aim_angle + 5.0) % 360
    elif key == GLUT_KEY_RIGHT:
        game.aim_angle = (game.aim_angle - 5.0) % 360

def mouse(button, state, x, y):
    global mouse_pressed, mouse_last_x, mouse_last_y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouse_pressed = True
            mouse_last_x = x
            mouse_last_y = y
        elif state == GLUT_UP:
            mouse_pressed = False

def motion(x, y, game):
    global mouse_last_x, mouse_last_y
    if mouse_pressed and game.camera.mode() == 'bola':
        dx = x - mouse_last_x
        dy = y - mouse_last_y
        game.camera.h_angle += dx * mouse_sensitivity
        game.camera.v_angle += dy * mouse_sensitivity
        game.camera.v_angle = max(-5.0, min(80.0, game.camera.v_angle))
        mouse_last_x = x
        mouse_last_y = y
        glutPostRedisplay()

def passive_motion(x, y, game):
    if game.isShooting or game.won:
        return
    try:
        model = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
    except Exception:
        return
    if model is None or proj is None or viewport is None:
        return
    win_x = float(x)
    win_y = float(viewport[3] - y)
    try:
        near_pt = gluUnProject(win_x, win_y, 0.0, model, proj, viewport)
        far_pt = gluUnProject(win_x, win_y, 1.0, model, proj, viewport)
    except Exception:
        return
    if not near_pt or not far_pt:
        return
    nx, ny, nz = near_pt
    fx, fy, fz = far_pt
    dirx, diry, dirz = fx - nx, fy - ny, fz - nz
    plane_y = max(0.0, game.ball.pos.y)
    if abs(diry) < 1e-8:
        diry = 1e-8
    t = (plane_y - ny) / diry
    if t <= 0:
        return
    ix = nx + dirx * t
    iz = nz + dirz * t
    dx = ix - game.ball.pos.x
    dz = iz - game.ball.pos.z
    if abs(dx) < 1e-9 and abs(dz) < 1e-9:
        return
    angle_deg = degrees(atan2(dx, dz)) % 360
    alpha = 0.35
    prev = getattr(game, "aim_angle", angle_deg)
    game.aim_angle = (1 - alpha) * prev + alpha * angle_deg
    glutPostRedisplay()