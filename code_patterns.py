import sys 

class CodePatterns:
    def __init__(self):
        self.timingMultiplier = 100
        self.fuzzFactor = 1.5
        self.symbols = {
                'SYMBOLSPACE': { 'transmitting': False, 'duration': 1 },
                'LETTERSPACE': { 'transmitting': False, 'duration': 3 },
                'WORDSPACE': { 'transmitting': False, 'duration': 5 }
        }

        self.alphabet = dict()

    def getAlphabet(self):
        return list(self.alphabet.keys())

    def getSymbol(self, transmitting, duration):
        idealDuration = round(duration / self.timingMultiplier)
        symbolPattern = {'transmitting': transmitting, 'duration': idealDuration}
        keys = [key for (key, value) in self.symbols.items() if value == symbolPattern]
        return keys

    def getSymbolDefinition(self, key):
        return self.symbols.get(key)

    def getCharacter(self, pattern):
        keys = [key for (key, value) in self.alphabet.items() if value == pattern]
        return keys

class TapCodePatterns(CodePatterns):
    def __init__(self):
        CodePatterns.__init__(self)
        symbols = {
                'TAP': { 'transmitting': True, 'duration': 1 },
                'PAUSE': { 'transmitting': False, 'duration': 1 } # how to specify these don't take a symbolpace? shorten by 2*symbolspace?
        }
        self.symbols.update(symbols)

        TAP = self.getSymbolDefinition('TAP')
        PAUSE = self.getSymbolDefinition('PAUSE')

        self.alphabet = {
            'A': [TAP, PAUSE, TAP],
            'B': [TAP, PAUSE, TAP, TAP],
            'C': [TAP, PAUSE, TAP, TAP, TAP],
            'K': [TAP, PAUSE, TAP, TAP, TAP],
            'D': [TAP, PAUSE, TAP, TAP, TAP, TAP],
            'E': [TAP, PAUSE, TAP, TAP, TAP, TAP, TAP],

            'F': [TAP, TAP, PAUSE, TAP],
            'G': [TAP, TAP, PAUSE, TAP, TAP],
            'H': [TAP, TAP, PAUSE, TAP, TAP, TAP],
            'I': [TAP, TAP, PAUSE, TAP, TAP, TAP, TAP],
            'J': [TAP, TAP, PAUSE, TAP, TAP, TAP, TAP, TAP],

            'L': [TAP, TAP, TAP, PAUSE, TAP],
            'M': [TAP, TAP, TAP, PAUSE, TAP, TAP],
            'N': [TAP, TAP, TAP, PAUSE, TAP, TAP, TAP],
            'O': [TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP],
            'P': [TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP, TAP],

            'Q': [TAP, TAP, TAP, TAP, PAUSE, TAP],
            'R': [TAP, TAP, TAP, TAP, PAUSE, TAP, TAP],
            'S': [TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP],
            'T': [TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP],
            'U': [TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP, TAP],

            'V': [TAP, TAP, TAP, TAP, TAP, PAUSE, TAP],
            'W': [TAP, TAP, TAP, TAP, TAP, PAUSE, TAP, TAP],
            'X': [TAP, TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP],
            'Y': [TAP, TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP],
            'Z': [TAP, TAP, TAP, TAP, TAP, PAUSE, TAP, TAP, TAP, TAP, TAP],
        }

class MorseCodePatterns(CodePatterns):
    def __init__(self):
        CodePatterns.__init__(self)
        symbols = {
                'DIT': { 'transmitting': True, 'duration': 1 },
                'DAH': { 'transmitting': True, 'duration': 3 }
        }
        self.symbols.update(symbols)

        DIT = self.getSymbolDefinition('DIT')
        DAH = self.getSymbolDefinition('DAH')

        self.alphabet = {
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
