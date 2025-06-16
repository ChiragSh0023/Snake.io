import pygame
import sys
import colors
import os
import random

# To center the window
os.environ['SDL_VIDEO_CENTERED'] = '1' # Creates an enviornment variable and tells SDL to center the window

# Initialise Pygame
pygame.init()
screen_width = 800
screen_height = 600

# Creating a window for game
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake.io")
pygame.display.update()

# Game Specific Variables
game_exit = False
game_over = False
snake_x = 45 # position of snake on x-axis
snake_y = 55 # position of snake on y-axis
snake_length = 20 # 10 * 10 size
snake_width = 10 # 10 * 10 size
fps = 60
velocity_x = 0
velocity_y = 0
food_x = random.randint(0, int(screen_width/2)) # position of food on x-axis
food_y = random.randint(0, int(screen_height/2)) # position of food on y-axis
food_size = 10
score = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Game Loop
while not game_exit:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_exit = True
        
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                velocity_x = 5
                velocity_y = 0
            
            elif (event.key == pygame.K_LEFT):
                velocity_x = -5
                velocity_y = 0
            
            elif (event.key == pygame.K_UP):
                velocity_x = 0
                velocity_y = -5
            
            elif (event.key == pygame.K_DOWN):
                velocity_x = 0
                velocity_y = 5
    
    snake_x += velocity_x
    snake_y += velocity_y

    # Logic if snake catches the food
    if (abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10):
        score += 10
        food_x = random.randint(0, int(screen_width))
        food_y = random.randint(0, int(screen_height))


    gameWindow.fill(colors.WHITE)
    score_screen(f"Score: {score}", colors.RED, 10, 10)
    # Creating snake
    pygame.draw.rect(gameWindow, colors.BLACK, [snake_x, snake_y, snake_width, snake_length])
    #Creating food
    pygame.draw.rect(gameWindow, colors.RED, [food_x, food_y, 10, 10])

    # if we don't use clock.tick, the game runs as fast as your CPU can handle — say, 3000 frames per second, which makes the snake very fast
    clock.tick(fps)
    # To reflect the updated changes
    pygame.display.update()


# Quitting the game
pygame.quit()
sys.exit()    

