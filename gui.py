import pygame
from constants import *
from components.buttons import Button
from pieces import *
import grid

keyboard = ""
buttons: list[Button] = []
mouse_down = None


def init():
    # main GUI variables
    global screen
    global square_size
    global offset

    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(LIGHT_GRAY)
    square_size = screen.get_height() // GRID_HEIGHT
    offset = screen.get_width() - square_size * GRID_WIDTH

    # test button
    size = 150, 80
    position = 50, 50
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Pause")
    buttons.append(button)
    position = 50, 140
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Slow")
    buttons.append(button)
    position = 50, 230
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Fast")
    buttons.append(button)
    # position = 50, 320 # Ufast is dev only
    # button_rect = pygame.Rect(*position, *size)
    # button = Button(screen, button_rect, "UFast")
    # buttons.append(button)

    position = 230, 50
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Attack")
    buttons.append(button)
    position = 230, 140
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Explore")
    buttons.append(button)
    position = 230, 230
    button_rect = pygame.Rect(*position, *size)
    button = Button(screen, button_rect, "Defend")
    buttons.append(button)

    # margin when the grid doesn't fill the screen
    margin = pygame.Rect(
        0,
        square_size * GRID_HEIGHT,
        screen.get_width(),
        screen.get_height() - square_size * GRID_HEIGHT
    )
    pygame.draw.rect(screen, BLACK, margin)


    console_rect = pygame.Rect(40, 350, 350, 140)
    pygame.draw.rect(screen, BLACK, console_rect) # fill black
        
    font = pygame.font.Font(FONT_STYLE, FONT_SIZE_SMALL)
    console_offset = pygame.Vector2(console_rect.topleft)

    line = font.render("Select turn speed in first column", True, WHITE) # input
    screen.blit(line, console_offset + (10,10))
    
    line = font.render("Select pieces with right click", True, WHITE) # output
    screen.blit(line, console_offset + (10,35))
    
    line = font.render("and deselect with left click", True, WHITE) # output
    screen.blit(line, console_offset + (10,60))

    line = font.render("Choose an action for the selected", True, WHITE) # output
    screen.blit(line, console_offset + (10,85))

    line = font.render("pieces in the second column", True, WHITE) # output
    screen.blit(line, console_offset + (10,110))
    


def input():
    clicked = None
    action = None
    global keyboard
    exit = False

    global mouse_down
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            exit = True
        
        # if clicked, test all the buttons
        if event.type == pygame.MOUSEBUTTONDOWN:

            position = ((mouse[0] - offset) // square_size, mouse[1] // square_size)
            if event.button == 1:
                clicked = (position, True)
            if event.button == 3:
                clicked = (position, False)

            if event.button == 1:
                for button in buttons:
                    value = button.click(mouse)
                    if value:
                        action = value

        if event.type == pygame.MOUSEBUTTONUP:

            mouse_down = None

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
    
    return clicked, action, keyboard, exit


def output(updated: bool, king_data: King):
    mouse = pygame.mouse.get_pos()

    # update mouse hovering on button
    for button in buttons:
        button.draw(mouse)

    # showing stats
    
    if updated:
        console_rect = pygame.Rect(40, 350, 350, 140)
        pygame.draw.rect(screen, BLACK, console_rect) # fill black
            
        font = pygame.font.Font(FONT_STYLE, FONT_SIZE_SMALL)
        console_offset = pygame.Vector2(console_rect.topleft)

        line = font.render("Minor piece fragment: " + str(king_data.low_piece_value), True, WHITE) # input
        screen.blit(line, console_offset + (10,10))

        line = font.render("Mayor piece fragment: " + str(king_data.high_piece_value), True, WHITE) # output
        screen.blit(line, console_offset + (10,35))

        line = font.render("Turns: " + str(grid.turn_count), True, WHITE) # output
        screen.blit(line, console_offset + (10,60))

        line = font.render("Danger level: " + str(max(0,king_data.danger)), True, WHITE) # output
        screen.blit(line, console_offset + (10,85))


    pygame.display.flip()