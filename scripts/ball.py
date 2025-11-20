import pygame
import math

class Ball:
    def __init__(self, game, pos, direction):
        self.game = game
        self.pos = pygame.Vector2(pos)
        self.radius = 3
        self.color = (255, 100, 100)

        # --- Motion setup ---
        self.speed = 3
        self.direction = direction  # +1 right, -1 left

        # 45° throw angle (upward)
        angle = math.radians(45)
        self.vel = pygame.Vector2(
            math.cos(angle) * self.speed * self.direction,
            -math.sin(angle) * self.speed
        )

        # Physics
        self.gravity = 0.05
        self.bounce_factor = 0.8  # how much energy it keeps after bouncing
        self.bounce_count = 0
        self.max_bounces = 10
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

            # Check collisions
        for rect in tilemap.physics_rects_around((self.pos.x, self.pos.y)):
            if ball_rect.colliderect(rect):
                # Compute overlap distances
                overlap_left   = ball_rect.right - rect.left
                overlap_right  = rect.right - ball_rect.left
                overlap_top    = ball_rect.bottom - rect.top
                overlap_bottom = rect.bottom - ball_rect.top

                # Find smallest overlap → correct collision axis
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_left and self.vel.x > 0:
                    self.pos.x -= overlap_left
                    self.vel.x *= -self.bounce_factor
                elif min_overlap == overlap_right and self.vel.x < 0:
                    self.pos.x += overlap_right
                    self.vel.x *= -self.bounce_factor
                elif min_overlap == overlap_top and self.vel.y > 0:
                    self.pos.y -= overlap_top
                    self.vel.y *= -self.bounce_factor
                elif min_overlap == overlap_bottom and self.vel.y < 0:
                    self.pos.y += overlap_bottom
                    self.vel.y *= -self.bounce_factor

                # Count bounces
                self.bounce_count += 1
                if self.bounce_count >= self.max_bounces:
                    self.alive = False
                    break

        # Off-screen cleanup
        if self.pos.y > 1000 or self.pos.x < -100 or self.pos.x > 2000:
            self.alive = False

    def draw(self, surf, offset=(0, 0)):
        draw_pos = (int(self.pos.x - offset[0]), int(self.pos.y - offset[1]))
        pygame.draw.circle(surf, self.color, draw_pos, self.radius)
