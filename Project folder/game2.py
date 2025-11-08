import pygame 
#  Importing modules 
#  Additional moudles 
import random
#  Additional moudles
import mainmenu

from sys import exit

def run():
    # Background music
    # References: https://www.youtube.com/watch?v=5bn3Jmvep1k&list=PLFM5gSFqaZ4_q7uHLYtBXmvQwEwENEpHu&index=8&t=260s
    pygame.mixer.music.load("assets/sound/bgm/bgm_game2.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)
    pygame.init() 
    #  Initialize pygame 

    clock = pygame.time.Clock()
    fps = 60 

    window_width = 800
    #  Define the the width of the window 
    window_heigth = 600
    #  Defined the height of the window 

    window = pygame.display.set_mode((window_width,window_heigth))
    #  Creating the game window by using pygame.display.set_mode and called it as window
    pygame.display.set_caption('Flappy Bird')
    #  The title of the window

    #  Define font
    font  = pygame.font.Font('assets/font/Pixeltype.ttf', 60)

    #  Define Colour 
    white = (255, 255, 255)

    #  Define game variable
    ground_scroll = 0
    scroll_speed = 5
    flying = False 
    game_over = False
    pipe_gap = 200 
    pipe_frequency = 1500 # milliseconds
    last_pipe = pygame.time.get_ticks() - pipe_frequency # - pipe_frequencey will make the pipe created when the game start
    score = 0
    pass_pipe = False 

    #  LOAD IMAGES
    #  Reference for background and ground https://github.com/russs123/flappy_bird/tree/main/img
    background = pygame.image.load('assets/image/background1.png')
    #  Setting window background 
    ground = pygame.image.load('assets/image/ground1.png')

    def draw_text(text, font, text_col, x , y):
        img = font.render(text, True, text_col ) 
        window.blit(img,(x,y))

    def reset_game():
        pipe_group.empty()
        flappy.rect.x= 100
        flappy.rect.y = int(window_heigth/2)
        score = 0
        return score
        #  Reset score and game


    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            #  Controlling the speed of the animation run 
            #  Reference for bird https://github.com/russs123/flappy_bird/tree/main/img
            for num in range(1, 4):
            #  Because using 3 image
                image = pygame.image.load(f'assets/image/bird{num}.png')
                self.images.append(image)
            self.image = self.images[self.index]
            # creating the bird 
            self.rect = self.image.get_rect()
            #  Make a rectangle from the boundaries of the image
            self.rect.center = [x,y]
            #  The position of the rectangle 
            self.vel = 0
            self.clicked = False 

        #  Make animation 
        def update(self):
            
            if flying == True:
            #  Make the bird start flying when we clicked it
            #  Setting Gravity
                self.vel += 0.5
                if self.vel > 7:
                #  Positive value make the bird go down 
                    self.vel = 7
                if self.rect.bottom < 500:
                    self.rect.y += int(self.vel)

            if game_over == False:
                # Setting Jump
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    jump_sound.play()
                    #  When mouse got clicked
                    self.vel = -10
                    #  Negative value make the bird go up
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                    #  When mouse released 
                
                #  Handle the animation
                self.counter += 1 
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0 
                #  Reset it back otherwise it will keep increasing 
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                    #  Make a check of the index and make sure it reset to 0 if no i will make an error
                self.image = self.images[self.index]

                #  Rotate the bird
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)
                #  When the bird hit the ground it will rotate 90 degree

    class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            #  Reference for pipe https://github.com/russs123/flappy_bird/tree/main/img
            self.image = pygame.image.load("assets/image/pipe.png")
            #  Creating pipe image
            self.rect = self.image.get_rect()
            #  Creating a rectangle boundary around the pipe
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x,y - int(pipe_gap)/2]
            #  Position 1 is from the top, -1 is from the bottom
            if position == -1:
                self.rect.topleft = [x,y + int(pipe_gap)/2]

        def update(self):
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

    # Sound effect
    # References: https://www.youtube.com/watch?v=vRMFEgaPmTE&list=PLFM5gSFqaZ4_q7uHLYtBXmvQwEwENEpHu&index=4
    flappy_fall = pygame.mixer.Sound("assets/sound/Flappy_bird/flappybird_dropafterhit.mp3")
    score_sound = pygame.mixer.Sound("assets/sound/Flappy_bird/flappybird_getpoint.wav")
    jump_sound = pygame.mixer.Sound("assets/sound/Flappy_bird/flappybird_jump.wav")
    click_sound = pygame.mixer.Sound("assets/sound/Click_sound.wav")
    bird_group = pygame.sprite.Group()

    pipe_group = pygame.sprite.Group()

    flappy = Bird( 100, int(window_heigth / 2))

    bird_group.add(flappy)

    #  Create restart button instance 
    button = mainmenu.Button("Restart", 40, (300, 100), 200, 40, window, 6)

    run = True
    #  Creating game loop
    while run: 
    #  !! If it was blank here there will be freeze and if you click 'x' button it also wont close it. !!
    #  So we need to add something here.
        
        clock.tick(fps)

        window.blit(background,(0,-200))
        #  Setting background coordinate.

        bird_group.draw(window)
        #  Make the bird on the screen 
        bird_group.update()

        pipe_group.draw(window)

        window.blit(ground,(ground_scroll,500))
        #  Setting ground coordinate

        #  Check the score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score_sound.play()
                    score += 1
                    pass_pipe = False   

        draw_text(str(score), font, white, int(window_width/2)-20, 20)         

        #  Look for collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            if not game_over:
                flappy_fall.play()
            game_over = True
            #  When the bird hit the pipe = Game over 

        #  Check if the bird hit the ground
        if flappy.rect.bottom >= 500:
            game_over = True
            flying = False 
        
        if game_over == False and flying == True:
            #  Generate new pipe 
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                #  Take 2 numbers and create a random integer between -100 , 100
                btm_pipe = Pipe(window_width, int(window_heigth / 2) + pipe_height,-1)
                top_pipe = Pipe(window_width, int(window_heigth / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe) 
                #  Add it in to group
                last_pipe = time_now
                
            ground_scroll -= scroll_speed 
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            #  Reset ground_scroll when it over 35pixel 
                
            pipe_group.update()
                #  Stop scrolling when the bird hit the ground or the pipes

        #  Check for game over and reset 
        if game_over == True:
            if flappy.rect.bottom >= 500:
                if button.draw() == True:
                    click_sound.play()
                    game_over = False
                    score = reset_game()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            #  Clicking the 'x' button on the top of the right 
                run = False
                pygame.quit()
                exit() 
                #  When we set False it will not meet the while loop required condition then it will close it 
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    run = False

        
        pygame.display.update()
    #  Call Funtion 
    pygame.mixer.music.load("assets/sound/bgm/bgm_mainmenu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)