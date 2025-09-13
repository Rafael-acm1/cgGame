import os

class Config:
    WINDOW_SIZE = (800, 600)
    CAMPO_METADE = 6.0
    RAIO_BOLA = 0.22
    ATRITO = 0.98
    VEL_MIN = 0.003
    
    # --- MUDANÇA 1 ---
    # Diminuímos o DT para uma física mais precisa e estável.
    DT = 0.05

    RAIO_BURACO = 0.35
    
    # --- MUDANÇA 2 ---
    # Aumentamos o multiplicador da tacada para compensar o DT menor.
    FORCA_MULTIPLICADOR = 3.5

    RAIO_ATRACAO_BURACO = 0.8
    FORCA_ATRACAO_BURACO = 0.4
    AMORTECIMENTO_BURACO = 1.5 

    # --- MUDANÇA 3 ---
    # Aumentamos a gravidade para compensar o DT menor.
    FORCA_GRAVIDADE = 9.8 * 0.7
    
    RESTITUICAO_SOLO = 0.9

    FORCA_MAXIMA = 2.5
    FORCA_MINIMA = 0.05
    FORCA_OSCILACAO_VELOCIDADE = 0.03

    ASSETS_DIR = "assets"
    LEVELS_DIR = os.path.join(ASSETS_DIR, "levels")
    SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
    
    DATA_DIR = "data"
    SCORE_FILE = os.path.join(DATA_DIR, "scores.json")

    SCREEN_STATE = { "MENU": 0, "PLAYING": 1, "SCORES": 2 , "OPTIONS": 3 }

    VELOCIDADE_MAX_QUEDA = 0.5
    ALTURA_INICIAL_BOLA = 4.0
    
    RAMP_FORCE_MULTIPLIER = 0.1