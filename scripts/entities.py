import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)          # top-left position of the entity
        self.size = size              # (width, height)
        self.velocity = [0, 0]        # (x, y) velocity
        self.grounded = False         # track if entity is standing on ground
        self.collisions ={'up': False, 'down': False, 'right': False, 'left': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions ={'up': False, 'down': False, 'right': False, 'left': False}
        # reset grounded state each frame
        self.grounded = False

        #combine input movement and velocity
        frame_movement = [movement[0] + self.velocity[0],
                          movement[1] + self.velocity[1]]

        #Horizontal movement
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:   # moving right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                elif frame_movement[0] < 0: # moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        #Vertical movement
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # falling down onto a tile
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.grounded = True
                    self.velocity[1] = 0
                elif frame_movement[1] < 0:  # hitting head
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
                # IMPORTANT: pos[1] is the rect.top (since pos = top-left)
                self.pos[1] = entity_rect.top

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

        #Gravity
        if not self.grounded:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)
        else:
            self.velocity[1] = 0  # keep grounded, no sinking

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

