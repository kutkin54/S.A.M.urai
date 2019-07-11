import pygame, random, sys
from pygame.locals import *

class CodePatterns:
    pass

class TapCodePatterns(CodePatterns):
    pass


class MorsePatterns(CodePatterns):
    pass

class Game:
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

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('S.A.M.urai')
        pygame.mouse.set_visible(False)

        self.playerImage = [pygame.image.load('resources/adventurer-run3-0{}.png'.format(i)) for i in range(6)]
        self.playerRect = self.playerImage[0].get_rect()
        self.playerRect.centery = self.WINDOWHEIGHT / 2

        self.baddieAddCounter = 0
        self.baddies = []
        self.font = pygame.font.SysFont(None, 72)



    def playerHasHitBaddie(self, player, baddies):
        return False

    def terminate(self):
        pygame.quit()
        sys.exit()

    def spawnBaddie(self, baddies):
        newBaddie = {
                'rect': pygame.Rect(
                    self.WINDOWWIDTH,
                    (self.WINDOWHEIGHT - self.BADDIESIZE) / 2,
                    self.BADDIESIZE,
                    self.BADDIESIZE
                ),
                'character': random.choice(list(self.BADDIEPATTERNS.keys()))
        }
        newBaddie['surface'] = self.font.render(newBaddie['character'], 1, self.TEXTCOLOR)

        self.baddies.append(newBaddie)


    def killBaddie(self, baddies, baddy):
        self.baddies.remove(baddy)

    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def fireWeapon(self, attackSequence, baddies):
        print(attackSequence)
        if len(baddies) > 0:
            if attackSequence == self.BADDIEPATTERNS[baddies[0]['character']]:
                self.killBaddie(baddies, baddies[0])

    def drawPlayer(self, windowSurface):
        playerIndex = 0
        numImages = 6
        framesPerImage = 4
        while True:
            windowSurface.blit(self.playerImage[(playerIndex // framesPerImage) % numImages], self.playerRect)
            playerIndex = (playerIndex + 1) % (framesPerImage * numImages)
            yield

    def drawBaddies(self, windowSurface):
            for b in self.baddies:
                windowSurface.blit(b['surface'], b['rect'])

    def handleEvents(self):
        keying = 0
        attackSequence = []
        while True:
            now = pygame.time.get_ticks()
            if (now - self.gapStartTime > self.SYMBOLGAP * self.timingMultiplier * self.fuzzFactor) and not keying and len(attackSequence) > 0:
                self.fireWeapon(attackSequence, self.baddies)
                attackSequence = []
                self.gapStartTime = now

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.terminate()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        keying = True
                        keyStartTime = gapEndTime = pygame.time.get_ticks()
                        gapElapsedTime = gapEndTime - self.gapStartTime

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        keying = False
                        keyEndTime = self.gapStartTime = pygame.time.get_ticks()
                        keyElapsedTime = keyEndTime - keyStartTime

                        if keyElapsedTime < self.DIT * self.timingMultiplier * self.fuzzFactor:
                            attackSequence.append(self.DIT)
                        elif keyElapsedTime < self.DAH * self.timingMultiplier * self.fuzzFactor:
                            attackSequence.append(self.DAH)
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
            yield

    def drawScore(self, windowSurface, score, topScore):
        #drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        #drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        pass

    def playGame(self):
        self.gapStartTime = pygame.time.get_ticks()
        windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        mainClock = pygame.time.Clock()
        drawPlayerGen = self.drawPlayer(windowSurface)
        eventHandler = self.handleEvents()
        score = topScore = 0

        while True:
            if len(self.baddies) == 0:
                self.spawnBaddie(self.baddies)
                self.BADDIESPEED -= 0.1

            next(eventHandler)

            for b in self.baddies:
                b['rect'].move_ip(self.BADDIESPEED, 0)

            for b in self.baddies[:]:
                if b['rect'].left < 0:
                    self.killBaddie(self.baddies, b)

            windowSurface.fill(self.BACKGROUNDCOLOR)

            next(drawPlayerGen)
            self.drawBaddies(windowSurface)

            self.drawScore(windowSurface, score, topScore)

            pygame.display.update()

            if self.playerHasHitBaddie(self.playerRect, self.baddies):
                topScore = max(topScore, score)
                break

            mainClock.tick(self.FPS)

if __name__ == "__main__":
    g = Game()
    g.playGame()

