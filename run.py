__author__ = 'Laxl'

import pygame
from time import time
from boid import FlockController


def draw(flock):
    SCREEN.fill(BACKGROUND)
    for b in flock:
        pygame.draw.circle(SCREEN, b.colour, (int(b.pos.x), int(b.pos.y)), 15, 3)
        pygame.draw.line(SCREEN, (200, 200, 200), (int(b.pos.x), int(b.pos.y)),
                         (int(b.pos.x + b.look_direction.x),   int(b.pos.y + b.look_direction.y)), 2)

pygame.init()

BACKGROUND = (69, 52, 218)
WIDTH, HEIGHT = 1600, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
run = True

last_tick = time()
flip_time = 0.0
timer = 0.0
frames_rendered = 0

BOID_AMOUNT = 30
MOUSE_ACTIVE = True
goal_attractive = True
flock_controller = FlockController(WIDTH, HEIGHT, BOID_AMOUNT)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            goal_attractive = not goal_attractive
    dt = time() - last_tick
    flip_time += dt
    last_tick = time()
    pygame.event.pump()
    if MOUSE_ACTIVE:
        mouse_pos = pygame.mouse.get_pos()
    else:
        mouse_pos = None
    flock_controller.update((mouse_pos, goal_attractive), dt)
    draw(flock_controller.flock)
    pygame.display.flip()
    flip_time = 0.0
    frames_rendered += 1

    timer += dt

print "FPS: " +str(frames_rendered/timer)