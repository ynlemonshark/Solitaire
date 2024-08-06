import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN
from random import shuffle

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

card_size = (120, 180)
shapes = 4
shape_topleft = (10, 10)
shape_size = (18, 18)
shape_image = pygame.transform.scale(pygame.image.load("resources/card_shapes.png"),
                                     (shape_size[0] * shapes, shape_size[1]))

denominations = 13
denomination_topleft = (12, 30)
denomination_size = (14, 18)
denomination_image = pygame.transform.scale(pygame.image.load("resources/card_donominations.png"),
                                            (denomination_size[0] * denominations,
                                             denomination_size[1] * shapes))

card_images = []
for e_number in range(shapes * denominations):
    e_image = pygame.transform.scale(pygame.image.load("resources/card_frame.jpg"), card_size)
    e_image.blit(shape_image, shape_topleft, ((e_number % shapes) * shape_size[0], 0, shape_size[0], shape_size[1]))
    e_image.blit(denomination_image, denomination_topleft,
                 ((e_number // shapes) * denomination_size[0], (e_number % shapes) * denomination_size[1],
                  denomination_size[0], denomination_size[1]))
    e_image = pygame.transform.rotate(e_image, 180)
    e_image.blit(shape_image, shape_topleft, ((e_number % shapes) * shape_size[0], 0, shape_size[0], shape_size[1]))
    e_image.blit(denomination_image, denomination_topleft,
                 ((e_number // shapes) * denomination_size[0], (e_number % shapes) * denomination_size[1],
                  denomination_size[0], denomination_size[1]))

    card_images.append(e_image)

foundation_start_topleft = (30, 30)
foundation_distance = 150
foundation_rects = []
for e_shape in range(shapes):
    foundation_rects.append(Rect(foundation_start_topleft[0] + e_shape * foundation_distance,
                                 foundation_start_topleft[1], card_size[0], card_size[1]))

foundation_empty_image = pygame.transform.scale(pygame.image.load("resources/foundation_void.png"),
                                                (card_size[0] * shapes, card_size[1]))
stacks_number = 7
stacks_first_topleft = (30, 250)
stacks_distance = 150
stacks_toplefts = []
for e_number in range(stacks_number):
    stacks_toplefts.append((stacks_first_topleft[0] + e_number * stacks_distance, stacks_first_topleft[1]))

stacking_distance = 50


card_cover = pygame.transform.scale(pygame.image.load("resources/card_cover.png"), card_size)



def card_number(shape, denomination):
    return shape + denomination * 4

def main():
    CHANNEL = "LOBBY"

    deck = list(range(shapes * denominations))

    shuffle(deck)

    foundations = [0, 0, 0, 0]
    stacks = []
    for em_number in range(stacks_number):
        em_list = []
        for em_repeat in range(em_number + 1):
            em_list.append(deck.pop())
        stacks.append(em_list)

    covered = list(range(stacks_number))

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

        elif CHANNEL == "GAME":
            for ew_shape in range(shapes):
                SURFACE.blit(foundation_empty_image, foundation_rects[ew_shape].topleft,
                             (card_size[0] * ew_shape, 0, card_size[0], card_size[1]))
                if foundations[ew_shape]:
                    SURFACE.blit(card_images[card_number(ew_shape, foundations[ew_shape] - 1)],
                                 foundation_rects[ew_shape].topleft)

            for ew_number in range(stacks_number):
                for ew_repeat in range(len(stacks[ew_number])):
                    if covered[ew_number] > ew_repeat:
                        SURFACE.blit(card_cover, (stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] +
                                                 stacking_distance * ew_repeat))
                    else:
                        SURFACE.blit(card_images[stacks[ew_number][ew_repeat]],
                                     (stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] + stacking_distance
                                      * ew_repeat))


        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
