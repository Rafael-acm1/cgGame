import os

class Config:
    WINDOW_SIZE = (800, 600)
    CAMPO_METADE = 6.0
    RAIO_BOLA = 0.22
    ATRITO = 0.98
    VEL_MIN = 0.003
    DT = 0.4
    RAIO_BURACO = 0.35
    FORCA_MULTIPLICADOR = 0.75

    RAIO_ATRACAO_BURACO = 0.8       # alcance em múltiplos do RAIO_BURACO
    FORCA_ATRACAO_BURACO = 0.4            # "aceleração" base (aumente se ainda fraco)
    AMORTECIMENTO_BURACO = 1.5 

    FORCA_GRAVIDADE = 9.8 * 0.4          # escala para caber no ritmo do jogo
    RESTITUICAO_SOLO = 0.45        # quique

    FORCA_MAXIMA = 1.5
    FORCA_MINIMA = 0.05
    FORCA_OSCILACAO_VELOCIDADE = 0.03

    ASSETS_DIR = "assets"
    LEVELS_DIR = os.path.join(ASSETS_DIR, "levels")
    SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
    
    DATA_DIR = "data"
    SCORE_FILE = os.path.join(DATA_DIR, "scores.json")

    SCREEN_STATE = {
        "MENU": 0,
        "PLAYING": 1,
        "SCORES": 2
    }