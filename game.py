import sys
import math
import random

import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.ball import Ball
from scripts.portal import Portal

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Jacsen's Platformer")
        self.screen = pygame.display.set_mode((960, 720))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.timer_running = True
        
        self.movement = [False, False]
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
        }
                
        self.player = Player(self, (0, 100), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 0
        self.max_balls = 5
        self.ballcount = 5
        self.font = pygame.font.SysFont("Impact", 14)
        self.big_font = pygame.font.SysFont("Impact", 32,)
        
        
        self.scroll = [0, 0]
        self.portals = []
        self.balls = []
        self.load_level(self.level)


    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.player.air_time = 0
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        self.portals = []
        self.ball_count = self.max_balls

        portal_positions = {
            0: (20, 18),
            1: (500, 20),
            2: (300, 130),
            3: (250, 20),
            4: (170, 30),
        }
        next_level = map_id + 1
        if map_id in portal_positions and next_level < 10:
            self.portals.append(Portal(self, portal_positions[map_id], target_level=next_level))
        if next_level == 6:
            self.timer_running = False

        
    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(self.level)
                    self.player = Player(self, (0, 100), (8, 15))
            
            if not self.dead:
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                self.tilemap.render(self.display, offset=render_scroll)
                
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            for ball in self.balls:
                ball.update(self.tilemap)

            self.balls = [b for b in self.balls if b.alive]

            for ball in self.balls:
                ball.draw(self.display, offset=render_scroll)

            for portal in self.portals:
                portal.update()
            for portal in self.portals:
                portal.draw(self.display, offset = render_scroll)    
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True  
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_r:
                        self.load_level(self.level)
                        self.player = Player(self, (0, 100), (8, 15))
                    if event.key == pygame.K_n:
                        self.level = self.level + 1
                        self.dead += 40
                    if event.key == pygame.K_SPACE and self.balls == [] and self.ball_count > 0:
                        direction = -1 if getattr(self.player, "flip", False) else 1
                        ball_pos = self.player.rect().center
                        self.balls.append(Ball(self, ball_pos, direction))

                        self.ball_count -= 1
                    if event.key == pygame.K_e:
                        if self.balls:
                            last_ball = self.balls[-1]
                            self.player.start_teleport(last_ball)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            ammo_text = self.font.render(f"Balls: {self.ball_count}/{self.max_balls}", True, (255, 255, 255))
            self.display.blit(ammo_text, (5, 5))
            #Timer
            if self.timer_running:
                self.elapsed_ms = pygame.time.get_ticks() - self.start_time
                font_used = self.font
                color = (255, 255, 255)
            else:
                font_used = self.big_font
                color = (0, 255, 0)


            elapsed_seconds = self.elapsed_ms // 1000

            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60

            timer_text = font_used.render(f"Time: {minutes:02d}:{seconds:02d}", True, color)
            self.display.blit(timer_text, (5, 20))

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(90)

Game().run()