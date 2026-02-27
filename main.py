import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

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
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

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
        self.image = pygame.image.load('graphics/lazer.png').convert_alpha()
        self.rect = self.image.get_rect(midright = (x, y))
    
    def kill_bullet(self):
        if self.rect.x >= 900:
            self.kill()

    def update(self):
        self.rect.x += 8
        self.kill_bullet()

def display_score(kills):
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score = current_time + kills
    score_surface = test_font.render(f'Score : {score}', False, (64,64,64))
    score_rectangle = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface, score_rectangle)
    return score

def collision_player_obstacle():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        projectile_group.empty()
        player.sprite.rect.bottom = 300
        return False
    else: return True

def collision_projectile_obastacle(projectile_group, obstacle_group):
    collisions = pygame.sprite.groupcollide(projectile_group, obstacle_group, True, True)
    return(len(collisions))



pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
kills = 0
last_shot_time = 0
shoot_cooldown = 2000

player=pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

projectile_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

cooldown_bar15 = pygame.image.load('graphics/cooldown_bar/Health bar15.png')
cooldown_bar0 = pygame.image.load('graphics/cooldown_bar/Health bar0.png')
cooldown_bar2 = pygame.image.load('graphics/cooldown_bar/Health bar2.png')
cooldown_bar4 = pygame.image.load('graphics/cooldown_bar/Health bar4.png')
cooldown_bar6 = pygame.image.load('graphics/cooldown_bar/Health bar6.png')
cooldown_bar8 = pygame.image.load('graphics/cooldown_bar/Health bar8.png')
cooldown_bar10 = pygame.image.load('graphics/cooldown_bar/Health bar10.png')
cooldown_bar12 = pygame.image.load('graphics/cooldown_bar/Health bar12.png')
cooldown_bar14 = pygame.image.load('graphics/cooldown_bar/Health bar14.png')
cooldown_bar= [cooldown_bar15, cooldown_bar0, cooldown_bar2, cooldown_bar4, cooldown_bar6, cooldown_bar8, cooldown_bar10, cooldown_bar12, cooldown_bar14]
cooldown_index = 0

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_title_surface = test_font.render('Runner', False, (111,196,169))
game_title_rectangle = game_title_surface.get_rect(center=(400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rectangle = game_message.get_rect(center=(400,330))

obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1000)

cooldown_bar_timer = pygame.USEREVENT +2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
    
            if event.type == pygame.MOUSEBUTTONUP:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= shoot_cooldown:
                    last_shot_time = current_time
                    cooldown_index = 1
                    pygame.time.set_timer(cooldown_bar_timer, 250, 8)
                    projectile_group.add(projectile(player.sprite.rect.midright[0], player.sprite.rect.midright[1]))

            if event.type == cooldown_bar_timer:
                cooldown_index +=1
                if cooldown_index > 8: cooldown_index = 0


        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)


    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(cooldown_bar[cooldown_index],(10,300))

        score = display_score(kills)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        projectile_group.draw(screen)
        projectile_group.update()

        game_active = collision_player_obstacle()
 
        kills += collision_projectile_obastacle(projectile_group, obstacle_group)
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_title_surface, game_title_rectangle)

        score_message = test_font.render(f'Your score : {score}',False, (111,196,169))
        score_message_rectangle = score_message.get_rect(center=(400,330))
        player_gravity=0
        if score != 0:
            screen.blit(score_message, score_message_rectangle)
        else:
            screen.blit(game_message, game_message_rectangle)

    pygame.display.update()
    clock.tick(60)

