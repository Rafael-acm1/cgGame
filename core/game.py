import os
import json
from math import sin, cos, radians, sqrt, atan2
from OpenGL.GLUT import glutTimerFunc
from config import Config
from entities.vec2 import Vec2
from entities.ball import Ball
from entities.obstacle import BoxObstacle, Ramp, WaterObstacle 
from entities.camera import Camera
from core.renderer import Renderer

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
        self.angle_vertical = 0
        
    def load_level(self, index):
        self.level_index = index % len(self.level_files)
        filename = self.level_files[self.level_index]
        filepath = os.path.join(Config.LEVELS_DIR, filename)
        with open(filepath) as file:
            level_data = json.load(file)

        ball_start_data = level_data["ball_start"]
        obstacles_data = level_data.get("obstacles", [])
        hole_position_data = level_data["hole_position"]
        
        pos_inicial = Vec2(x=ball_start_data[0], y=Config.ALTURA_INICIAL_BOLA, z=ball_start_data[1])
        self.ball = Ball(pos=pos_inicial, vel=Vec2(0, 0, 0))
        # Salva posição inicial para reset em caso de queda na água
        self.ball_initial_position = Vec2(x=ball_start_data[0], y=Config.ALTURA_INICIAL_BOLA, z=ball_start_data[1])

        self.obstacles = []
        for data in obstacles_data:
            if data.get("type") == "ramp":
                self.obstacles.append(Ramp(**data))
            elif data.get("type") == "water":
                self.obstacles.append(WaterObstacle(**data))
            else: 
                self.obstacles.append(BoxObstacle(**data))

        self.hole_position = tuple(hole_position_data)
        self.reset_game_state()
    
    def reset_game_state(self):
        self.aim_angle = 25.0; self.shot_power = 0.35; self.shots = 0
        self.won = False; self.isShooting = False
        self.angle_vertical = 0
    
    def reset_ball_to_start(self):
        """Reseta a bola para a posição inicial quando toca na água"""
        self.ball.pos.x = self.ball_initial_position.x
        self.ball.pos.y = self.ball_initial_position.y
        self.ball.pos.z = self.ball_initial_position.z
        self.ball.vel.x = 0.0
        self.ball.vel.y = 0.0
        self.ball.vel.z = 0.0
        # Toca som de splash
        if self.sounds.get("water_splash"):
            self.sounds["water_splash"].play()
    
    def reset(self): self.load_level(self.level_index)
    
    def next_level(self): self.load_level(self.level_index + 1)

    def update_physics(self):
        if self.won: return
        
        # Verifica colisões com obstáculos
        for obstacle in self.obstacles:
            collision_result = obstacle.collide_ball(self.ball)
            # Se a bola tocou na água, reseta posição
            if collision_result == "water_collision":
                self.reset_ball_to_start()
                return

        self.ball.update(Config.DT)

        for axis in ('x','z'):
            pos_axis = getattr(self.ball.pos, axis); vel_axis = getattr(self.ball.vel, axis)
            if pos_axis < -Config.CAMPO_METADE + self.ball.radius:
                setattr(self.ball.pos, axis, -Config.CAMPO_METADE + self.ball.radius)
                setattr(self.ball.vel, axis, -vel_axis * 0.9)
            if pos_axis > Config.CAMPO_METADE - self.ball.radius:
                setattr(self.ball.pos, axis, Config.CAMPO_METADE - self.ball.radius)
                setattr(self.ball.vel, axis, -vel_axis * 0.9)
            
        dx = self.ball.pos.x - self.hole_position[0]
        dz = self.ball.pos.z - self.hole_position[1]
        dist_ao_buraco = sqrt(dx*dx + dz*dz)

        if dist_ao_buraco < Config.RAIO_BURACO and self.ball.pos.y < -self.ball.radius:
            self.won = True; self.ball.vel.x = self.ball.vel.y = self.ball.vel.z = 0.0
            if self.sounds.get("win"): self.sounds["win"].play()
            self.save_score()
            glutTimerFunc(2000, lambda v: self.next_level(), 0)
            return

        if dist_ao_buraco < Config.RAIO_BURACO:
            if dist_ao_buraco > 0.01:
                dir_x = -dx / dist_ao_buraco; dir_z = -dz / dist_ao_buraco
                forca = Config.FORCA_ATRACAO_BURACO * Config.DT
                self.ball.vel.x += dir_x * forca; self.ball.vel.z += dir_z * forca
        else:
            is_on_ramp = False
            for obs in self.obstacles:
                if isinstance(obs, Ramp) and obs.collide_ball(self.ball) is not None:
                     is_on_ramp = True
                     break
            if not is_on_ramp and self.ball.pos.y < self.ball.radius:
                self.ball.pos.y = self.ball.radius
                if self.ball.vel.y < 0:
                    self.ball.vel.y *= -Config.RESTITUICAO_SOLO
                    if abs(self.ball.vel.y) < 0.01: self.ball.vel.y = 0

    def save_score(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        data = {"scores": []}
        
        # Try to load existing data with error handling
        if os.path.exists(Config.SCORE_FILE):
            try:
                with open(Config.SCORE_FILE) as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load scores file: {e}")
                print("Creating new scores file...")
                data = {"scores": []}
        
        score_entry = {"level": self.level_files[self.level_index], "shots": self.shots}
        data.setdefault("scores", []).append(score_entry)
        
        # Try to save with error handling
        try:
            with open(Config.SCORE_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save scores file: {e}")

    def start_shooting(self):
        if self.ball.horizontal_speed() > 0.01 or self.won: return
        if self.isShooting: return
        self.isShooting = True; self.power_dir = 1
        if self.shot_power < Config.FORCA_MINIMA or self.shot_power > Config.FORCA_MAXIMA: self.shot_power = 0.35
        self._schedule_power_tick()

    def _schedule_power_tick(self):
        if not self.isShooting: return
        self.shot_power += self.power_dir * Config.FORCA_OSCILACAO_VELOCIDADE
        if self.shot_power >= Config.FORCA_MAXIMA:
            self.shot_power = Config.FORCA_MAXIMA; self.power_dir = -1
        elif self.shot_power <= Config.FORCA_MINIMA:
            self.shot_power = Config.FORCA_MINIMA; self.power_dir = 1
        glutTimerFunc(30, lambda v: self._schedule_power_tick(), 0)

    def shoot(self):
        if not self.isShooting: return
        self.isShooting = False; angle_rad = radians(self.aim_angle)
        force = self.shot_power * Config.FORCA_MULTIPLICADOR
        self.ball.vel.x += sin(angle_rad) * force; self.ball.vel.z += cos(angle_rad) * force
        self.ball.vel.y += sin(self.angle_vertical) * (force * 1.7) 
        self.shots += 1
        if self.sounds.get("hit"): self.sounds["hit"].play()
        self.shot_power = Config.FORCA_MINIMA
        self.angle_vertical = 0
        