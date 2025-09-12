from dataclasses import dataclass
from OpenGL.GL import *
from OpenGL.GLUT import *
from entities.ball import Ball

@dataclass
class BoxObstacle:
    cx: float
    cz: float
    sx: float
    sz: float
    h: float = 0.5

    def draw(self):
        glPushMatrix()
        glColor3f(0.82, 0.71, 0.55)
        glTranslatef(self.cx, self.h/2.0, self.cz)
        glScalef(self.sx*2, self.h, self.sz*2)
        glutSolidCube(1.0)
        glPopMatrix()

    def collide_ball(self, ball: Ball):
        bx, bz = ball.pos.x, ball.pos.z
        vx, vz = ball.vel.x, ball.vel.z
        r = ball.radius

        minx = self.cx - self.sx - r
        maxx = self.cx + self.sx + r
        minz = self.cz - self.sz - r
        maxz = self.cz + self.sz + r

        if (minx <= bx <= maxx) and (minz <= bz <= maxz):
            dist_left   = abs(bx - minx)
            dist_right  = abs(maxx - bx)
            dist_bottom = abs(bz - minz)
            dist_top    = abs(maxz - bz)
            min_dist    = min(dist_left, dist_right, dist_bottom, dist_top)

            if min_dist == dist_left:
                ball.pos.x = minx
            elif min_dist == dist_right:
                ball.pos.x = maxx
            elif min_dist == dist_bottom:
                ball.pos.z = minz
            else:
                ball.pos.z = maxz

            if min_dist == dist_left or min_dist == dist_right:
                 ball.vel.x *= -0.9
            else:
                 ball.vel.z *= -0.9