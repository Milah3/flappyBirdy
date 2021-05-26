import pygame, sys, random

from pygame.version import PygameVersion

def draw_floor(): 
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))

def create_pipes():
    pipe_height = [random.randrange(round(512 / 3 + 50), round(512 * .75), 5)]    # List of possible heights for pipes
    # pipe_height = [512 * .75]    # List of possible heights for pipes
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (600, random_pipe_pos))   # 600 a.k.a offscreen, coming in from the right
    top_pipe = pipe_surface.get_rect(midbottom = (600, random_pipe_pos - 150))

    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 450:          # 512 - 120            
            # if bottom pipe touches bottom edge of window or surpasses, draw normally, 
            screen.blit(pipe_surface, pipe) 
        else :
            #else flip the pipe that doesn't reach the bottom and draw it
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe) 

def checkCollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print("Collision detected!")
            hit_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        print("Collision detected Out of bounds!")
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,  1) 
    return new_bird

def bird_animation():           # Function creates new surface, because bird images (@ index 0, 1, 2) might have different dimensions
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100 , bird_rect.centery))       # centery not = 512 / 2, because continuity in bird flap animation
    return new_bird, new_bird_rect      # Cycles between indexes and returns different image every time, hence animated wings flapping

def display_score(game_state) : 
    if game_state == 'main_game':    
        score_surface = game_font.render(f'{int(score / 2)}', True, (255,255, 255))
        score_rect = score_surface.get_rect(center = (288 / 2, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':    
        score_surface = game_font.render(f'Score: {int(score / 2)}', True, (255,255, 255))
        score_rect = score_surface.get_rect(center = (288 / 2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score / 2)}', True, (255,255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288 / 2, 50))
        screen.blit(high_score_surface, high_score_rect)

        game_over_surface = game_font.render('Play Again', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center = (288 / 2, 420))
        screen.blit(game_over_surface, game_over_rect)
        bird_rect.centery = 512 / 2
        screen.blit(bird_surface, bird_rect)

# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=256)

pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('./text/FlappyBirdy.ttf, inkfree', 30, bold=True, italic=False)
 
# print("Fonts: ", pygame.font.get_fonts())

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True

score = 0               # keeping score
high_score = 0

bg_surface = pygame.image.load("assets/sprites/background-day.png").convert()
# bg_surface = pygame.transform.scale2x(bg_surface); # scaling to fill display surface

floor_surface = pygame.image.load("assets/sprites/base.png").convert()
floor_x_pos = 0;

# bird surface v2: bird animation (multiple images)
bird_downflap = pygame.image.load("assets/sprites/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/sprites/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]

bird_rect = bird_surface.get_rect(center = (100 , 512 / 2))

# bird surface v1: for only one image 
    # bird_surface = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
    # # bird_surface = pygame.transform.scale2x(bird_surface)
    # bird_rect = bird_surface.get_rect(center = (100 , 512 / 2))             # puts rectangle around bird_surface

pipe_surface = pygame.image.load("assets/sprites/pipe-green.png").convert()
pipe_rect = pipe_surface.get_rect(center = (200 , 512 / 4)) # puts rectangle around pipe_surface 
pipe_list = []      # Create empty pipe     
# pipe_height = [random.randrange(200, 500, 10)]    # List of possible heights for pipes

# Animate Flappy Wings
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

 
# Create rectangles using timer
SPAWNPIPE = pygame.USEREVENT                    # Create variable name for personal event
pygame.time.set_timer(SPAWNPIPE, 1500)          # Sets timer that causes SPAWNPIPE event every 1.2 sec

game_over_surface = pygame.image.load("assets/sprites/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center= (288 / 2, 512 / 2 ))

flap_sound = pygame.mixer.Sound('SFX/sfx_wing.wav')
point_sound = pygame.mixer.Sound('assets/audio/point.wav')
hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')
theme_song = pygame.mixer.Sound('assets/audio/Naruto_Fooling_Mode.mp3')

while True:  
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                pygame.mixer.Channel(0).play(flap_sound)
        
        if event.type == pygame.KEYDOWN and game_active == False:
            pipe_list.clear()
            bird_rect.center = (100, 512 / 2)
            bird_movement = 0
            score = 0
 
            game_active = True

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes()) 
            # print(pipe_list)
         
        if event.type == BIRDFLAP: 
            if (bird_index < 2):
                bird_index += 1
            else:
                bird_index = 0
        bird_surface, bird_rect = bird_animation()


    # Background 
    screen.blit(bg_surface, (0,0))          # places background image unto display surface

    if game_active:
        # Bird
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)    # shows the bird
        
        bird_movement += gravity
        bird_rect.centery += bird_movement
        # Pipes
        pipe_list = move_pipes(pipe_list)

        #update score
        for pipe in pipe_list:
            if pipe.centerx == bird_rect.centerx:
                score += 1
                pygame.mixer.Channel(1).play(point_sound)
                if score > high_score:
                    high_score = score 

        draw_pipes(pipe_list)

        game_active = checkCollision(pipe_list)
        display_score('main_game')

    else:
        # theme_song.play()
        display_score('game_over')
        screen.blit(game_over_surface, game_over_rect)
        # pygame.mixer.Channel(2).set_volume(1)             # Attempt to lower default volume; seems to have no effect
        pygame.mixer.Channel(2).play(theme_song)


    # Floor 
    floor_x_pos -= 1 
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0


    pygame.display.update()     # updates the images continously to give illusion of movement
    clock.tick(57)             #sets framerate so game isn't too fast or too slow


