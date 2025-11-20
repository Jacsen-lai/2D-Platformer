import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        
        self.last_movement = [0, 0]
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        
        self.velocity[1] = min(3, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
    def render(self, surf, offset=(0, 0)):
        if hasattr(self, "teleporting") and self.teleporting:
            return
        

        img = self.game.assets['player']
        if hasattr(self, "flip") and self.flip:
            img = pygame.transform.flip(img, True, False)

        surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 0
        self.wall_slide = False
        self.coyote_time_max = 20
        self.coyote_timer = 0
        self.wall_jump_cooldown = 0
        self.teleporting = False
        self.teleport_timer = 0
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        if self.teleporting:
            self.teleport_timer -= 1
            self.velocity = [0, 0]  # freeze player

            if self.target_ball:
                self.target_ball.vel.x = 0
                self.target_ball.vel.y = 0


            if self.teleport_timer <= 0:
                # Teleport now
                self.teleporting = False

                desired = (
                    self.target_ball.pos.x - self.size[0] / 2,
                    self.target_ball.pos.y - self.size[1] / 2
                )

                safe_pos = self.find_safe_position(desired, tilemap)

                self.pos[0], self.pos[1] = safe_pos

                self.air_time = 5

                if self.target_ball in self.game.balls:
                    self.game.balls.remove(self.target_ball)
            return

            
        self.air_time += 1

        if self.air_time > 180:
            self.game.dead += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 0
            self.coyote_timer = self.coyote_time_max
        else:
            if self.coyote_timer > 0:
                self.coyote_timer -= 1
            
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)

        if self.wall_jump_cooldown > 0:
            self.wall_jump_cooldown -= 1
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True


                
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def start_teleport(self, ball):
        if not self.teleporting:
            self.teleporting = True
            self.teleport_timer = 15
            self.target_ball = ball


    def jump(self):
        if self.wall_slide and self.wall_jump_cooldown == 0:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(self.jumps -1, 0)
                self.wall_jump_cooldown = 1
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(self.jumps -1, 0)
                self.wall_jump_cooldown = 1
                return True

        if self.jumps or self.coyote_timer > 0:
            self.velocity[1] = -3
            self.air_time = 5

            if self.coyote_timer <= 0:
                self.jumps -= 1     #use a jump if not using coyote
            else:
                pass    #coyote doesnt consume a jump
            return True
        
    def find_safe_position(self, desired_pos, tilemap):
        test_rect = pygame.Rect(desired_pos[0], desired_pos[1], self.size[0], self.size[1])

        #if the position is safe, then it can be returned. 
        for rect in tilemap.physics_rects_around(desired_pos):
            if test_rect.colliderect(rect):
                break
        else:
            return desired_pos 
        

        OFFSETS = [
            (0, 0),
            (0, -4), (0, 4),
            (4, 0), (-4, 0),
            (4, -4), (4, 4),
            (-4, -4), (-4, 4),
        ]

        for dx, dy in OFFSETS:
            new_pos = (desired_pos[0] + dx, desired_pos[1] + dy)
            test_rect.x, test_rect.y = new_pos

            collision = False
            for rect in tilemap.physics_rects_around(new_pos):
                if test_rect.colliderect(rect):
                    collision = True
                    break
            if not collision:
                return new_pos 
            
        return desired_pos