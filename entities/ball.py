from dataclasses import dataclass
from config import Config
from entities.vec2 import Vec2
from math import sqrt

@dataclass
class Ball:
    pos: Vec2
    vel: Vec2
    radius: float = Config.RAIO_BOLA
    
    def apply_friction(self):
        self.vel.x *= Config.ATRITO
        self.vel.y *= Config.ATRITO
        self.vel.z *= Config.ATRITO
        if abs(self.vel.x) < Config.VEL_MIN:
            self.vel.x = 0.0
        if abs(self.vel.y) < Config.VEL_MIN:
            self.vel.y = 0.0
        if abs(self.vel.z) < Config.VEL_MIN:
            self.vel.z = 0.0

    def update(self, dt):
        # Aplica a gravidade à velocidade vertical
        self.vel.y -= Config.FORCA_GRAVIDADE * dt

        # Atualiza a posição com base na velocidade
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.pos.z += self.vel.z * dt

        self.apply_friction()

    def speed(self):
        return sqrt(self.vel.x*self.vel.x + self.vel.y*self.vel.y + self.vel.z*self.vel.z)

    def horizontal_speed(self):
        # NOVA FUNÇÃO: Calcula a velocidade apenas no plano XZ
        return sqrt(self.vel.x*self.vel.x + self.vel.z*self.vel.z)