import pygame
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('assets/graphics/player/player_walk_1.png')
        player_walk2 = pygame.image.load('assets/graphics/player/player_walk_2.png')
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('assets/graphics/player/jump.png')

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity = min(self.gravity + 1, 20)
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else: 
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index=0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_frame1 = pygame.image.load('assets/graphics/fly/fly1.png')
            fly_frame2 = pygame.image.load('assets/graphics/fly/fly2.png')
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('assets/graphics/snail/snail1.png')
            snail_frame2 = pygame.image.load('assets/graphics/snail/snail2.png')
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
        self.passed = False

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): 
            self.animation_index=0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/graphics/lazer.png')
        self.rect = self.image.get_rect(midright = (x, y))
    
    def kill_bullet(self):
        if self.rect.x >= 900:
            self.kill()

    def update(self):
        self.rect.x += 8
        self.kill_bullet()


class RunnerEnv(gym.Env):

    def __init__(self, render_mode=False):
        self.render_mode = render_mode
        self.gravity = 1
        self.obstacle_spawn_counter = 0
        self.spawn_interval = 60  # frames
        self.shoot_cooldown = 120
        self.clock = pygame.time.Clock()
        self.fps=120
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(10,), dtype=np.float32)

        if self.render_mode: 
            self.sky_surface=pygame.image.load('assets/graphics/Sky.png')
            self.ground_surface=pygame.image.load('assets/graphics/ground.png')
            self.screen = pygame.display.set_mode((800, 400))

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.player = Player()
        self.obstacles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.score = 0
        self.kills = 0
        self.done = False
        self.frame_count = 0
        self.last_shot_frame = 0
        return self.get_state(), {}
    
    def _apply_action(self, action):
        # 0 = rien
        # 1 = saut
        # 2 = tir

        if action == 1 and self.player.rect.bottom >= 300:
            self.player.gravity = -20

        if action == 2:
            if self.frame_count - self.last_shot_frame > self.shoot_cooldown:
                self.last_shot_frame = self.frame_count
                self.projectiles.add(projectile(
                    self.player.rect.midright[0],
                    self.player.rect.midright[1]
                ))

    def get_state(self):
            # --- Player Y ---
            player_y = self.player.rect.bottom  # 0 = top écran, 300 = sol
            player_y_norm = player_y / 300      # normalisé 0 → 1

            # --- Next obstacle ---
            if len(self.obstacles) > 0:

                obstacles_sorted = sorted(self.obstacles, key=lambda o: o.rect.x)
                obs1 = obstacles_sorted[0] if len(obstacles_sorted) > 0 else None
                obs2 = obstacles_sorted[1] if len(obstacles_sorted) > 1 else None

                distance = obs1.rect.x - self.player.rect.x
                obstacle_x_norm = np.clip(distance / 800, 0, 1)   # normalisé par largeur écran
                obstacle_y_norm = obs1.rect.bottom / 300  # normalisé par sol
                obs1_type = 0 if obs1.rect.bottom ==300 else 1
                if obs2:
                    next_obstacle_x_norm = obs2.rect.x / 800
                    next_obstacle_y_norm = obs2.rect.y / 300
                    obs2_type = 0 if obs2.rect.bottom ==300 else 1
                else: 
                    next_obstacle_x_norm = 1.5
                    next_obstacle_y_norm = 0.0
                    obs2_type = 1.5

                time_to_collision = distance / 6
                obstacle_x_distance_norm = np.clip(time_to_collision, 0, 1)
            else:
                # Pas d’obstacle visible → valeurs par défaut
                obstacle_x_norm = 1.5
                obstacle_y_norm = 1.5
                obstacle_x_distance_norm = 1.5
                next_obstacle_x_norm = 1.5
                next_obstacle_y_norm = 0.0
                obs1_type = 1.5
                obs2_type = 1.5

            # --- Cooldown ---
            cooldown_remaining = self.frame_count - self.last_shot_frame
            cooldown_remaining_norm = min(cooldown_remaining/self.shoot_cooldown, 1.0)
            
            player_vy_norm = self.player.gravity / 20
            is_grounded = 1.0 if self.player.rect.bottom >= 300 else 0.0

            # --- State vector ---
            state = [
                player_y_norm,
                player_vy_norm,
                is_grounded,
                obstacle_x_norm,
                obstacle_y_norm,
                obs1_type,
                obs2_type,
                next_obstacle_x_norm,
                next_obstacle_y_norm,
                cooldown_remaining_norm,

            ]

            return np.array(state, dtype=np.float32)
        
    def step(self, action):
        reward = 0.1
        self.frame_count += 1

        self._apply_action(action)

        # Update logique
        self.player.apply_gravity()
        self.obstacles.update()
        self.projectiles.update()

        # Spawn obstacle
        self.obstacle_spawn_counter += 1
        if self.obstacle_spawn_counter >= self.spawn_interval:
            self.obstacle_spawn_counter = 0
            self.obstacles.add(Obstacle(choice(['fly','snail','snail'])))

        # Collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.done = True
    
        kills = pygame.sprite.groupcollide(
            self.projectiles, self.obstacles, True, True
        )

        # if action ==1:
        #     reward -= 0.01
        # if action ==2:
        #     reward -= 0.03

        # reward += len(kills) * 5

        # for obstacle in self.obstacles:
        #     if obstacle.rect.right < self.player.rect.left and not hasattr(obstacle, "passed"):
        #         obstacle.passed = True
        #         reward += 3

        if self.done: reward = -10
        if self.render_mode: self.render(self.screen)
        return self.get_state(), reward, self.done, False, {}

    def render(self, screen):
        if not self.render_mode:
            return

        screen.fill((0,0,0))

        screen.blit(self.sky_surface, (0,0))
        screen.blit(self.ground_surface, (0,300))
        screen.blit(self.player.image, self.player.rect)
        self.obstacles.draw(screen)
        self.projectiles.draw(screen)
        pygame.display.update()
        self.clock.tick(self.fps)
    
