import pygame
import math

class Ball:
    def __init__(self, game, pos, direction):
        self.game = game
        self.pos = pygame.Vector2(pos)
        self.radius = 4
        self.color = (255, 100, 100)

        # --- Motion setup ---
        self.speed = 6
        self.direction = direction  # +1 right, -1 left

        # 45° throw angle (upward)
        angle = math.radians(45)
        self.vel = pygame.Vector2(
            math.cos(angle) * self.speed * self.direction,
            -math.sin(angle) * self.speed
        )

        # Physics
        self.gravity = 0.25
        self.bounce_factor = 0.6  # how much energy it keeps after bouncing
        self.bounce_count = 0
        self.max_bounces = 3
        self.alive = True

    def update(self, tilemap):
        # Apply gravity
        self.vel.y += self.gravity
        self.pos += self.vel

        # Collision rect for ball
        ball_rect = pygame.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        # Check for collisions with nearby tiles
        for rect in tilemap.physics_rects_around((self.pos.x, self.pos.y)):
            if ball_rect.colliderect(rect):
                # Horizontal bounce
                if abs(rect.left - ball_rect.right) < 6 and self.vel.x > 0:
                    self.pos.x = rect.left - self.radius
                    self.vel.x *= -self.bounce_factor
                    self.bounce_count += 1
                elif abs(rect.right - ball_rect.left) < 6 and self.vel.x < 0:
                    self.pos.x = rect.right + self.radius
                    self.vel.x *= -self.bounce_factor
                    self.bounce_count += 1

                # Vertical bounce
                if abs(rect.top - ball_rect.bottom) < 6 and self.vel.y > 0:
                    self.pos.y = rect.top - self.radius
                    self.vel.y *= -self.bounce_factor
                    self.bounce_count += 1
                elif abs(rect.bottom - ball_rect.top) < 6 and self.vel.y < 0:
                    self.pos.y = rect.bottom + self.radius
                    self.vel.y *= -self.bounce_factor
                    self.bounce_count += 1

                # limit bounces
                if self.bounce_count >= self.max_bounces:
                    self.alive = False
                    break

        # Off-screen cleanup
        if self.pos.y > 1000 or self.pos.x < -100 or self.pos.x > 2000:
            self.alive = False

    def draw(self, surf, offset=(0, 0)):
        draw_pos = (int(self.pos.x - offset[0]), int(self.pos.y - offset[1]))
        pygame.draw.circle(surf, self.color, draw_pos, self.radius)
