import pygame
import sys
from pygame.locals import QUIT

Display_width = 1200
Display_height = 800

Surface_width = 1200
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = 40

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

channels = ("LOBBY", "GAME")
backgrounds = {}
for e_channel in channels:
    backgrounds[e_channel] = pygame.transform.scale(pygame.image.load("resources/backgrounds/{}.png".format(e_channel)),
                                                    (Surface_width, Surface_height))


def main():
    CHANNEL = "LOBBY"
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 0, 0))
        SURFACE.blit(backgrounds[CHANNEL], (0, 0))

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
