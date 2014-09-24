__author__ = 'Laxl'

import pygame
from time import time
from boid import FlockController


def draw(flock):
    SCREEN.fill(BACKGROUND)
    for b in flock:
        pygame.draw.circle(SCREEN, b.colour, (b.pos[0], b.pos[1]), 15, 3)
        pygame.draw.line(SCREEN, (200, 200, 200), (b.pos[0], b.pos[1]),
                         (b.pos[0] + b.look_direction[0],   b.pos[1] + b.look_direction[1]), 2)

pygame.init()

BACKGROUND = (69, 52, 218)
WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
flock_controller = FlockController(WIDTH, HEIGHT, 20)
last_tick = time()
flip_time = 0.0
timer = 0.0
frames_rendered = 0

follow_goal = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    dt = time() - last_tick
    flip_time += dt
    last_tick = time()
    pygame.event.pump()
    if follow_goal:
        mouse_pos = pygame.mouse.get_pos()
    else:
        mouse_pos = None
    flock_controller.update(mouse_pos, dt)
    draw(flock_controller.flock)
    pygame.display.flip()
    flip_time = 0.0
    frames_rendered += 1

    timer += dt

print "FPS: " +str(frames_rendered/timer)