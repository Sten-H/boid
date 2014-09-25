__author__ = 'Laxl'

import pygame
from boid import FlockController


def draw(flock):
    SCREEN.fill(BACKGROUND)
    for b in flock:
        pygame.draw.circle(SCREEN, b.colour, (int(b.pos.x), int(b.pos.y)), 10, 0)
        pygame.draw.line(SCREEN, (200, 200, 200), (int(b.pos.x), int(b.pos.y)),
                         (int(b.pos.x + b.look_direction.x),   int(b.pos.y + b.look_direction.y)), 2)

pygame.init()

BOID_AMOUNT = 100
BACKGROUND = (69, 52, 218)
WIDTH, HEIGHT = 1600, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    run = True
    clock = pygame.time.Clock()
    frames_rendered = 0

    mouse_active = False
    goal_attractive = True
    flock_controller = FlockController(WIDTH, HEIGHT, BOID_AMOUNT)

    while run:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = pygame.mouse.get_pressed()
                print pressed
                if pressed[0]:
                    goal_attractive = not goal_attractive
                elif pressed[2]:
                    mouse_active = not mouse_active

        pygame.event.pump()
        if mouse_active:
            mouse_pos = pygame.mouse.get_pos()
        else:
            mouse_pos = None
        flock_controller.update((mouse_pos, goal_attractive), clock.get_time() / 1000.0)
        draw(flock_controller.flock)
        pygame.display.flip()
        frames_rendered += 1
    #End Main Loop
    print "FPS: " +str(frames_rendered/(pygame.time.get_ticks()/1000.0))

main()

