class BaseScenario:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
    
    def draw(self):
        self.draw_sky()
        self.draw_ground()
        self.draw_elements()

    def draw_sky(self):
        raise NotImplementedError

    def draw_ground(self):
        raise NotImplementedError

    def draw_elements(self):
        raise NotImplementedError