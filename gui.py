import pygame
from constants import *
from components.buttons import Button


keyboard = ""
buttons: list[Button] = []


def init():
    # main GUI variables
    global screen
    global square_size
    global offset

    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill((255,0,255)) #PURPLE
    square_size = screen.get_height() // GRID_HEIGHT
    offset = screen.get_width() - square_size * GRID_WIDTH

    # test button
    size = 200, 100
    position = 50, 50
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Pause")
    buttons.append(button)
    position = 50, 150
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Continue")
    buttons.append(button)
    position = 50, 250
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Death")
    buttons.append(button)

    # margin when the grid doesn't fill the screen
    margin = pygame.Rect(
        0,
        square_size * GRID_HEIGHT,
        screen.get_width(),
        screen.get_height() - square_size * GRID_HEIGHT
    )
    pygame.draw.rect(screen, BLACK, margin)


def input():
    selection = None
    option = None
    global keyboard
    exit = False

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            exit = True
        
        # if clicked, test all the buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                value = button.click(mouse)
                if value:
                    option = value

        if event.type == pygame.KEYDOWN:
            # [esc] closes the game
            if event.key == pygame.K_ESCAPE:
                exit = True

            # [backspace] remove last key
            elif event.key == pygame.K_BACKSPACE:
                keyboard = keyboard[:-1]

            # add pressed key
            else:
                keyboard += event.unicode    
    
    return selection, option, keyboard, exit


def draw():
    mouse = pygame.mouse.get_pos()

    # update mouse hovering on button
    for button in buttons:
        button.draw(mouse)

    pygame.display.flip()