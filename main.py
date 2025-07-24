import sys

import pygame

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640,480))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("NEA Jacsen Lai Teleporting Platformer")

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                pygame.display.update()
                self.clock.tick(60)        

Game().run()
