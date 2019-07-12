import pygame, random, sys
from pygame.locals import *
from code_patterns import *

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

        self.codePatterns = MorseCodePatterns()

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
                'character': random.choice(list(self.codePatterns.getAlphabet()))
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
        attackedCharacterList = self.codePatterns.getCharacter(attackSequence)
        if len(baddies) > 0:
            if baddies[0]['character'] in attackedCharacterList:
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
            #if (now - self.gapStartTime > self.SYMBOLGAP * self.timingMultiplier * self.fuzzFactor) and not keying and len(attackSequence) > 0:
            pauseLengthIndicatingFire = self.codePatterns.getSymbolDefinition('SYMBOLSPACE')['duration'] * self.codePatterns.timingMultiplier * self.codePatterns.fuzzFactor
            if (now - self.gapStartTime > pauseLengthIndicatingFire) and not keying and len(attackSequence) > 0:
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
                        symbol = self.codePatterns.getSymbol(False, gapElapsedTime)
                        if len(symbol) > 0:
                            attackSequence.append(symbol[0])
                        else:
                            attackSequence = []

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        keying = False
                        keyEndTime = self.gapStartTime = pygame.time.get_ticks()
                        keyElapsedTime = keyEndTime - keyStartTime
                        symbol = self.codePatterns.getSymbol(True, gapElapsedTime)
                        if len(symbol) > 0:
                            attackSequence.append(symbol[0])
                        else:
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

