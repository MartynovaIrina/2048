
import json
import os
import pygame
import sys

from database import get_best, insert_result
from logics import *

# main settings
COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (128, 128, 128),
    2: (205, 192, 176),
    4: (238, 220, 130),
    8: (205, 190, 112),
    16: (205, 102, 0),
    32: (255, 165, 0),
    64: (255, 128, 0),
    128: (238, 64, 0),
    256: (255, 69, 0),
    512: (205, 55, 0),
    1024: (238, 18, 137),
    2048: (255, 20, 147)
}
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)

BLOCKS = 4
BLOCK_SIZE = 110
MARGIN = 10
WIDTH = BLOCKS * BLOCK_SIZE + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_RECTANGLE = pygame.Rect(0, 0, WIDTH, 110)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
PLAYERS_DB = get_best()


def draw_top_players():
    '''shows 3 top players'''
    font_top = pygame.font.SysFont('comicsansms', 30)
    font_player = pygame.font.SysFont('comicsansms', 14)
    text_top = font_top.render('Best tries: ', True, COLOR_TEXT)
    screen.blit(text_top, (250, 5))
    for index, player in enumerate(PLAYERS_DB, 1):
        name, score = player
        to_show = f'{index}. {name} - {score}'
        text_player = font_player.render(to_show, True, COLOR_TEXT)
        screen.blit(text_player, (250, 23 + 20*index))


def draw_interface(score, delta=0):
    '''shows main interface'''
    pygame.draw.rect(screen, WHITE, TITLE_RECTANGLE)
    font = pygame.font.SysFont('comicsansms', 70)
    font_score = pygame.font.SysFont('comicsansms', 36)
    font_delta = pygame.font.SysFont('comicsansms', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 0))
    screen.blit(text_score_value, (20, 35))
    if delta > 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (25, 65))
    draw_top_players()
    for row in range(BLOCKS):
        # this part is to show the numbers in the cells
        for column in range(BLOCKS):
            value = array[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * BLOCK_SIZE + (column + 1) * MARGIN
            h = row * BLOCK_SIZE + (row + 1) * MARGIN + BLOCK_SIZE
            pygame.draw.rect(
                screen, COLORS[value], (w, h, BLOCK_SIZE, BLOCK_SIZE))
            if value != 0:
                # searching for the width and height of the value text
                font_w, font_h = text.get_size()
                # searching for text coordinates in cell in line
                text_i = w + (BLOCK_SIZE - font_w) / 2
                # searching for text coordinates in cell in column
                text_j = h + (BLOCK_SIZE - font_h) / 2
                screen.blit(text, (text_i, text_j))


def reset_value():
    global array, score
    array = [[0]*4 for _ in range(4)]
    empty = get_empty_cells(array)
    random.shuffle(empty)
    random_cell_1 = empty.pop()
    random_cell_2 = empty.pop()
    i_1, j_1 = get_index_from_position(random_cell_1)
    array = add_2_or_4(array, i_1, j_1)
    i_2, j_2 = get_index_from_position(random_cell_2)
    array = add_2_or_4(array, i_2, j_2)
    score = 0


array = None
score = None
USER_NAME = None
path = os.getcwd()
if 'data.txt' in os.listdir():
    with open('data.txt') as file:
        data = json.load(file)
        array = data['array']
        score = data['score']
        USER_NAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
else:
    reset_value()


def draw_intro():
    '''shows intro screen and asking to type the name'''
    global USER_NAME
    img2048 = pygame.image.load('intro.png')
    font = pygame.font.SysFont('comicsansms', 50)
    text_welcome = font.render('Welcome!', True, WHITE)
    name = 'Enter name'
    while USER_NAME is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Enter name':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and len(name) > 2:
                    USER_NAME = name
                    break
        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        screen.blit(text_welcome, (230, 90))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    '''shows game over screen'''
    global USER_NAME, array, PLAYERS_DB
    img2048 = pygame.image.load('intro.png')
    font = pygame.font.SysFont('comicsansms', 20)
    text_game_over = font.render('Game over!', True, WHITE)
    text_score = font.render(f'You got {score}!', True, WHITE)
    best_score = PLAYERS_DB[0][1]
    if score > best_score:
        text = 'New record!'
    else:
        text = f'The record is still {best_score}'
    text_record = font.render(text, True, WHITE)
    insert_result(USER_NAME, score)
    PLAYERS_DB = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with saved name
                    make_decision = True
                    reset_value()
                elif event.key == pygame.K_RETURN:
                    # restart game without name
                    USER_NAME = None
                    make_decision = True
                    reset_value()
        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 90))
        screen.blit(text_score, (15, 250))
        screen.blit(text_record, (15, 350))
        screen.blit(pygame.transform.scale(img2048, (200, 200)), (10, 10))
        pygame.display.update()
    screen.fill(BLACK)


def save_game():
    '''saves the game when closing it'''
    data = {
        'user': USER_NAME,
        'score': score,
        'array': array
    }
    with open('data.txt', 'w') as backup:
        json.dump(data, backup)


def game_loop():
    '''main game loop'''
    global score, array
    draw_interface(score)
    pygame.display.update()
    is_array_move = False
    while is_zero_in_array(array) or can_move(array):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    array, delta, is_array_move = move_left(array)
                elif event.key == pygame.K_RIGHT:
                    array, delta, is_array_move = move_right(array)
                elif event.key == pygame.K_UP:
                    array, delta, is_array_move = move_up(array)
                elif event.key == pygame.K_DOWN:
                    array, delta, is_array_move = move_down(array)
                score += delta
                if is_zero_in_array(array) and is_array_move:
                    empty = get_empty_cells(array)
                    random.shuffle(empty)
                    random_cell = empty.pop()
                    i, j = get_index_from_position(random_cell)
                    array = add_2_or_4(array, i, j)
                    is_array_move = False
                draw_interface(score, delta)
                pygame.display.update()


if __name__ == '__main__':
    while True:
        if USER_NAME is None:
            draw_intro()
        game_loop()
        draw_game_over()
