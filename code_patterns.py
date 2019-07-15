import sys 

class CodePatterns:
    def __init__(self):
        self.keepInternalSpaces = False
        self.timingMultiplier = 90
        self.symbols = {
                #'SYMBOLSPACE': { 'transmitting': False, 'duration': 1 },
                'LETTERSPACE': { 'transmitting': False, 'minDuration': 4 , 'maxDuration': 4},
                'WORDSPACE': { 'transmitting': False, 'minDuration': 5, 'maxDuration': 6 }
        }

        self.alphabet = dict()

    def getAlphabet(self):
        return list(self.alphabet.keys())

    def getSymbol(self, transmitting, duration):
        idealDuration = max(1, round(duration / self.timingMultiplier))
        symbolPattern = {'transmitting': transmitting, 'duration': idealDuration}
        #print('{} idealized to {} which is {}'.format(duration, idealDuration, symbolPattern))
        for (key, value) in self.symbols.items():
            if value.get('transmitting') == symbolPattern.get('transmitting') and value.get('minDuration') <= idealDuration <= value.get('maxDuration'):
                return key
        return None

    def getSymbolDefinition(self, key):
        return self.symbols.get(key)

    def getCharacter(self, pattern):
        keys = [key for (key, value) in self.alphabet.items() if value == pattern]
        return keys

class TapCodePatterns(CodePatterns):
    def __init__(self):
        CodePatterns.__init__(self)
        self.keepInternalSpaces = True
        symbols = {
                'TAP': { 'transmitting': True, 'minDuration': 1, 'maxDuration': 1 },
                'PAUSE': { 'transmitting': False, 'minDuration': 2, 'maxDuration': 4 },
                'LETTERSPACE': { 'transmitting': False, 'minDuration': 5, 'maxDuration': 6 },
        }
        self.symbols.update(symbols)

        self.alphabet = {
            'A': ['TAP', 'PAUSE', 'TAP'],
            'B': ['TAP', 'PAUSE', 'TAP', 'TAP'],
            'C': ['TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'K': ['TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'D': ['TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP'],
            'E': ['TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP', 'TAP'],

            'F': ['TAP', 'TAP', 'PAUSE', 'TAP'],
            'G': ['TAP', 'TAP', 'PAUSE', 'TAP', 'TAP'],
            'H': ['TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'I': ['TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP'],
            'J': ['TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP', 'TAP'],

            'L': ['TAP', 'TAP', 'TAP', 'PAUSE', 'TAP'],
            'M': ['TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP'],
            'N': ['TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'O': ['TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP'],
            'P': ['TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP', 'TAP'],

            'Q': ['TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP'],
            'R': ['TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP'],
            'S': ['TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'T': ['TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP'],
            'U': ['TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP', 'TAP'],

            'V': ['TAP', 'TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP'],
            'W': ['TAP', 'TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP'],
            'X': ['TAP', 'TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP'],
            'Y': ['TAP', 'TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP'],
            'Z': ['TAP', 'TAP', 'TAP', 'TAP', 'TAP', 'PAUSE', 'TAP', 'TAP', 'TAP', 'TAP', 'TAP'],
        }

class MorseCodePatterns(CodePatterns):
    def __init__(self):
        CodePatterns.__init__(self)
        symbols = {
                'DIT': { 'transmitting': True, 'minDuration': 0, 'maxDuration': 1 },
                'DAH': { 'transmitting': True, 'minDuration': 2, 'maxDuration': 5 },
        }
        self.symbols.update(symbols)

        self.alphabet = {
            'A': ['DIT', 'DAH'],
            'B': ['DAH', 'DIT', 'DIT', 'DIT'],
            'C': ['DAH', 'DIT', 'DAH', 'DIT'],
            'D': ['DAH', 'DIT', 'DIT'],
            'E': ['DIT'],
            'F': ['DIT', 'DIT', 'DAH', 'DIT'],
            'G': ['DAH', 'DAH', 'DIT'],
            'H': ['DIT', 'DIT', 'DIT', 'DIT'],
            'I': ['DIT', 'DIT'],
            'J': ['DIT', 'DAH', 'DAH', 'DAH'],
            'K': ['DAH', 'DIT', 'DAH'],
            'L': ['DIT', 'DAH', 'DIT', 'DIT'],
            'M': ['DAH', 'DAH'],
            'N': ['DAH', 'DIT'],
            'O': ['DAH', 'DAH', 'DAH'],
            'P': ['DIT', 'DAH', 'DAH', 'DIT'],
            'Q': ['DAH', 'DAH', 'DIT', 'DAH'],
            'R': ['DIT', 'DAH', 'DIT'],
            'S': ['DIT', 'DIT', 'DIT'],
            'T': ['DAH'],
            'U': ['DIT', 'DIT', 'DAH'],
            'V': ['DIT', 'DIT', 'DIT', 'DAH'],
            'W': ['DIT', 'DAH', 'DAH'],
            'X': ['DAH', 'DIT', 'DIT', 'DAH'],
            'Y': ['DAH', 'DIT', 'DAH', 'DAH'],
            'Z': ['DAH', 'DAH', 'DIT', 'DIT'],
            '1': ['DIT', 'DAH', 'DAH', 'DAH', 'DAH'],
            '2': ['DIT', 'DIT', 'DAH', 'DAH', 'DAH'],
            '3': ['DIT', 'DIT', 'DIT', 'DAH', 'DAH'],
            '4': ['DIT', 'DIT', 'DIT', 'DIT', 'DAH'],
            '5': ['DIT', 'DIT', 'DIT', 'DIT', 'DIT'],
            '6': ['DAH', 'DIT', 'DIT', 'DIT', 'DIT'],
            '7': ['DAH', 'DAH', 'DIT', 'DIT', 'DIT'],
            '8': ['DAH', 'DAH', 'DAH', 'DIT', 'DIT'],
            '9': ['DAH', 'DAH', 'DAH', 'DAH', 'DIT'],
            '0': ['DAH', 'DAH', 'DAH', 'DAH', 'DAH'],
        }
