#Loads modules
import sys
import math
import random


import pygame

#Loads scripts
from scripts.utils import load_image, load_images		
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.ball import Ball


class Game:
    def __init__(self):
        pygame.init()

#Set a name, size of screen, and surface
        pygame.display.set_caption("Jacsen's Platformer")
        self.screen = pygame.display.set_mode((960, 720))
        self.display = pygame.Surface((320, 240))

#clock
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(90)

Game().run()