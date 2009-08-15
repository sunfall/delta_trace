#!/usr/bin/env python

import pygame
from pygame.locals import *

def render_sprite_groups(*groups):
    pygame.init()

    winstyle = 0
    screen_rect = pygame.rect.Rect(0, 0, 256, 240)
    bestdepth = pygame.display.mode_ok(screen_rect.size, winstyle, 32)
    screen = pygame.display.set_mode(screen_rect.size, winstyle, bestdepth)

    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        dirty_sprites = []

        for group in groups:
            group.clear(screen, lambda sur, rect: sur.fill((0, 0, 0), rect))
            group.update()
            dirty_sprites += group.draw(screen)

        pygame.display.update(dirty_sprites)

        clock.tick(60)

    pygame.quit()

