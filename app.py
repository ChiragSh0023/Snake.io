import pygame
import sys
import colors
import os

# To center the window
os.environ['SDL_VIDEO_CENTERED'] = '1' # Creates an enviornment variable and tells SDL to center the window

# Initialise Pygame
pygame.init()

# Creating a window for game
gameWindow = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake.io")
pygame.display.update()

# Game Specific Variables
game_exit = False
game_over = False

while not game_exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_exit = True
        
    gameWindow.fill(colors.WHITE)

    # To reflect the updated changes
    pygame.display.update()


# Quitting the game
pygame.quit()
sys.exit()    

