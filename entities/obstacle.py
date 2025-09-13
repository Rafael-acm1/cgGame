from dataclasses import dataclass
from OpenGL.GL import *
from OpenGL.GLUT import *
from entities.ball import Ball
from config import Config
from math import sin, cos, radians, pi, atan2, sqrt

@dataclass
class BoxObstacle:
    cx: float; cz: float; sx: float; sz: float; h: float = 0.5; type: str = "box"
    def draw(self):
        glPushMatrix(); glColor3f(0.82, 0.71, 0.55)
        glTranslatef(self.cx, self.h/2.0, self.cz); glScalef(self.sx*2, self.h, self.sz*2)
        glutSolidCube(1.0); glPopMatrix()
    def collide_ball(self, ball: Ball):
        bx, bz = ball.pos.x, ball.pos.z; r = ball.radius
        minx = self.cx - self.sx - r; maxx = self.cx + self.sx + r
        minz = self.cz - self.sz - r; maxz = self.cz + self.sz + r
        if (minx <= bx <= maxx) and (minz <= bz <= maxz):
            if ball.pos.y > self.h + r:
                return
                
            dist_left   = abs(bx - minx); dist_right  = abs(maxx - bx)
            dist_bottom = abs(bz - minz); dist_top    = abs(maxz - bz)
            min_dist    = min(dist_left, dist_right, dist_bottom, dist_top)
            if min_dist == dist_left: ball.pos.x = minx; ball.vel.x *= -0.9
            elif min_dist == dist_right: ball.pos.x = maxx; ball.vel.x *= -0.9
            elif min_dist == dist_bottom: ball.pos.z = minz; ball.vel.z *= -0.9
            else: ball.pos.z = maxz; ball.vel.z *= -0.9

@dataclass
class Ramp:
    cx: float; cz: float; sx: float; sz: float; h: float
    rotation_y: float = 0; type: str = "ramp"

    def draw(self):
        glPushMatrix(); glColor3f(0.6, 0.6, 0.65)
        glTranslatef(self.cx, 0, self.cz); glRotatef(self.rotation_y, 0, 1, 0)
        v = [
            [-self.sx, 0, -self.sz], [ self.sx, 0, -self.sz],
            [ self.sx, 0,  self.sz], [-self.sx, 0,  self.sz],
            [-self.sx, self.h, self.sz], [ self.sx, self.h, self.sz]
        ]
        glBegin(GL_QUADS)
        glVertex3fv(v[0]); glVertex3fv(v[3]); glVertex3fv(v[2]); glVertex3fv(v[1])
        glVertex3fv(v[2]); glVertex3fv(v[3]); glVertex3fv(v[4]); glVertex3fv(v[5])
        glVertex3fv(v[0]); glVertex3fv(v[1]); glVertex3fv(v[5]); glVertex3fv(v[4])
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex3fv(v[0]); glVertex3fv(v[3]); glVertex3fv(v[4])
        glVertex3fv(v[1]); glVertex3fv(v[5]); glVertex3fv(v[2])
        glEnd(); glPopMatrix()

    def collide_ball(self, ball: Ball):
        angle_rad_rot = radians(-self.rotation_y)
        local_x = ball.pos.x - self.cx; local_z = ball.pos.z - self.cz
        rotated_x = local_x * cos(angle_rad_rot) - local_z * sin(angle_rad_rot)
        rotated_z = local_x * sin(angle_rad_rot) + local_z * cos(angle_rad_rot)

        # Se a bola não estiver sobre a área da rampa, não faz nada
        if not (-self.sx < rotated_x < self.sx and -self.sz < rotated_z < self.sz):
            return

        # Calcula a altura da superfície da rampa na posição da bola
        progresso = (rotated_z + self.sz) / (2 * self.sz)
        altura_rampa = progresso * self.h

        # Se a bola colidir ou estiver sobre a rampa
        if ball.pos.y <= altura_rampa + ball.radius:
            # 1. Corrige a posição para ficar exatamente sobre a superfície
            ball.pos.y = altura_rampa + ball.radius

            # 2. Simula a FÍSICA DA RAMPA
            angulo_inclinacao = atan2(self.h, 2 * self.sz)

            # Força Normal (Perpendicular): Empurra a bola para CIMA, cancelando a gravidade.
            gravidade_perp = Config.FORCA_GRAVIDADE * cos(angulo_inclinacao)
            forca_normal_y = gravidade_perp * cos(angulo_inclinacao)
            ball.vel.y += forca_normal_y * Config.DT # Adiciona velocidade para cima

            # Força de Deslizamento (Paralela): Puxa a bola para BAIXO da rampa.
            gravidade_paralela = Config.FORCA_GRAVIDADE * -sin(angulo_inclinacao)
            forca_deslizamento = gravidade_paralela * Config.RAMP_FORCE_MULTIPLIER

            # Aplica a força na direção correta
            vel_x_rampa = sin(radians(self.rotation_y)) * forca_deslizamento * Config.DT
            vel_z_rampa = cos(radians(self.rotation_y)) * forca_deslizamento * Config.DT
            ball.vel.x += vel_x_rampa
            ball.vel.z += vel_z_rampa

@dataclass
class WaterObstacle:
    cx: float; cz: float; sx: float; sz: float; type: str = "water"
    
    def draw(self):
        # Desenha água com cor azul transparente
        glPushMatrix()
        glColor4f(0.0, 0.4, 0.8, 0.6)  # Azul translúcido
        glTranslatef(self.cx, 0.002, self.cz)  # Ligeiramente acima do chão
        glBegin(GL_QUADS)
        glVertex3f(-self.sx, 0, -self.sz)
        glVertex3f( self.sx, 0, -self.sz)
        glVertex3f( self.sx, 0,  self.sz)
        glVertex3f(-self.sx, 0,  self.sz)
        glEnd()
        glPopMatrix()
    
    def collide_ball(self, ball: Ball):
        # Verifica se a bola está sobre a área de água
        if (self.cx - self.sx <= ball.pos.x <= self.cx + self.sx and
            self.cz - self.sz <= ball.pos.z <= self.cz + self.sz and
            ball.pos.y <= ball.radius + 0.1):  # Próximo ao nível da água
            return "water_collision"  # Sinal especial para o Game processar
        return None