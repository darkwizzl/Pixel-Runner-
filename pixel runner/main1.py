import pygame
from sys import exit
from random import randint, choice
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'pixel runner\graphics\Player\player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'pixel runner\graphics\Player\player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load(
            'pixel runner\graphics\Player\jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.playe_index = 0

        self.image = self.player_walk[self.playe_index]
        self.rect = self.image.get_rect(midbottom=(90, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('pixel runner/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def animate_player(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.playe_index += 0.1
            if self.playe_index >= len(self.player_walk):
                self.playe_index = 0
            self.image = self.player_walk[int(self.playe_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_player()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'snail':
            snail1 = pygame.image.load(
                'pixel runner\graphics\snail\snail1.png').convert_alpha()
            snail2 = pygame.image.load(
                'pixel runner\graphics\snail\snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        else:
            fly1 = pygame.image.load(
                'pixel runner\graphics\Fly\Fly1.png').convert_alpha()
            fly2 = pygame.image.load(
                'pixel runner\graphics\Fly\Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1200), y_pos))

    def animate_obstacle(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill

    def update(self):
        self.animate_obstacle()
        self.rect.x -= 6
        self.destroy()


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 4.8
            if obstacle.bottom == 300:
                screen.blit(snail_surface, obstacle)
            else:
                screen.blit(fly_surf, obstacle)
        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -60]

        return obstacle_rect_list

    else:
        return []


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = text_font.render(
        f'score :{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collisoins(player_rect, obstacles):
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Maze Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('pixel runner/font/Pixeltype.ttf', 50)

font2 = pygame.font.Font('pixel runner/font/Pixeltype.ttf', 80)


sky_surface = pygame.image.load('pixel runner\graphics\Sky.png').convert()
ground_surface = pygame.image.load(
    'pixel runner\graphics\ground.png').convert()


start_time = 0

score = 0


bg_music = pygame.mixer.Sound('pixel runner/audio/music.wav')
bg_music.set_volume(0.02)
#########################################
# groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# intro screen
player_stand = pygame.image.load(
    'pixel runner\graphics\Player\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

intro_text = font2.render('Pixel Run', False, (64, 64, 64))
intro_text_rect = intro_text.get_rect(center=(400, 60))

intro_text2 = text_font.render('press ENTER to continue', False, (64, 64, 64))
intro_text2_rect = intro_text2.get_rect(center=(400, 360))


game_activity = False

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_activity:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_activity = True
                start_time = int(pygame.time.get_ticks()/1000)
        if event.type == obstacle_timer and game_activity:
            obstacle_group.add(
                Obstacle(choice(['snail', 'fly', 'snail', 'snail'])))

    if game_activity:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        bg_music.play()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_activity = collision_sprite()

    else:
        screen.fill((92, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(intro_text, intro_text_rect)
        score_txt = font2.render(f'score :{score}', False, (64, 64, 64))
        score_txt_rect = score_txt.get_rect(center=(400, 360))

        if score == 0:
            screen.blit(intro_text2, intro_text2_rect)
        else:
            screen.blit(score_txt, score_txt_rect)

    pygame.display.update()
    clock.tick(60)
