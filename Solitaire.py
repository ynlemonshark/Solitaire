import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN

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


play_button_rect = Rect(800, 600, 300, 100)
play_button_image = pygame.transform.scale(pygame.image.load("resources/play_button.png"), play_button_rect.size)


def main():
    CHANNEL = "LOBBY"
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif pygame_event.type == MOUSEBUTTONDOWN:
                event_pos = (pygame_event.pos[0] / display_ratio_x,
                             pygame_event.pos[1] / display_ratio_y)

                if CHANNEL == "LOBBY":
                    if play_button_rect.collidepoint(event_pos):
                        CHANNEL = "GAME"

        SURFACE.fill((255, 0, 0))
        SURFACE.blit(backgrounds[CHANNEL], (0, 0))

        if CHANNEL == "LOBBY":
            SURFACE.blit(play_button_image, play_button_rect.topleft)

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
