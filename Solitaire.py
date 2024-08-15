import pygame
import sys
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN, MOUSEBUTTONUP
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

black_shapes = (0, 3)
red_shapes = (1, 2)

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

stacking_distance = 30


card_cover = pygame.transform.scale(pygame.image.load("resources/card_cover.png"), card_size)

deck_topleft = (1000, 30)

deck_card_topleft = (850, 30)
deck_card_previous1_topleft = (810, 30)
deck_card_previous2_topleft = (770, 30)

deck_empty_image = pygame.transform.scale(pygame.image.load("resources/deck_empty.png"), card_size)


def card_number(shape, denomination):
    return shape + denomination * 4


def main():
    CHANNEL = "LOBBY"

    deck = list(range(shapes * denominations))

    deck_card = 0

    shuffle(deck)

    foundations = [0, 0, 0, 0]
    stacks = []
    for em_number in range(stacks_number):
        em_list = []
        for em_repeat in range(em_number + 1):
            em_list.append(deck.pop())
        stacks.append(em_list)

    covered = list(range(stacks_number))

    dragging = False
    dragging_card_data = {}

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

                elif CHANNEL == "GAME":
                    if Rect(deck_topleft, card_size).collidepoint(event_pos):
                        deck_card += 1
                        if deck_card > len(deck):
                            deck_card = 0

                    if pygame_event.button == pygame.BUTTON_LEFT:
                        for ew_number in range(stacks_number):
                            for ew_repeat in range(len(stacks[ew_number])):
                                if covered[ew_number] <= ew_repeat:
                                    if ew_repeat == len(stacks[ew_number]) - 1:
                                        ew_rect = Rect(stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] +
                                                       ew_repeat * stacking_distance, card_size[0], card_size[1])
                                    else:
                                        ew_rect = Rect(stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] +
                                                       ew_repeat * stacking_distance, card_size[0], stacking_distance)
                                    if ew_rect.collidepoint(event_pos):
                                        dragging = True
                                        dragging_card_data = {"location": "stacks", "stack": ew_number, "index": ew_repeat}

                        if Rect(deck_card_topleft, card_size).collidepoint(event_pos):
                            dragging = True
                            dragging_card_data = {"location": "deck_card"}

                    elif pygame_event.button == pygame.BUTTON_RIGHT:
                        for ew_number in range(stacks_number):
                            if Rect((stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] + stacking_distance
                                                                    * ew_number), card_size).collidepoint(event_pos):
                                ew_shape = stacks[ew_number][-1] % shapes
                                if foundations[ew_shape] == stacks[ew_number][-1] // shapes:
                                    foundations[ew_shape] += 1

                                    stacks[ew_number] = stacks[ew_number][0:-2]

                        if deck_card > 0:
                            if Rect(deck_card_topleft, card_size).collidepoint(event_pos):
                                ew_shape = deck[deck_card - 1] % shapes
                                if foundations[ew_shape] == deck[deck_card - 1] // shapes:
                                    deck.remove(deck[deck_card - 1])
                                    foundations[ew_shape] += 1

                                    deck_card -= 1

                        for ew_number in range(stacks_number):
                            if len(stacks[ew_number]) <= covered[ew_number]:
                                covered[ew_number] = len(stacks[ew_number]) - 1

            elif pygame_event.type == MOUSEBUTTONUP:
                event_pos = (pygame_event.pos[0] / display_ratio_x,
                             pygame_event.pos[1] / display_ratio_y)

                if CHANNEL == "GAME":
                    if dragging:
                        for ew_number in range(stacks_number):
                            if len(stacks[ew_number]) == 0:
                                ew_rect = Rect(stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1],
                                               card_size[0], card_size[1])
                            else:
                                ew_rect = Rect(stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1]
                                               + stacking_distance * (len(stacks[ew_number]) - 1),
                                               card_size[0], card_size[1])

                            if ew_rect.collidepoint(event_pos):
                                ew_able = []
                                if not len(stacks[ew_number]):
                                    for ew_shape in range(shapes):
                                        ew_able.append(card_number(ew_shape, denominations - 1))

                                elif stacks[ew_number][-1] // shapes != denominations - 1:
                                    ew_able_shapes = []
                                    if stacks[ew_number][-1] % shapes in black_shapes:
                                        ew_able_shapes.extend(red_shapes)
                                    else:
                                        ew_able_shapes.extend(black_shapes)

                                    for ew_shape in ew_able_shapes:
                                        ew_able.append(card_number(ew_shape, stacks[ew_number][-1] // shapes - 1))

                                ew_move = False
                                if dragging_card_data["location"] == "stacks":
                                    ew_move = stacks[dragging_card_data["stack"]][dragging_card_data["index"]] in ew_able

                                elif dragging_card_data["location"] == "deck_card":
                                    ew_move = deck[deck_card - 1] in ew_able

                                if ew_move:
                                    ew_list = []
                                    if dragging_card_data["location"] == "stacks":
                                        for ew_repeat in range(len(stacks[dragging_card_data["stack"]]) -
                                                               dragging_card_data["index"]):
                                            ew_list.append(stacks[dragging_card_data["stack"]].pop())
                                        ew_list = ew_list[::-1]
                                    elif dragging_card_data["location"] == "deck_card":
                                        ew_list.append(deck[deck_card - 1])
                                        deck[deck_card - 1] = -1
                                        deck.remove(-1)

                                        deck_card -= 1

                                    stacks[ew_number].extend(ew_list)

                                    break

                        for ew_number in range(stacks_number):
                            if len(stacks[ew_number]) <= covered[ew_number]:
                                covered[ew_number] = len(stacks[ew_number]) - 1


                        dragging = False


        SURFACE.fill((255, 0, 0))
        SURFACE.blit(backgrounds[CHANNEL], (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / display_ratio_x, mouse_pos[1] / display_ratio_y)

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
                    ew_draw_okay = False
                    if not dragging:
                        ew_draw_okay = True
                    else:
                        if dragging_card_data["location"] != "stacks":
                            ew_draw_okay = True
                        else:
                            if dragging_card_data["stack"] != ew_number or dragging_card_data["index"] > ew_repeat:
                                ew_draw_okay = True

                    if ew_draw_okay:
                        if covered[ew_number] > ew_repeat:
                            SURFACE.blit(card_cover, (stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] +
                                                     stacking_distance * ew_repeat))
                        else:
                            SURFACE.blit(card_images[stacks[ew_number][ew_repeat]],
                                         (stacks_toplefts[ew_number][0], stacks_toplefts[ew_number][1] + stacking_distance
                                          * ew_repeat))

            if deck_card != len(deck):
                SURFACE.blit(card_cover, deck_topleft)
            else:
                SURFACE.blit(deck_empty_image, deck_topleft)

            if deck_card >= 3:
                SURFACE.blit(card_images[deck[deck_card - 3]], deck_card_previous2_topleft)
            if deck_card >= 2:
                SURFACE.blit(card_images[deck[deck_card - 2]], deck_card_previous1_topleft)

            if deck_card:
                if dragging:
                    if not dragging_card_data["location"] == "deck_card":
                        SURFACE.blit(card_images[deck[deck_card - 1]], deck_card_topleft)
                else:
                    SURFACE.blit(card_images[deck[deck_card - 1]], deck_card_topleft)

            if dragging:
                if dragging_card_data["location"] == "stacks":
                    for ew_index in range(len(stacks[dragging_card_data["stack"]]) - dragging_card_data["index"]):
                        SURFACE.blit(card_images[stacks[dragging_card_data["stack"]][ew_index + dragging_card_data["index"]]],
                                     (mouse_pos[0], mouse_pos[1] + ew_index * stacking_distance))
                elif dragging_card_data["location"] == "deck_card":
                    SURFACE.blit(card_images[deck[deck_card - 1]], mouse_pos)



        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
