#!/usr/bin/env python3
"""
Linear A Frequency Calculator
Calculates accumulated sound frequencies for Linear A signs and words
"""

import math
from fractions import Fraction

class LinearAFrequencyCalculator:
    def __init__(self):
        # Base frequencies for vowel signs (in Hz, using A4=440 as reference)
        self.vowel_frequencies = {
            '*01': 440.0,  # A - root frequency
            '*08': 550.0,  # E - major third above A
            '*28': 660.0,  # I - perfect fifth above A  
            '*61': 587.33, # O - perfect fourth above A
            '*10': 880.0   # U - octave above A
        }
        
        # Consonant frequency modifiers (as ratios)
        self.consonant_modifiers = {
            # Guttural sounds (lower frequency)
            '*77': Fraction(1, 2),  # KA
            '*67': Fraction(1, 3),  # QA  
            '*39': Fraction(1, 4),  # GA
            
            # Sibilant sounds (higher frequency)
            '*31': Fraction(3, 2),  # SA
            '*41': Fraction(4, 3),  # SE
            '*51': Fraction(5, 4),  # SI
            
            # Liquid consonants
            '*53': Fraction(2, 3),  # RA
            '*27': Fraction(3, 4),  # LA
            
            # Nasal consonants  
            '*80': Fraction(5, 6),  # MA
            '*30': Fraction(6, 7),  # NA
        }
        
        # Linear A fractional ratios
        self.fractional_ratios = {
            'J': Fraction(1, 2),    # Octave
            'E': Fraction(1, 4),    # Double octave
            'B': Fraction(1, 5),    # Major third approximation
            'D': Fraction(1, 6),    # Minor third approximation
            'F': Fraction(1, 8),    # Triple octave
            'K': Fraction(1, 10),   # Compound interval
            'H': Fraction(1, 16),   # Quadruple octave
            'W': Fraction(2, 3),    # Perfect fifth
            'X': Fraction(1, 12),   # Semitone
            'L2': Fraction(1, 20),  # Complex ratio
            'A': Fraction(1, 24),   # Chromatic division
            'L6': Fraction(1, 60),  # Minute division
        }
    
    def calculate_word_frequency(self, vowel_sign, consonant_signs=None, fraction_sign=None):
        """
        Calculate the accumulated frequency for a Linear A word
        
        Args:
            vowel_sign: Base vowel sign (e.g., '*01')
            consonant_signs: List of consonant signs (e.g., ['*77', '*31'])
            fraction_sign: Fractional modifier (e.g., 'J')
            
        Returns:
            Final frequency in Hz
        """
        if vowel_sign not in self.vowel_frequencies:
            raise ValueError(f"Unknown vowel sign: {vowel_sign}")
            
        # Start with base vowel frequency
        base_freq = self.vowel_frequencies[vowel_sign]
        
        # Apply consonant modifiers
        consonant_modifier = Fraction(1, 1)  # Start with 1
        if consonant_signs:
            for consonant in consonant_signs:
                if consonant in self.consonant_modifiers:
                    consonant_modifier *= self.consonant_modifiers[consonant]
        
        # Apply fractional ratio
        fractional_modifier = Fraction(1, 1)  # Start with 1
        if fraction_sign and fraction_sign in self.fractional_ratios:
            fractional_modifier = self.fractional_ratios[fraction_sign]
        
        # Calculate final frequency
        final_freq = base_freq * float(consonant_modifier * fractional_modifier)
        
        return final_freq
    
    def frequency_to_note(self, frequency):
        """Convert frequency to musical note name"""
        # A4 = 440 Hz is our reference
        A4 = 440.0
        
        # Calculate semitones from A4
        semitones_from_A4 = 12 * math.log2(frequency / A4)
        
        # Note names
        notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
        
        # Calculate octave and note
        octave = 4 + int(semitones_from_A4 // 12)
        note_index = int(semitones_from_A4 % 12)
        
        return f"{notes[note_index]}{octave}"
    
    def analyze_linear_a_word(self, vowel_sign, consonant_signs=None, fraction_sign=None):
        """Complete analysis of a Linear A word"""
        freq = self.calculate_word_frequency(vowel_sign, consonant_signs, fraction_sign)
        note = self.frequency_to_note(freq)
        
        result = {
            'vowel_sign': vowel_sign,
            'consonant_signs': consonant_signs or [],
            'fraction_sign': fraction_sign,
            'frequency_hz': round(freq, 2),
            'musical_note': note,
            'base_frequency': self.vowel_frequencies[vowel_sign]
        }
        
        return result

# Example usage and testing
if __name__ == "__main__":
    calc = LinearAFrequencyCalculator()
    
    print("Linear A Frequency Analysis Examples:")
    print("=" * 50)
    
    # Example 1: Simple vowel
    result1 = calc.analyze_linear_a_word('*01')  # Pure A
    print(f"Pure A vowel (*01): {result1['frequency_hz']} Hz = {result1['musical_note']}")
    
    # Example 2: Vowel with guttural consonant
    result2 = calc.analyze_linear_a_word('*01', ['*77'])  # A + KA (1/2 modifier)
    print(f"A + KA (*01 + *77): {result2['frequency_hz']} Hz = {result2['musical_note']}")
    
    # Example 3: Complex word with fraction
    result3 = calc.analyze_linear_a_word('*01', ['*77', '*31'], 'J')  # A + KA + SA + octave fraction
    print(f"A + KA + SA + octave (*01 + *77 + *31 + J): {result3['frequency_hz']} Hz = {result3['musical_note']}")
    
    # Example 4: Perfect fifth relationship
    result4 = calc.analyze_linear_a_word('*01', fraction_sign='W')  # A with perfect fifth fraction
    print(f"A + perfect fifth (*01 + W): {result4['frequency_hz']} Hz = {result4['musical_note']}")
    
    print("\nLinear A Fractional Scale Analysis:")
    print("=" * 40)
    
    # Analyze all fractional relationships from base A
    base_vowel = '*01'
    for fraction_name, fraction_value in calc.fractional_ratios.items():
        result = calc.analyze_linear_a_word(base_vowel, fraction_sign=fraction_name)
        ratio_decimal = float(fraction_value)
        print(f"{fraction_name} ({fraction_value}): {result['frequency_hz']} Hz = {result['musical_note']} (×{ratio_decimal:.3f})")
