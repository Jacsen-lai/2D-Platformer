import pygame

class Portal():
    def __init__(self, game, pos, size=(16, 24), target_level=None):
        self.game = game
        self.pos = pos
        self.size = size
        self.target_level = target_level  
        self.color = (150, 100, 255)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.animation_phase = 0  

    def update(self):
        self.animation_phase = (self.animation_phase + 1) % 60
        
        self.rect.topleft = self.pos

        player_rect = self.game.player.rect()
        if player_rect.colliderect(self.rect):
            if self.target_level is not None:
                self.game.load_level(self.target_level)
                self.game.player = self.game.player.__class__(self.game, (100, 100), (8, 15))

    def draw(self, surf, offset=(0, 0)):
        color_shift = int(50 * abs(30 - self.animation_phase) / 30)
        aura = (self.color[0] + color_shift, self.color[1], self.color[2] + color_shift)
        draw_rect = pygame.Rect(
            self.rect.x - offset[0], self.rect.y - offset[1], 
            self.rect.width, self.rect.height
        )
        pygame.draw.rect(surf, aura, draw_rect, border_radius = 6)
