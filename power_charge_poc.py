import pygame, random, sys
from pygame.locals import *
from itertools import cycle

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (10, 255, 10)
RED = (255, 10, 10)
BACKGROUNDCOLOR = WHITE
TEXTCOLOR = BLACK

FPS = 60

TAPLENGTH = 90

pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
mainClock = pygame.time.Clock()

def drawPower(windowSurface, sequence):
    drawConcentricCircles(windowSurface, sequence)
    drawStackedBar(windowSurface, sequence)
    drawDashes(windowSurface, sequence)

def drawStackedBar(windowSurface, sequence):
    width = 5
    radius = 10
    windowHeight = windowSurface.get_height()
    y = windowHeight
    surface = pygame.Surface((width, windowHeight))
    surface.fill(BACKGROUNDCOLOR)

    colorCycle = cycle([GREEN, RED])
    for i in range(0, len(sequence), 2):
        if len(sequence) > i + 1:
            color = next(colorCycle)
            keyed = sequence[i+1] // TAPLENGTH + 1
            height = radius * keyed
            pygame.draw.rect(surface, color, (0, y - height, width, height))
            y -= height + 1

    windowSurface.blit(surface, (0, 0))

def drawConcentricCircles(windowSurface, sequence):
    radiusInc = 3
    circles = []
    windowWidth = windowSurface.get_width()
    windowHeight = windowSurface.get_height()
    surface = pygame.Surface((windowWidth, windowHeight))
    surface.fill(BACKGROUNDCOLOR)

    radius = 0
    for i in range(0, len(sequence), 2):
        if len(sequence) > i + 1:
            keyed = sequence[i+1] // TAPLENGTH + 1
            width = radiusInc * keyed
            circles.append(radius + width)
            radius += width

    colorCycle = cycle([GREEN, RED])
    if len(circles) % 2 == 0:
        circles.append(0)
    for c in circles[::-1]:
        color = next(colorCycle)
        pygame.draw.circle(surface, color, (windowWidth // 2, windowHeight // 2), c)
        #print('A {} {}'.format(color, c))

    windowSurface.blit(surface, (0, 0))
    #terminate()


def drawDashes(windowSurface, sequence):
    # These are fixed, should be moved out of the function
    y = radius = xStart = xEnd = 5
    surface = pygame.Surface((windowSurface.get_width(), 2*radius))
    surface.fill(BACKGROUNDCOLOR)

    for i in range(0, len(sequence), 2):
        gap = sequence[i] // TAPLENGTH
        xStart = xEnd + radius * 2 + radius * gap

        if len(sequence) > i + 1:
            keyed = sequence[i+1] // TAPLENGTH
            width = radius * keyed
            xEnd = xStart + width

            # Start dot
            pygame.draw.circle(surface, GREEN, (xStart, y), radius)

            # Middle rect
            pygame.draw.rect(surface, GREEN, (xStart, y - radius, width, radius * 2))

            # End dot
            pygame.draw.circle(surface, GREEN, (xEnd, y), radius)

    windowSurface.blit(surface, (0, 0))

def handleEvents():
    keying = False
    timingSequence = [0]
    gapStartTime = keyStartTime = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if isTerminateEvent(event):
                terminate()

            if isFireEvent(event) and not keying:
                keyStartTime = now
                timingSequence.append(0)
                keying = True

            if isCeaseFireEvent(event) and keying:
                gapStartTime = now
                timingSequence.append(0)
                keying = False

        if keying:
            timingSequence[-1] = now - keyStartTime
        else:
            timingSequence[-1] = now - gapStartTime
            if timingSequence[-1] > TAPLENGTH * 5:
                timingSequence = [0]

        yield timingSequence

def isTerminateEvent(event):
    return event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)

def isFireEvent(event):
    return event.type in (MOUSEBUTTONDOWN, FINGERDOWN) or (event.type == KEYDOWN and event.key == K_SPACE)

def isCeaseFireEvent(event):
    return event.type in (MOUSEBUTTONUP, FINGERUP) or (event.type == KEYUP and event.key == K_SPACE)

def terminate():
    pygame.quit()
    sys.exit()

def calculateSymbols(sequence):
    rectifiedSequence = rectifySequence(sequence)
    if len(rectifiedSequence) > 1:
        print(rectifiedSequence)

def rectifySequence(sequence):
    rectifiedSequence = []
    for i in range(1, len(sequence), 2):
        tap = sequence[i]
        rectifiedDuration = max(1, round(tap / TAPLENGTH))
        if rectifiedDuration > 1:
            symbol = 'DAH'
        else:
            symbol = 'DIT'
        rectifiedSequence.append(symbol)

    return rectifiedSequence

windowSurface.fill(BACKGROUNDCOLOR)

sequence = handleEvents()

while True:
    windowSurface.fill(BACKGROUNDCOLOR)
    rawSequence = next(sequence)
    drawPower(windowSurface, rawSequence)
    calculateSymbols(rawSequence)
    pygame.display.update()
    mainClock.tick(FPS)
