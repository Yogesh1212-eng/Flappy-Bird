import random #for genarating random numbers
import sys #we will use sys.exit to exit the program 
import pygame
from pygame.locals import *  # basic pygame imports
#global variables for the game
FPS = 32
SCREENWIDTH =289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER = 'gallery/sprites/brid.png'
BACKGROUND = 'gallery/sprites/background.png'
BUILDING = 'gallery/sprites/building.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)  
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)   
    basex = 0
    
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button ,close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            #if the user presses space or up key ,start the game for them
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))  
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))  
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)  
                
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0 
    
    #create 2 building for blitting on the screen
    newBuilding1 = getRandomBuilding()
    newBuilding2 = getRandomBuilding() 
    #my list of upper building
    upperBuildings = [
        {'x':SCREENWIDTH+200, 'y':newBuilding1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newBuilding2[0]['y']},
    ]
    #my list of lower building  
    lowerBuildings = [
        {'x':SCREENWIDTH+200, 'y':newBuilding1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newBuilding2[1]['y']},
    ]
    
    buildingVelX = -4
    playerVelY = -9
    playerMaxvelY = 10
    playerMinVelY = -8
    playerAccY = 1
    
    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False #it is true only when the bird is flapping
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key ==K_SPACE or event.key == K_UP):
                if playery> 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wings'].play()
                    
        crashTest = isCollide(playerx,playery,upperBuildings,lowerBuildings) # this function will return true if the player is crashed
        if crashTest:
            return
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for building in upperBuildings:
            buildingMidPos =  building['x'] + GAME_SPRITES['building'][0].get_width()/2
            if buildingMidPos<= playerMidPos < buildingMidPos+4:
                score += 1
                print(f"your score is{score}")
                GAME_SOUNDS['point'].play()
            
            
        if playerVelY < playerMaxvelY and not playerFlapped:
            playerVelY += playerAccY
            
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        
        # move building to the left 
        for upperBuilding, lowerBuilding in zip(upperBuildings,lowerBuildings):
            upperBuilding['x'] += buildingVelX
            lowerBuilding['x'] += buildingVelX
            
        # add a new building when the frist is about to cross the leftmost part of the screen
        if 0 < upperBuildings[0]['x']<5:
            newbuilding = getRandomBuilding()
            upperBuildings.append(newbuilding[0])
            lowerBuildings.append(newbuilding[1])
            
        # if the building is out of the screen ,remove it 
        if upperBuildings[0]['x'] < -GAME_SPRITES['building'][0].get_width():
            upperBuildings.pop(0)
            lowerBuildings.pop(0)
            
        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperBuilding , lowerBuilding in zip(upperBuildings, lowerBuildings):
            SCREEN.blit(GAME_SPRITES['building'][0], (upperBuilding['x'], upperBuilding['y']))
            SCREEN.blit(GAME_SPRITES['building'][1], (lowerBuilding['x'], lowerBuilding['y']))
            
            
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['number'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2
        
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['number'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['number'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        
def isCollide(playerx,playery,upperBuildings,lowerBuildings):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for building in upperBuildings:
        buildingHeight = GAME_SPRITES['building'][0].get_height()
        if(playery < buildingHeight + building['y'] and abs(playerx - building['x']) < GAME_SPRITES['building'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
        
    for building in lowerBuildings:
        if (playery + GAME_SPRITES['player'].get_height() > building['y']) and abs(playerx - building['x']) < GAME_SPRITES['building'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
            
        
    
    
    return False                   
def getRandomBuilding():
    """generate  position of two building(one buttom straight and one top rotate) for blitting on screen
    """  
    
    buildingHeight = GAME_SPRITES['building'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() -1.2 *offset))
    buildingX = SCREENWIDTH + 10
    y1 = buildingHeight - y2 + offset
    building = [
        {'x': buildingX, 'y': -y1}, #upper Building
        {'x': buildingX, 'y': y2} # lower building
    ]
    return building   
 
if __name__=="__main__":
    #this will be the main point from where our game will start
    pygame.init() #initialise all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Yogesh Maurya')
    GAME_SPRITES['number'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        
    )
    GAME_SPRITES['message'] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha() 
    GAME_SPRITES['building'] = (pygame.transform.rotate(pygame.image.load(BUILDING).convert_alpha(),180),
    pygame.image.load(BUILDING).convert_alpha()
    )
    
    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav.mp3')
    GAME_SOUNDS['wings'] = pygame.mixer.Sound('gallery/audio/wings.wav.mp3')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    while True:
        welcomeScreen() #Shows welcome screen to user until he presses a button
        mainGame()  #This is the main game function 
