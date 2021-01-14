import pygame
import sys
import random


def draw_floor(image, x, y, move, width):
    screen.blit(image, (x + move, y))
    screen.blit(FLOOR, (x + move + width, y))


def create_pipe():
    random_pipe_pos = random.randint(280, 470)
    bottom_pipe = GREEN_PIPE.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = GREEN_PIPE.get_rect(midbottom=(700, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(GREEN_PIPE, pipe)

        else:
            flip_pipe = pygame.transform.flip(GREEN_PIPE, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if BLUE_BIRD_RECT.colliderect(pipe):
            return False

    if BLUE_BIRD_RECT.top <= -50 or BLUE_BIRD_RECT.bottom >= 600:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 1)
    return new_bird


WIDTH, HEIGHT = 576, 750

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FPS = 60
BG_X, BG_Y = 0, -400
FLOOR_X, FLOOR_Y = 0, 600

DAY_BACKGROUND = pygame.transform.scale2x(pygame.image.load('Images/background-day.png').convert())
FLOOR = pygame.transform.scale2x(pygame.image.load('Images/base.png').convert())
BLUE_BIRD = pygame.image.load('Images/bluebird-midflap.png').convert_alpha()
GREEN_PIPE = pygame.image.load('Images/pipe-green.png').convert()

BLUE_BIRD_RECT = BLUE_BIRD.get_rect(center=(100, HEIGHT // 2))

game_loop = True
move_floor = 0
speed = 5
pipe_speed = 5
gravity = 0.5
bird_jump = 12
bird_movement = 0
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 2000)
game_active = True

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= bird_jump

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                BLUE_BIRD_RECT.center = (100, HEIGHT // 2)
                bird_movement = 0

        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

    screen.blit(DAY_BACKGROUND, (BG_X, BG_Y))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(BLUE_BIRD)
        BLUE_BIRD_RECT.centery += bird_movement
        screen.blit(rotated_bird, BLUE_BIRD_RECT)
        game_active = check_collision(pipe_list)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    move_floor -= speed
    draw_floor(FLOOR, FLOOR_X, FLOOR_Y, move_floor, WIDTH)

    if move_floor <= -WIDTH:
        move_floor = 0

    pygame.display.update()
    clock.tick(FPS)
