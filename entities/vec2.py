from math import sqrt, sin, cos, radians
from dataclasses import dataclass

@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0  # opcional, mas não usado
    z: float = 0.0

    def len(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def translate(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz
        return self

    def rotate(self, angle_deg):
        angle_rad = radians(angle_deg)
        cos_a = cos(angle_rad)
        sin_a = sin(angle_rad)
        x_new = self.x * cos_a - self.z * sin_a
        z_new = self.x * sin_a + self.z * cos_a
        self.x = x_new
        self.z = z_new
        return self

    def scaled(self, k):
        return Vec2(self.x * k, self.y * k, self.z * k)
