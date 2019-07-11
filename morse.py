import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1200
WINDOWHEIGHT = 80
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUNDCOLOR = WHITE
TEXTCOLOR = BLACK

FPS = 60

ADDNEWBADDIERATE = 150
BADDIESPEED = -1
BADDIESIZE = 40

DIT = 1
DAH = 3 * DIT
SYMBOLGAP = DIT
LETTERGAP = 3 * DIT
WORDGAP = 7 * DIT

timingMultiplier = 100
fuzzFactor = 1.5

BADDIEPATTERNS = {
    'A': [DIT, DAH],
    'B': [DAH, DIT, DIT, DIT],
    'C': [DAH, DIT, DAH, DIT],
    'D': [DAH, DIT, DIT],
    'E': [DIT],
    'F': [DIT, DIT, DAH, DIT],
    'G': [DAH, DAH, DIT],
    'H': [DIT, DIT, DIT, DIT],
    'I': [DIT, DIT],
    'J': [DIT, DAH, DAH, DAH],
    'K': [DAH, DIT, DAH],
    'L': [DIT, DAH, DIT, DIT],
    'M': [DAH, DAH],
    'N': [DAH, DIT],
    'O': [DAH, DAH, DAH],
    'P': [DIT, DAH, DAH, DIT],
    'Q': [DAH, DAH, DIT, DAH],
    'R': [DIT, DAH, DIT],
    'S': [DIT, DIT, DIT],
    'T': [DAH],
    'U': [DIT, DIT, DAH],
    'V': [DIT, DIT, DIT, DAH],
    'W': [DIT, DAH, DAH],
    'X': [DAH, DIT, DIT, DAH],
    'Y': [DAH, DIT, DAH, DAH],
    'Z': [DAH, DAH, DIT, DIT],
    '1': [DIT, DAH, DAH, DAH, DAH],
    '2': [DIT, DIT, DAH, DAH, DAH],
    '3': [DIT, DIT, DIT, DAH, DAH],
    '4': [DIT, DIT, DIT, DIT, DAH],
    '5': [DIT, DIT, DIT, DIT, DIT],
    '6': [DAH, DIT, DIT, DIT, DIT],
    '7': [DAH, DAH, DIT, DIT, DIT],
    '8': [DAH, DAH, DAH, DIT, DIT],
    '9': [DAH, DAH, DAH, DAH, DIT],
    '0': [DAH, DAH, DAH, DAH, DAH],
}

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('S.A.M.urai')
pygame.mouse.set_visible(False)

playerImage = [pygame.image.load('resources/adventurer-run3-0{}.png'.format(i)) for i in range(6)]
playerRect = playerImage[0].get_rect()
playerRect.centery = WINDOWHEIGHT / 2

baddieAddCounter = 0
baddies = []

font = pygame.font.SysFont(None, 72)

def playerHasHitBaddie(player, baddies):
    return False

def terminate():
    pygame.quit()
    sys.exit()

def spawnBaddie(baddies):
    newBaddie = {
            'rect': pygame.Rect(
                WINDOWWIDTH,
                (WINDOWHEIGHT - BADDIESIZE) / 2,
                BADDIESIZE,
                BADDIESIZE
            ),
            'character': random.choice(list(BADDIEPATTERNS.keys()))
    }
    newBaddie['surface'] = font.render(newBaddie['character'], 1, TEXTCOLOR)

    baddies.append(newBaddie)


def killBaddie(baddies, baddy):
    baddies.remove(baddy)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def fire(attackSequence, baddies):
    print(attackSequence)
    if len(baddies) > 0:
        if attackSequence == BADDIEPATTERNS[baddies[0]['character']]:
            killBaddie(baddies, baddies[0])


attackSequence = []
playerIndex = 0

gapStartTime = pygame.time.get_ticks()
keying = False

while True:
    if len(baddies) == 0:
        spawnBaddie(baddies)
        BADDIESPEED -= 0.1
    now = pygame.time.get_ticks()
    if (now - gapStartTime > SYMBOLGAP * timingMultiplier * fuzzFactor) and not keying and len(attackSequence) > 0:
        fire(attackSequence, baddies)
        attackSequence = []
        gapStartTime = now

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            terminate()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                keying = True
                keyStartTime = gapEndTime = pygame.time.get_ticks()
                gapElapsedTime = gapEndTime - gapStartTime

        if event.type == KEYUP:
            if event.key == K_SPACE:
                keying = False
                keyEndTime = gapStartTime = pygame.time.get_ticks()
                keyElapsedTime = keyEndTime - keyStartTime

                if keyElapsedTime < DIT * timingMultiplier * fuzzFactor:
                    attackSequence.append(DIT)
                elif keyElapsedTime < DAH * timingMultiplier * fuzzFactor:
                    attackSequence.append(DAH)
                else: # too long
                    attackSequence = []

                    

            #if event.key == K_m:
            #    if musicPlaying:
            #        pygame.mixer.music.stop()
            #    else:
            #        pygame.mixer.music.play(-1, 0.0)
            #    musicPlaying = not musicPlaying
#        if event.type == MOUSEBUTTONUP:
#            foods.append(pygame.Rect(event.pos[0] - FOODSIZE // 2, event.pos[1] - FOODSIZE // 2, FOODSIZE, FOODSIZE))
            

    for b in baddies:
        b['rect'].move_ip(BADDIESPEED, 0)

    for b in baddies[:]:
        if b['rect'].left < 0:
            killBaddie(baddies, b)

    windowSurface.fill(BACKGROUNDCOLOR)

    windowSurface.blit(playerImage[(playerIndex // 4) % 6], playerRect)
    playerIndex = (playerIndex + 1)

    for b in baddies:
        windowSurface.blit(b['surface'], b['rect'])

    #drawText('Score: %s' % (score), font, windowSurface, 10, 0)
    #drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

    pygame.display.update()

    if playerHasHitBaddie(playerRect, baddies):
        topScore = max(topScore, score)
        break

    mainClock.tick(FPS)


