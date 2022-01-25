import pygame
from sys import exit
from random import randint
pygame.init()


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


def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 300:
        player_surface = player_jump

    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

        # walk


screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Maze Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font\Pixeltype.ttf', 50)

font2 = pygame.font.Font('font\Pixeltype.ttf', 80)


sky_surface = pygame.image.load('graphics\Sky.png').convert()
ground_surface = pygame.image.load('graphics\ground.png').convert()

#score_surface = text_font.render('My game', False, (64, 64, 64))
#score_rect = score_surface.get_rect(center=(400, 50))

# obstacles
snail_surface = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics\Fly\Fly1.png').convert_alpha()
obstacle_rect_list = []


player_walk_1 = pygame.image.load(
    'graphics\Player\player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'graphics\Player\player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics\Player\jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(60, 300))
player_gravity = 0
start_time = 0

score = 0


# intro screen
player_stand = pygame.image.load(
    'graphics\Player\player_stand.png').convert_alpha()
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
        if game_activity:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = - 20

            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_activity = True
                start_time = int(pygame.time.get_ticks()/1000)
        if event.type == obstacle_timer and game_activity:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(
                    midbottom=(randint(900, 1200), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(
                    midbottom=(randint(900, 1200), 210)))

    if game_activity:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # obstacle movement
        obstacle_movement(obstacle_rect_list)

        game_activity = collisoins(player_rect, obstacle_rect_list)

    else:
        obstacle_rect_list.clear()
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
