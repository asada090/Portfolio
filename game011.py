import random
import sys
import pygame

#import pygame.locals import*
#import itertools

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
PIPEGAPSIZE = 100
BASEY  = SCREENHEIGHT * 0.97

IMAGES,SOUNDS,HIMASKS = {},{},{}

PLAYER_LIST = (

    (
        'assets/sprites/redbird-uplap.png',
        'assets/sprites/redbird-midlap.png',
        'assets/sprites/redbird-downlap.png',
        
    ),
    (   'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',

    ),
)

BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)
try:
    xrange
except NameErroe:
    xrange = range
    
def main():
    global SCREEN,FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')
    
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
        
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'
    
    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)
    
    while True:
        randBg = random.randint(0,len(BACKGROUNDS_LIST) -1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LISY[randBg]).convert()
        
        randPlayer = random.randint(0,len(PLAYER_LIST) -1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )
        pipeindex = random.randint(0,len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),False,True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )
        
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )
        
        movementInfo = showWwlcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverSocreen(creashInfo)
        
def showWelcomeAnimation():
    playerIndex = 0
    playerIndexGen = cycle([0,1,2,1])
    
    loopIter = 0
    
    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) //2)
    
    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) //2)
    messagey = int(SCREENHEIGHT * 0.12)
    
    basex = 0
    
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    
    playerShmVals = {'val': 0 ,'dir': 1 }
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen
                }
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter +1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)
        
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],(playerx,playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'],(messagex,messagey))
        SCREEN.blit(IMAGES['base'],(basex,BASEY))
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx,playery = int(SCREENWIDTH * 0.2),movementInfo['playery']
    
    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    upperPipes = [
        {'x' : SCREENWIDTH + 200,'y':newPipe1[0]['y']}
#        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH //2),'y':newPipe1[0]['y']}
        
    ]
    lowerPipes = [
        {'x' : SCREENWIDTH + 200,'y':newPipe1[1]['y']}
#        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH //2),'y':newPipe1[1]['y']}
        
    ]
    
    pipeVelX = -4
    
    playerVelY      = -9
    playerMaxVelY   = 10
    playerMinVelY   = -8
    playerAccY      = 1
    playerRot       = 45
    playerVelRot    = 3
    playerRotThr    = 20
    playerFlapAcc   = -9
    playerFlapped   = False
    
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    if playery > -2* IMAGES['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        SOUNDS['wing'].play()
                        
        crashTest = checkCrash({'x': playerx, 'y':playery,'index':playerIndex},upperPipes,lowerPipes)
        if crashTest[0]:
            return {
                'y':playery,
                'groundCrash':crashTest[1],
                'upperPipes':upperPipes,
                'lowerPipes':lowerPipes,
                'score':score,
                'playerVelY':playerVelY,
                'playerRot':playerRot
            }
        
        playerMidPos = playerx + IMAGES['player'][0].get_width() //2
        for pipe in upperPipes:
            pipMidPos = pipe['x'] + IMSGES['pipe'][0].get_width() //2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()
                
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)
        
        if playerRot > -90:
            playerRot -= playerVelRot
            
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
            
            playerRot = 45
        
        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY,BASEY - playery - playerHeight)
        
        for uPipe,lPipe in zip(upperPipes,lowerPipes):
            