import pygame

def _clamp_color_value(v):
    """Clamp a numeric to the valid pygame color range 0..255 and return int."""
    return max(0, min(255, int(v)))

class Portal:
    def __init__(self, game, pos, size=(16, 24), target_level=None):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.target_level = target_level
        self.base_color = (150, 100, 200)  # safe starting color (r,g,b)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.animation_phase = 0  # simple visual shimmer

    def update(self):
        # Simple animation counter
        self.animation_phase = (self.animation_phase + 1) % 60
        self.rect.topleft = (self.pos[0], self.pos[1])

        # Collision with player -> load target level (if any)
        player_rect = self.game.player.rect()
        if player_rect.colliderect(self.rect):
           if self.target_level is not None:
                self.game.level = self.target_level  # ✅ remember what level we’re on
                self.game.load_level(self.target_level)
                self.game.player = self.game.player.__class__(self.game, (0, 100), (8, 15))

    def draw(self, surf, offset=(0, 0)):
        # Create a pulsating glow color safely
        # animation_phase runs 0..59; convert to -30..+30 so pulse is symmetric
        phase = self.animation_phase - 30
        color_shift = (50 * abs(phase) / 30)  # float 0..50

        r = _clamp_color_value(self.base_color[0] + color_shift)
        g = _clamp_color_value(self.base_color[1])
        b = _clamp_color_value(self.base_color[2] + color_shift)

        glow = (r, g, b)

        draw_rect = pygame.Rect(
            int(self.rect.x - offset[0]),
            int(self.rect.y - offset[1]),
            self.rect.width,
            self.rect.height
        )

        # Draw glow (filled) and a border for clarity
        pygame.draw.rect(surf, glow, draw_rect, border_radius=6)
        pygame.draw.rect(surf, (0, 0, 0), draw_rect, width=1, border_radius=6)
