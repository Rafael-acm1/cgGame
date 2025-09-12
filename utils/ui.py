from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

def draw_rect(x, y, w, h, color=(0,0,0,0.5)):
    """Retângulo cheio."""
    r,g,b,a = color
    glColor4f(r,g,b,a)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()

def draw_rect_outline(x, y, w, h, color=(1,1,1,1), width=2):
    """Borda de retângulo."""
    glLineWidth(width)
    r,g,b,a = color
    glColor4f(r,g,b,a)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()

def text_width(text, font=GLUT_BITMAP_HELVETICA_18):
    """Calcula a largura em pixels do texto."""
    return sum(glutBitmapWidth(font, ord(c)) for c in text)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1,1,1,1)):
    """Desenha texto na tela."""
    r,g,b,a = color
    glColor4f(r,g,b,a)
    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(font, ord(c))

def draw_button(x, y, w, h, label, bg_color=(0,0,0,0.55), outline_color=(1,1,1,0.9)):
    """Desenha um componente de botão completo com texto centralizado."""
    draw_rect(x, y, w, h, color=bg_color)
    draw_rect_outline(x, y, w, h, color=outline_color, width=2)
    
    # Calcula a posição para centralizar o texto
    label_width = text_width(label)
    label_height = 16
    text_x = x + (w - label_width) / 2
    text_y = y + (h - label_height) / 2
    
    draw_text(text_x, text_y, label)

def begin_2d(width, height):
    """Prepara o ambiente para desenhar em 2D (UI)."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

def end_2d():
    """Restaura o ambiente para o desenho 3D."""
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
