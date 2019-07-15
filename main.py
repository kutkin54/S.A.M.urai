#TODO: allow a text file to be dropped onto the game; use that text

import pygame, random, sys
from pygame.locals import *
from code_patterns import *
from itertools import cycle

TAPLENGTH = 90

class Game:
    WINDOWWIDTH = 1200
    WINDOWHEIGHT = 80
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (10, 255, 10)
    RED = (255, 10, 10)
    BACKGROUNDCOLOR = WHITE
    TEXTCOLOR = BLACK

    FPS = 60

    ADDNEWBADDIERATE = 150
    BADDIESPEED = -1
    BADDIESIZE = 40

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('S.A.M.urai')
        pygame.mouse.set_visible(False)

        self.playerImage = [pygame.image.load('resources/adventurer-run3-0{}.png'.format(i)) for i in range(6)]
        self.playerRect = self.playerImage[0].get_rect()
        self.playerRect.bottom = self.WINDOWHEIGHT - 2

        self.baddieAddCounter = 0
        self.baddies = []
        self.font = pygame.font.SysFont(None, 72)

        #self.codePatterns = MorseCodePatterns()
        self.codePatterns = TapCodePatterns()

        self.score = 0

    def playerHasHitBaddie(self, player, baddies):
        return any(player.colliderect(b.get('rect')) for b in baddies)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def spawnBaddie(self, baddies):
        newBaddie = {
                'rect': pygame.Rect(
                    self.WINDOWWIDTH,
                    (self.WINDOWHEIGHT - self.BADDIESIZE) - 2,
                    self.BADDIESIZE,
                    self.BADDIESIZE
                ),
                'character': random.choice(list(self.codePatterns.getAlphabet()))
        }
        newBaddie['surface'] = self.font.render(newBaddie['character'], 1, self.TEXTCOLOR)

        self.baddies.append(newBaddie)

    def killBaddie(self, baddy):
        self.baddies.remove(baddy)

    def drawText(self, text, surface, x, y):
        font = pygame.font.SysFont(None, 24)
        textobj = font.render(text, 1, self.TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def fireWeapon(self, attackSequence):
        if len(attackSequence) > 1:
            rectifiedSequence = self.rectifySequence(attackSequence)
            attackedCharacterList = self.codePatterns.getCharacter(rectifiedSequence)
            if len(self.baddies) > 0:
                if self.baddies[0]['character'] in attackedCharacterList:
                    self.killBaddie(self.baddies[0])
                    self.score += len(rectifiedSequence)
                else:
                    self.score -= len(rectifiedSequence)

    def drawPlayer(self, windowSurface):
        playerIndex = 0
        numImages = len(self.playerImage)
        framesPerImage = 4
        while True:
            windowSurface.blit(self.playerImage[(playerIndex // framesPerImage) % numImages], self.playerRect)
            playerIndex = (playerIndex + 1) % (framesPerImage * numImages)
            yield

    def drawBaddies(self, windowSurface):
        for b in self.baddies:
            windowSurface.blit(b['surface'], b['rect'])

    def drawAttackSequence(self, windowSurface, attackSequence):
        #font = pygame.font.SysFont(None, 36)
        #x = 1
        #y = 1
        #self.drawText(' '.join(attackSequence), font, windowSurface, x, y)
        #self.drawConcentricCircles(windowSurface, attackSequence)
        #self.drawStackedBar(windowSurface, attackSequence)
        self.drawDashes(windowSurface, attackSequence)

    def drawPower(self, windowSurface, sequence):
        drawConcentricCircles(windowSurface, sequence)
        drawStackedBar(windowSurface, sequence)
        drawDashes(windowSurface, sequence)

    def drawStackedBar(self, windowSurface, sequence):
        width = 5
        radius = 10
        windowHeight = windowSurface.get_height()
        y = windowHeight
        surface = pygame.Surface((width, windowHeight))
        surface.fill(self.BACKGROUNDCOLOR)

        colorCycle = cycle([self.GREEN, self.RED])
        for i in range(0, len(sequence), 2):
            if len(sequence) > i + 1:
                color = next(colorCycle)
                keyed = sequence[i+1] // TAPLENGTH + 1
                height = radius * keyed
                pygame.draw.rect(surface, color, (0, y - height, width, height))
                y -= height + 1

        windowSurface.blit(surface, (0, 0))

    def drawConcentricCircles(self, windowSurface, sequence):
        radiusInc = 3
        circles = []
        windowWidth = windowSurface.get_width()
        windowHeight = windowSurface.get_height()
        surface = pygame.Surface((windowWidth, windowHeight))
        surface.fill(self.BACKGROUNDCOLOR)

        radius = 0
        for i in range(0, len(sequence), 2):
            if len(sequence) > i + 1:
                keyed = sequence[i+1] // TAPLENGTH + 1
                width = radiusInc * keyed
                circles.append(radius + width)
                radius += width

        colorCycle = cycle([self.GREEN, self.RED])
        if len(circles) % 2 == 0:
            circles.append(0)
        for c in circles[::-1]:
            color = next(colorCycle)
            pygame.draw.circle(surface, color, (windowWidth // 2, windowHeight // 2), c)

        windowSurface.blit(surface, (0, 0))


    def drawDashes(self, windowSurface, sequence):
        # These are fixed, should be moved out of the function
        y = radius = xStart = xEnd = 5
        surface = pygame.Surface((windowSurface.get_width(), 2*radius))
        surface.fill(self.BACKGROUNDCOLOR)

        for i in range(0, len(sequence), 2):
            gap = sequence[i] // TAPLENGTH
            xStart = xEnd + radius * 2 + radius * gap

            if len(sequence) > i + 1:
                keyed = sequence[i+1] // TAPLENGTH
                width = radius * keyed
                xEnd = xStart + width

                # Start dot
                pygame.draw.circle(surface, self.GREEN, (xStart, y), radius)

                # Middle rect
                pygame.draw.rect(surface, self.GREEN, (xStart, y - radius, width, radius * 2))

                # End dot
                pygame.draw.circle(surface, self.GREEN, (xEnd, y), radius)

        windowSurface.blit(surface, (0, 20))

    def handleEvents(self):
        keying = False
        timingSequence = [0]
        gapStartTime = keyStartTime = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if self.isTerminateEvent(event):
                    self.terminate()

                if self.isFireEvent(event) and not keying:
                    keyStartTime = now
                    timingSequence.append(0)
                    keying = True

                if self.isCeaseFireEvent(event) and keying:
                    gapStartTime = now
                    timingSequence.append(0)
                    keying = False

            if keying:
                timingSequence[-1] = now - keyStartTime
            else:
                timingSequence[-1] = now - gapStartTime
                if timingSequence[-1] > self.codePatterns.getSymbolDefinition('LETTERSPACE').get('minDuration') * TAPLENGTH:
                    self.fireWeapon(timingSequence)
                    timingSequence = [0]

            yield timingSequence

                    #if event.key == K_m:
                    #    if musicPlaying:
                    #        pygame.mixer.music.stop()
                    #    else:
                    #        pygame.mixer.music.play(-1, 0.0)
                    #    musicPlaying = not musicPlaying
        #        if event.type == MOUSEBUTTONUP:
        #            foods.append(pygame.Rect(event.pos[0] - FOODSIZE // 2, event.pos[1] - FOODSIZE // 2, FOODSIZE, FOODSIZE))

    def isTerminateEvent(self, event):
        return event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)

    def isFireEvent(self, event):
        return event.type in (MOUSEBUTTONDOWN, FINGERDOWN) or (event.type == KEYDOWN and event.key == K_SPACE)

    def isCeaseFireEvent(self, event):
        return event.type in (MOUSEBUTTONUP, FINGERUP) or (event.type == KEYUP and event.key == K_SPACE)
            

    def drawScore(self, windowSurface, score, topScore):
        self.drawText('Score: %s' % (score), windowSurface, 10, 0)
        #self.drawText('Top Score: %s' % (topScore), windowSurface, 10, 20)
        pass

    def rectifySequence(self, sequence):
        rectifiedSequence = []
        step = 1 if self.codePatterns.keepInternalSpaces else 2
        for i in range(1, len(sequence) - 1, step):
            tap = sequence[i]
            symbol = self.codePatterns.getSymbol(i % 2 == 1, tap)
            if symbol != None:
                rectifiedSequence.append(symbol)
            #print(rectifiedSequence)

        return rectifiedSequence

    def playGame(self):
        windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        mainClock = pygame.time.Clock()
        drawPlayerGen = self.drawPlayer(windowSurface)
        eventHandler = self.handleEvents()
        topScore = 0
        self.attackSequence = []

        while True:
            if len(self.baddies) == 0:
                self.spawnBaddie(self.baddies)
                self.BADDIESPEED -= 0.1

            rawSequence = next(eventHandler)

            for b in self.baddies:
                b['rect'].move_ip(self.BADDIESPEED, 0)

            for b in self.baddies[:]:
                if b['rect'].left < 0:
                    self.killBaddie(b)

            windowSurface.fill(self.BACKGROUNDCOLOR)
            self.drawAttackSequence(windowSurface, rawSequence)
            next(drawPlayerGen)
            self.drawBaddies(windowSurface)

            self.drawScore(windowSurface, self.score, topScore)

            pygame.display.update()

            if self.playerHasHitBaddie(self.playerRect, self.baddies):
                topScore = max(topScore, self.score)
                break

            mainClock.tick(self.FPS)

        self.drawText('You died.', windowSurface, 600, 30)
        pygame.display.update()

        while True:
            next(eventHandler)

if __name__ == "__main__":
    g = Game()
    g.playGame()
