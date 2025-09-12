from OpenGL.GL import *

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
