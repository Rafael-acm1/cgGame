import os
import pygame
from config import Config

def init_sounds():
    pygame.mixer.init()

    bg_music_path = os.path.join(Config.SOUNDS_DIR, "playing.ogg")
    hit_sound_path = os.path.join(Config.SOUNDS_DIR, "hit.wav")
    win_sound_path = os.path.join(Config.SOUNDS_DIR, "win.wav")
    water_splash_path = os.path.join(Config.SOUNDS_DIR, "water_splash.wav")

    bg_music = pygame.mixer.Sound(file=bg_music_path) if os.path.exists(bg_music_path) else None
    hit_sound = pygame.mixer.Sound(file=hit_sound_path) if os.path.exists(hit_sound_path) else None
    win_sound = pygame.mixer.Sound(file=win_sound_path) if os.path.exists(win_sound_path) else None
    water_splash_sound = pygame.mixer.Sound(file=water_splash_path) if os.path.exists(water_splash_path) else None

    if bg_music:
        bg_music.set_volume(0.05)
        bg_music.play(loops=-1)  # Loop infinito

    if hit_sound:
        hit_sound.set_volume(0.1)

    if water_splash_sound:
        water_splash_sound.set_volume(0.15)
    
    return {
        "bg_music": bg_music,
        "hit": hit_sound,
        "win": win_sound,
        "water_splash": water_splash_sound,
    }