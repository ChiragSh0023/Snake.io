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

# Music
pygame.mixer.init()

# Creating a window for game
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake.io")
pygame.display.update()

#image
bgimg = pygame.image.load("Images/bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

font1 = pygame.font.SysFont(None, 35)
font2 = pygame.font.SysFont(None, 50)
def score_screen(text, color, x = None, y = None, center = False, font = font1):
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

def snakeTouchItself(snake_x, snake_y, snk_list):
    # Excluding the last element, because we just pushed the head into the snk_list
    return [snake_x, snake_y] in snk_list[:-1]

clock = pygame.time.Clock()
fps = 60
# Game Loop
def gameLoop():
    pygame.mixer.music.load('Music/back.mp3')
    pygame.mixer.music.play(-1)
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
    cheat_code = ""
    cheat_trigger = "hesoyam"
    cheat_activated = False
    cheat_timer = 0
    last_cheat_key_time = 0

    # If highscore.txt does not exist
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
            
    # Reading high score
    with open("highscore.txt", "r") as f:
        highscore = int(f.readline())
    
    while not game_exit:
        if (game_over):
            gameWindow.fill(colors.WHITE)
            gameWindow.blit(bgimg, (0, 0))
            text = "Game Over! Press any key to continue."
            if (score >= highscore):
                text = "You have a new highscore!!! Press any key to continue."
                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))
            score_screen(text, colors.RED, center=True)
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
                    key_char = pygame.key.name(event.key).lower()
                    if (key_char.isalpha()):
                        current_time = pygame.time.get_ticks()
                        
                        if current_time - last_cheat_key_time > 2000:
                            cheat_code = ''
                        
                        cheat_code += key_char
                        cheat_code = cheat_code[-len(cheat_trigger):]  # Keeps only the last 7 characters in the string
                        last_cheat_key_time = current_time

                        if (cheat_code == cheat_trigger):
                            cheat_activated = True
                            cheat_timer = pygame.time.get_ticks()   # Stores the current time
                            score += 100
                            if (score > highscore):
                                highscore = score

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
            if (abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20):
                snk_length += 5
                score += 10
                if (score > highscore):
                    highscore = score
                food_x = random.randint(0, int(screen_width - 20))
                food_y = random.randint(0, int(screen_height - 20))


            gameWindow.fill(colors.WHITE)
            gameWindow.blit(bgimg, (0, 0))
            score_screen(f"Score: {score} Highscore: {highscore}", colors.RED, 10, 10)
            
            #Creating food
            pygame.draw.rect(gameWindow, colors.RED, [food_x, food_y, food_size, food_size])

            # Creating snake
            snk_list.append([snake_x, snake_y])

            # if len(snk_list) > snk_length , eg, if the snake moves forward without eating food, its length should not change. But, the new positions will be appended to snk_list. So, we have to cut the previous length
            if (len(snk_list) > snk_length):
                del snk_list[0]
            
            # If snake goes beyond the wall
            if (snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height):
                game_over = True
                pygame.mixer.music.load('Music/gameover.mp3')
                pygame.mixer.music.play()
            
            # If snake touches itself
            if snakeTouchItself(snake_x, snake_y, snk_list):
                game_over = True
                pygame.mixer.music.load('Music/gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, colors.BLACK, snk_list, snake_size)

            # Displaying cheat code activated for 2 seconds
            if (cheat_activated):
                if (pygame.time.get_ticks() - cheat_timer > 2000):
                    cheat_activated = False
                else:
                    score_screen("Cheat Code Activated!", colors.GREEN, screen_width - 280, 10)


        # if we don't use clock.tick, the game runs as fast as your CPU can handle — say, 3000 frames per second, which makes the snake very fast
        clock.tick(fps)
        # To reflect the updated changes
        pygame.display.update()

    # Quitting the game
    pygame.quit()
    sys.exit()    
    
def welcome():
    play_game = False

    while not play_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_game = True
                sys.exit()   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_game = True
            
        gameWindow.fill(colors.PINK)
        score_screen("Welcome to Snakes.io!", colors.BLACK, center=True, font=font2)
        score_screen("Press Spacebar to play", colors.RED, 260, 300, center=False)
        clock.tick(60)
        pygame.display.update()

welcome()
while True:
    gameLoop()