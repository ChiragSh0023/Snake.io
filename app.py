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
snake_x = 45 # position of snake on x-axis
snake_y = 55 # position of snake on y-axis
snake_size = 10 # 20 * 20 size
fps = 30
velocity_x = 0
velocity_y = 0

clock = pygame.time.Clock()

# Game Loop
while not game_exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_exit = True
        
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                velocity_x = 5
                velocity_y = 0
            
            if (event.key == pygame.K_LEFT):
                velocity_x = -5
                velocity_y = 0
            
            if (event.key == pygame.K_UP):
                velocity_x = 0
                velocity_y = -5
            
            if (event.key == pygame.K_DOWN):
                velocity_x = 0
                velocity_y = 5
    
    snake_x += velocity_x
    snake_y += velocity_y

    gameWindow.fill(colors.WHITE)

    pygame.draw.rect(gameWindow, colors.BLACK, [snake_x, snake_y, snake_size, snake_size])

    # if we don't use clock.tick, the game runs as fast as your CPU can handle — say, 3000 frames per second, which makes the snake very fast
    clock.tick(fps)
    # To reflect the updated changes
    pygame.display.update()


# Quitting the game
pygame.quit()
sys.exit()    

