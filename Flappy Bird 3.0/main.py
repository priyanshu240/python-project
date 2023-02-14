import random
import sys
import pygame
from pygame.locals import *

GameFps = 32
WIDTH = 289
HEIGHT = 511
SCREEN_SIZE = pygame.display.set_mode((WIDTH, HEIGHT))
GROUND = HEIGHT * 0.8
SPRITES = {}
SOUNDS = {}
PLAYER = 'resources\SPRITES\\bird.png'
BACKGROUND = 'resources\SPRITES\\bg.jpg'
PIPE = 'resources\SPRITES\pipe.png '

def mainGame():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('resources/AUDIO/bg_song.mp3')
    pygame.mixer.music.play()
    score = 0
    playerx = int(WIDTH / 5)
    playery = int (HEIGHT / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10  
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:

        for event in pygame.event.get():
           
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return     

        playerMidPos = playerx + SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                SOUNDS['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUND - playery - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN_SIZE.blit(SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN_SIZE.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN_SIZE.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN_SIZE.blit(SPRITES['base'], (basex, GROUND))
        SCREEN_SIZE.blit(SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += SPRITES['numbers'][digit].get_width()
        Xoffset = (WIDTH - width) / 2

        for digit in myDigits:
            SCREEN_SIZE.blit(SPRITES['numbers'][digit], (Xoffset, HEIGHT * 0.12))
            Xoffset += SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(GameFps)

def welcomeScreen():
    playerx = int(WIDTH / 5)
    playery = int(HEIGHT - SPRITES['player'].get_height()) / 2
    messagex = int(WIDTH - SPRITES['message'].get_width()) / 2
    messagey = int(HEIGHT * 0.13)
    basex = 0
    
    playbutton = pygame.Rect(108,222,68,65)

    while True:
        for event in pygame.event.get():
            if event.type== QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0] > playbutton[0]  and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]:
                if pygame.mouse.get_pos()[1] > playbutton[1]  and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if playbutton.collidepoint(pygame.mouse.get_pos()):
            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mainGame()

            else :
                SCREEN_SIZE.blit(SPRITES['background'], (0, 0))
                SCREEN_SIZE.blit(SPRITES['player'], (playerx, playery))
                SCREEN_SIZE.blit(SPRITES['message'], (messagex, messagey))
                SCREEN_SIZE.blit(SPRITES['base'], (basex, GROUND))

                pygame.mixer.music.load('resources/AUDIO/intro_song.mp3')
                pygame.mixer.music.play()
                pygame.display.update()
                FPSCLOCK.tick(GameFps)

def getRandomPipe():            
    pipeHeight = SPRITES['pipe'][0].get_height()
    offset = HEIGHT / 4.5
    y2 = offset + random.randrange(0, int(HEIGHT - SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [ 
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUND - 25  or playery<0:
        SOUNDS['hit'].play()
        pygame.mixer.music.stop()
        gameOver()

    for pipe in upperPipes:
        pipeHeight = SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < SPRITES['pipe'][0].get_width()-20):
            SOUNDS['hit'].play()
            print(playerx, pipe['x'],)
            pygame.mixer.music.stop()
            gameOver()
            

    for pipe in lowerPipes:
        if (playery + SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < SPRITES['pipe'][0].get_width()-20:
            SOUNDS['hit'].play()
            pygame.mixer.music.stop()
            gameOver()

    return False

def gameOver():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Mini Bird')
    SPRITES['OVER'] = pygame.image.load('resources/SPRITES/gameover.png').convert_alpha()
    SPRITES['RETRY'] = pygame.image.load('resources/SPRITES/retry.png').convert_alpha()
    SPRITES['HOME'] = pygame.image.load('resources/SPRITES/Home.png').convert_alpha()
    SCREEN.blit(SPRITES['background'], (0, 0))
    SCREEN.blit(SPRITES['base'], (0, GROUND))
    SCREEN.blit(SPRITES['OVER'], (0, 0))
    SCREEN.blit(SPRITES['RETRY'], (30, 220))
    SCREEN.blit(SPRITES['HOME'], (30, 280))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
 
            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]< 30+SPRITES['RETRY'].get_width():
                if pygame.mouse.get_pos()[1]>220 and pygame.mouse.get_pos()[1]< 220+SPRITES['RETRY'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        
                        mainGame()

            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]< 30+SPRITES['HOME'].get_width():
                if pygame.mouse.get_pos()[1]>280 and pygame.mouse.get_pos()[1]< 280+SPRITES['HOME'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomeScreen()
            
if __name__ == "__main__":

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Mini Bird')

    SPRITES['numbers'] = (
        pygame.image.load('resources\SPRITES\\0.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\1.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\2.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\3.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\4.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\5.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\6.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\7.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\8.png').convert_alpha(),
        pygame.image.load('resources\SPRITES\\9.png').convert_alpha(),
    ) 
    
    
    SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    SPRITES['message'] = pygame.image.load('resources\SPRITES\message.jpeg').convert_alpha()
    SPRITES['base'] = pygame.image.load('resources\SPRITES\\base.png').convert_alpha()
    SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

  
    SOUNDS['hit'] = pygame.mixer.Sound('resources\AUDIO\death_sound.mp3')
    SOUNDS['point'] = pygame.mixer.Sound('resources\AUDIO\point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('resources\AUDIO\swoosh.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('resources\AUDIO\wing.wav')
    while True:
        welcomeScreen()
        mainGame()