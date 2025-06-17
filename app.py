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

font = pygame.font.SysFont(None, 40)
def score_screen(text, color, x = None, y = None, center = False):
    # Renders the text as a surface
    screen_text = font.render(text, True, color)
    # gives you a rectangle the same size as your text surface
    text_rect = screen_text.get_rect()

    if center:
        # Positions the center of the rectangle at the center of the screen
        text_rect.center = (screen_width // 2, screen_height // 2 - 30)
    else:
        # Positions the text at the top left corner
        text_rect.topleft = (x, y)
    
    gameWindow.blit(screen_text, text_rect)

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Game Loop
def gameLoop():
    clock = pygame.time.Clock()

    # Game Specific Variables
    game_exit = False
    game_over = False
    snake_x = 45 # position of snake on x-axis
    snake_y = 55 # position of snake on y-axis
    snake_size = 20 # 10 * 10 snake
    fps = 60
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, int(screen_width/2)) # position of food on x-axis
    food_y = random.randint(0, int(screen_height/2)) # position of food on y-axis
    food_size = 20
    score = 0
    snk_list = []
    snk_length = 1
    while not game_exit:
        if (game_over):
            gameWindow.fill(colors.WHITE)
            score_screen("Game Over! Press any key to continue", colors.RED, center=True)
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()   
                    elif (event.type == pygame.KEYDOWN):
                        waiting = False
                        return
        
        else:
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

            if (snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height):
                game_over = True

            # Logic if snake catches the food
            if (abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20):
                snk_length += 3
                score += 10
                food_x = random.randint(0, int(screen_width))
                food_y = random.randint(0, int(screen_height))


            gameWindow.fill(colors.WHITE)
            score_screen(f"Score: {score}", colors.RED, 10, 10)
            
            #Creating food
            pygame.draw.rect(gameWindow, colors.RED, [food_x, food_y, food_size, food_size])

            # Creating snake
            snk_list.append([snake_x, snake_y])

            # if len(snk_list) > snk_length , eg, if the snake moves forward without eating food, its length should not change. But, the new positions will be appended to snk_list. So, we have to cut the previous length
            if (len(snk_list) > snk_length):
                del snk_list[0]

            plot_snake(gameWindow, colors.BLACK, snk_list, snake_size)

        # if we don't use clock.tick, the game runs as fast as your CPU can handle — say, 3000 frames per second, which makes the snake very fast
        clock.tick(fps)
        # To reflect the updated changes
        pygame.display.update()

    # Quitting the game
    pygame.quit()
    sys.exit()    
    
while True:
    gameLoop()