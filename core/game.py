import os
import json
from math import sqrt
from OpenGL.GLUT import glutTimerFunc, glutMouseFunc
from config import Config
from entities.vec2 import Vec2
from entities.ball import Ball
from entities.obstacle import BoxObstacle
from entities.camera import Camera
from core.renderer import Renderer

from math import sin, cos, radians

class Game:
    def __init__(self, sounds):
        self.sounds = sounds
        self.SCREEN_STATE = Config.SCREEN_STATE['MENU'] or 0

        self.level_files = sorted([file for file in os.listdir(Config.LEVELS_DIR) if file.endswith(".json")])      
        self.level_index = 0
        
        self.camera = Camera()
        self.renderer = Renderer(self)
        self.renderer.initialize_textures()
        self.load_level(self.level_index)
        
    def load_level(self, index):
        # cria loop no índice do nível
        self.level_index = index % len(self.level_files)
        filename = self.level_files[self.level_index]
        filepath = os.path.join(Config.LEVELS_DIR, filename)

        with open(filepath) as file:
            level_data = json.load(file)

        ball_start_data = level_data["ball_start"]
        obstacles_data = level_data["obstacles"]
        hole_position_data = level_data["hole_position"]
        
        self.ball = Ball(pos=Vec2(*ball_start_data), vel=Vec2(0, 0))
        self.obstacles = [BoxObstacle(**data) for data in obstacles_data]
        self.hole_position = tuple(hole_position_data)

        self.reset_game_state()
    
    def reset_game_state(self):
        self.aim_angle = 25.0
        self.shot_power = 0.35
        self.shots = 0
        self.won = False
        self.isShooting = False
    
    def reset(self):
        self.load_level(self.level_index)

    def next_level(self):
        self.load_level(self.level_index + 1)

    def update_physics(self):
        if self.won: return
        self.ball.update(Config.DT)
        
        # Colisão com bordas
        for axis in ('x','z'):
            pos_axis = getattr(self.ball.pos, axis)
            vel_axis = getattr(self.ball.vel, axis)
            if pos_axis < -Config.CAMPO_METADE + self.ball.radius:
                setattr(self.ball.pos, axis, -Config.CAMPO_METADE + self.ball.radius)
                setattr(self.ball.vel, axis, -vel_axis * 0.9)
            if pos_axis > Config.CAMPO_METADE - self.ball.radius:
                setattr(self.ball.pos, axis, Config.CAMPO_METADE - self.ball.radius)
                setattr(self.ball.vel, axis, -vel_axis * 0.9)

        # Colisão com obstáculos
        for obstacle in self.obstacles:
            obstacle.collide_ball(self.ball)
            
        # Buraco
        dx = self.ball.pos.x - self.hole_position[0]
        dz = self.ball.pos.z - self.hole_position[1]
        d = sqrt(dx*dx + dz*dz)
        if d < Config.RAIO_BURACO * 0.9 and self.ball.speed() < 0.06:
            self.won = True
            self.ball.vel.x = self.ball.vel.z = 0.0
            if self.sounds.get("win"): self.sounds["win"].play()
            self.save_score()
            glutTimerFunc(2000, lambda v: self.next_level(), 0)

    def save_score(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        data = {"scores": []}
        
        if os.path.exists(Config.SCORE_FILE):
            with open(Config.SCORE_FILE) as f:
                data = json.load(f)

        score_entry = {
            "level": self.level_files[self.level_index],
            "shots": self.shots
        }
        data.setdefault("scores", []).append(score_entry)
        
        with open(Config.SCORE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def start_shooting(self):
        # Inicia oscilação da força enquanto espaço estiver pressionado
        if self.ball.speed() > 0.01 or self.won:
            return
        if self.isShooting:
            return
        self.isShooting = True
        self.power_dir = 1
        # Garante limites
        if self.shot_power < Config.FORCA_MINIMA or self.shot_power > Config.FORCA_MAXIMA:
            self.shot_power = 0.35
        self._schedule_power_tick()

    def _schedule_power_tick(self):
        if not self.isShooting:
            return
        self.shot_power += self.power_dir * Config.FORCA_OSCILACAO_VELOCIDADE
        if self.shot_power >= Config.FORCA_MAXIMA:
            self.shot_power = Config.FORCA_MAXIMA
            self.power_dir = -1
        elif self.shot_power <= Config.FORCA_MINIMA:
            self.shot_power = Config.FORCA_MINIMA
            self.power_dir = 1
        # if self.renderer:
        #     self.renderer.update_power_bar(self.shot_power)
        glutTimerFunc(30, lambda v: self._schedule_power_tick(), 0)

    def shoot(self):
        if not self.isShooting:
            return
        
        self.isShooting = False
        angle_rad = radians(self.aim_angle)
        force = self.shot_power * Config.FORCA_MULTIPLICADOR
        self.ball.vel.x += sin(angle_rad) * force
        self.ball.vel.z += cos(angle_rad) * force
        self.shots += 1
        if self.sounds.get("hit"): self.sounds["hit"].play()
        self.shot_power = Config.FORCA_MINIMA
