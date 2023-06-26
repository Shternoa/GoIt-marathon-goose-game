import sys
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_q
import random
import os

pygame.init()

fps = pygame.time.Clock()

screen_height = 800
screen_width = 1400

font = pygame.font.SysFont('Times New Roman', 36)

# image_path = r'C:\Users\evilp\PycharmProjects\Study2\Game\goose'
image_path = os.path.join(os.path.dirname(__file__), 'goose')
player_images = os.listdir(image_path)

screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), 'background.png')),
                            (screen_width, screen_height))

bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

player_size = (40, 40)
score_color = (0, 0, 255)
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left = [-4, 0]
player_move_up = [0, -4]
player = pygame.image.load(os.path.join(os.path.dirname(__file__), 'player.png')).convert_alpha()
player_rect = player.get_rect()
player_rect.left = 0
player_rect.centery = screen_height // 2


def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load(os.path.join(os.path.dirname(__file__), 'enemy.png')).convert_alpha()
    max_y = screen_height - enemy_size[1]
    enemy_rect = pygame.Rect(screen_width, random.randint(0, max_y), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.image.load(os.path.join(os.path.dirname(__file__), 'bonus.png')).convert_alpha()
    center_x = random.randint(screen_width // 3, 2 * screen_width // 3)
    bonus_rect = pygame.Rect(center_x, 20, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_ENEMY, 2100)
pygame.time.set_timer(CREATE_BONUS, 5000)
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0
player_image_index = 0

active = True
while active:
    fps.tick(144)
    for event in pygame.event.get():
        if event.type == QUIT:
            active = False
        elif event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        elif event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        elif event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(image_path, player_images[player_image_index]))
            player_image_index += 1
            if player_image_index >= len(player_images):
                player_image_index = 0

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < - bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < - bg.get_width():
        bg_x2 = bg.get_width()

    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < screen_height:
        player_rect = player_rect.move(player_move_down)
    elif keys[K_RIGHT] and player_rect.right < screen_width:
        player_rect = player_rect.move(player_move_right)
    elif keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
    elif keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    elif keys[K_q]:
        sys.exit()

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        screen.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            active = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        screen.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    screen.blit(font.render(str(score), True, score_color), (screen_width - 30, 20))
    screen.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > screen_height:
            bonuses.pop(bonuses.index(bonus))

pygame.quit()
