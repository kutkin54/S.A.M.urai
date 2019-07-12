import pytest
from morse import *

def test_morse_dit_precise():
    m = MorseCodePatterns()
    transmitting = True
    duration = 100
    assert m.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dah_precise():
    m = MorseCodePatterns()
    transmitting = True
    duration = 300
    assert m.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dit_short():
    m = MorseCodePatterns()
    transmitting = True
    duration = 51 
    assert m.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dit_long():
    m = MorseCodePatterns()
    transmitting = True
    duration = 149
    assert m.getSymbol(transmitting, duration)[0] == 'DIT'

def test_morse_dah_short():
    m = MorseCodePatterns()
    transmitting = True
    duration = 251 
    assert m.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dah_long():
    m = MorseCodePatterns()
    transmitting = True
    duration = 349
    assert m.getSymbol(transmitting, duration)[0] == 'DAH'

def test_morse_dit_too_short():
    m = MorseCodePatterns()
    transmitting = True
    duration = 49 
    assert len(m.getSymbol(transmitting, duration)) == 0

def test_morse_dit_too_long():
    m = MorseCodePatterns()
    transmitting = True
    duration = 151 
    assert len(m.getSymbol(transmitting, duration)) == 0

def test_morse_dah_too_short():
    m = MorseCodePatterns()
    transmitting = True
    duration = 249 
    assert len(m.getSymbol(transmitting, duration)) == 0
