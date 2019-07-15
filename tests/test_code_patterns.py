import pytest
from code_patterns import *
import string

morsePattern = MorseCodePatterns()
tapPattern = TapCodePatterns()

def test_morse_dit_precise():
    transmitting = True
    duration = 100
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dah_precise():
    transmitting = True
    duration = 300
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dit_short():
    transmitting = True
    duration = 51 
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dit_long():
    transmitting = True
    duration = 149
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dah_short():
    transmitting = True
    duration = 251 
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dah_long():
    transmitting = True
    duration = 349
    assert morsePattern.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dit_too_short():
    transmitting = True
    duration = 49 
    assert len(morsePattern.getSymbol(transmitting, duration)) == 0

def test_morse_dit_too_long():
    transmitting = True
    duration = 151 
    assert len(morsePattern.getSymbol(transmitting, duration)) == 0

def test_morse_dah_too_short():
    transmitting = True
    duration = 249 
    assert len(morsePattern.getSymbol(transmitting, duration)) == 0

def test_morse_get_a():
    seq = ['DIT', 'DAH']
    assert 'A' in morsePattern.getCharacter(seq)

def test_tap_get_a():
    seq = ['TAP', 'PAUSE', 'TAP']
    assert 'A' in tapPattern.getCharacter(seq)

def test_get_alphabet():
    alphabet = string.ascii_uppercase + string.digits
    assert set(morsePattern.getAlphabet()) == set(alphabet)

def test_get_symbol_DIT_definition():
    dit = {'transmitting': True, 'duration': 1}
    assert morsePattern.getSymbolDefinition('DIT') == dit

def test_get_symbol_DAH_definition():
    dah = {'transmitting': True, 'duration': 3}
    assert morsePattern.getSymbolDefinition('DAH') == dah


