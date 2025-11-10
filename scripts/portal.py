import pygame
import math

class Portal:
    def __init__(self, game, pos, size=(20, 28), target_level=None):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.target_level = target_level

        # Swamp-style colors
        self.main_color = (60, 150, 80)     # soft green light
        self.inner_color = (30, 100, 50)    # darker green interior
        self.outline_color = (15, 40, 20)   # dark moss outline
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def update(self):
        self.rect.topleft = (self.pos[0], self.pos[1])

        # Check for player entering
        player_rect = self.game.player.rect()
        if player_rect.colliderect(self.rect):
            if self.target_level is not None:
                self.game.level = self.target_level
                self.game.load_level(self.target_level)
                self.game.player = self.game.player.__class__(self.game, (100, 100), (8, 15))

    def draw(self, surf, offset=(0, 0)):
        x = self.rect.x - offset[0]
        y = self.rect.y - offset[1]
        w, h = self.size


        # Outer frame (solid)
        frame_rect = pygame.Rect(x - 2, y - 2, w + 4, h + 4)
        pygame.draw.rect(surf, self.outline_color, frame_rect, border_radius=4)

        # Slightly darker inner rectangle for depth
        inner_rect = pygame.Rect(x + 3, y + 3, w - 6, h - 6)
        pygame.draw.rect(surf, self.inner_color, inner_rect, border_radius=2)
