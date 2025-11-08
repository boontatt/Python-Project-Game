def run():    
    import pygame
    from sys import exit
    from random import randint

    def display_score():
        current_time=int(pygame.time.get_ticks()/1000) - start_time #in milisecond
        score_surf = Font.render(f'Score: {current_time}',False,(64,64,64))
        score_rect = score_surf.get_rect(center = (400,50))
        screen.blit(score_surf,score_rect)
        return current_time

    

    pygame.init()
    pygame.display.set_caption("TrexRun")
    clock = pygame.time.Clock()
    Ghost_x_position = 700
    Player_x_position = 100
    Player_y_position = 500
    player_gravity = 0
    game_active = False
    start_time = 0  
    score = 0

    # Background music
    pygame.mixer.music.load("assets/sound/bgm/bgm_game1.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)

    # Sound effect
    # References for both background music and sound effect: https://mixkit.co/free-sound-effects/game/  
    enter_sound = pygame.mixer.Sound("assets/sound/T-rex/Trex_enter_game.mp3")
    gameover_sound = pygame.mixer.Sound("assets/sound/T-rex/Trex_game_over.mp3")
    jump_sound = pygame.mixer.Sound("assets/sound/T-rex/Trex_jump.mp3")
    land_sound = pygame.mixer.Sound("assets/sound/T-rex/Trex_landing.mp3")
    
    # main display screen (width,height)
    screen = pygame.display.set_mode((800,600))

    # Background
    #https://www.dreamstime.com/stock-illustration-seamless-cartoon-game-background-trees-meadow-grass-stones-hills-clouds-image88373942
    Background = pygame.image.load("assets/image/background_zheyee.jpg").convert_alpha()

    # enemy
    #https://www.pngegg.com/en/png-zvwpc
    Ghost = pygame.image.load('assets/image/ghost.png').convert_alpha()
    Ghost_rect = Ghost.get_rect(midbottom = (700,500))
    #https://apexembdesigns.com/embroidery/product/little-flying-ghost-embroidery-design
    FlyingGhost = pygame.image.load('assets/image/fly_ghost.png').convert_alpha()
    FlyingGhost_rect = FlyingGhost.get_rect(midbottom = (800,randint(200,450)))

    #player
    #https://www.redbubble.com/i/sticker/Dynamic-Dinosaurs-by-arksdesigns/23987605.EJUG5#&gid=1&pid=3
    Player = pygame.image.load("assets/image/dino.png").convert_alpha()
    Player_rect = Player.get_rect(bottomleft = (Player_x_position,Player_y_position))

    #intro screen
    #https://www.redbubble.com/i/sticker/Dynamic-Dinosaurs-by-arksdesigns/23987605.EJUG5#&gid=1&pid=3
    Dino_intro = pygame.image.load("assets/image/dino.png").convert_alpha()
    Dino_intro = pygame.transform.rotozoom(Dino_intro,0,4)
    Dino_intro_rect = Dino_intro.get_rect(center = (400,300))

    # Font
    Font = pygame.font.Font("assets/font/Pixeltype.ttf",100)
    game_name = Font.render("Trex Run",False,(111,196,169))
    game_name_rect=game_name.get_rect(center=(400,80))
    game_message = Font.render("Press space to run",False,(111,196,169))
    game_message_rect = game_message.get_rect(center = (400,515))

    # Sound effect
    click_sound = pygame.mixer.Sound("assets/sound/Click_sound.wav")

    run = True
    #Event loop
    while run:
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click_sound.play()
                    run = False
                
            if game_active:   
                
                # set player position
                Player_y_position = 500
                # enable player use keyboard to jump  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                    #only allow it to jump if player is on the ground
                        if Player_rect.bottom == 500: 
                            player_gravity = -30
                            jump_sound.play()
                # enable player use mouse click to jump  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #only allow it to jump if player is on the ground
                    if Player_rect.bottom == 500: 
                        player_gravity = -30
                        jump_sound.play()
                # press w to jump            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if Player_rect.bottom == 500: 
                            player_gravity = -30
                            jump_sound.play()
                # press s to down directly
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if Player_rect.bottom >= 0:
                            player_gravity = 30
                            land_sound.play()
            
            # game over
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        player_gravity = 0
                        Player_rect.bottom = 500 #reset the player position
                        Ghost_rect.left = 800
                        FlyingGhost_rect.left = 800
                        start_time = int(pygame.time.get_ticks()/1000) #let our score begin from zero
                        enter_sound.play()
                        pygame.mixer.music.unpause()
        
        if game_active :
            # this is our regular screen        
            screen.blit(Background,(0,0)) # dimension(800,600)
            screen.blit(Player,Player_rect)
            score=display_score()
            
            player_gravity += 1
            Player_rect.y += player_gravity
            if Player_rect.bottom >= 500:
                Player_rect.bottom=500 
                
            # ghost
            screen.blit(Ghost,(Ghost_rect)) 
            Ghost_rect.left -= 15 # speed of Ghost
            if Ghost_rect.right <= 0: Ghost_rect.left = 800  
            
            screen.blit(FlyingGhost,(FlyingGhost_rect))
            FlyingGhost_rect.left -= 7 # speed of Ghost
            if FlyingGhost_rect.right <= 0: 
                FlyingGhost_rect.left = 800
                FlyingGhost_rect.bottom = randint(225,400)
            
            # if player collide with enemy, the game stop
            if FlyingGhost_rect.colliderect(Player_rect) or Ghost_rect.colliderect(Player_rect): 
                pygame.mixer.music.pause()
                gameover_sound.play()
                game_active = False


        else:
            screen.fill((84, 117, 171))
            screen.blit(Dino_intro,Dino_intro_rect)
            
            score_message =Font.render(f"Your score : {score}",False,(111,196,169))
            score_message_rect= score_message.get_rect(center=(400,515))
            
            screen.blit(game_name,game_name_rect)
            if score == 0:
                screen.blit(game_message,game_message_rect)
            else:
                screen.blit(score_message,score_message_rect)
        
        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.load("assets/sound/bgm/bgm_mainmenu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)