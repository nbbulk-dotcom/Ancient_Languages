#!/usr/bin/env python3
"""
Khitan Large Script Frequency Analysis System
Building on Linear A success methodology
By Nicolas of the Family Brett with Manus AI pattern recognition
"""

import math
import json
from typing import Dict, List, Tuple, Optional

class KhitanFrequencyAnalyzer:
    def __init__(self):
        """Initialize the Khitan frequency analysis system"""
        self.base_frequency = 440.0  # A440 standard
        
        # Chinese pentatonic scale ratios
        self.chinese_pentatonic = {
            'gong': 1/1,      # Palace - Administrative/Imperial
            'shang': 9/8,     # Commerce - Trade/Economic
            'jue': 81/64,     # Horn - Military/Ceremonial  
            'zhi': 3/2,       # Feather - Ritual/Religious
            'yu': 27/16       # Wing - Natural/Seasonal
        }
        
        # Mongolian throat singing base frequencies
        self.mongolian_bases = {
            'khoomei': 123.47,    # B2 - Basic vocabulary
            'sygyt': 130.81,      # C3 - Titles/Ranks
            'kargyraa': 98.00,    # G1 - Numbers/Quantities
            'borbangnadyr': 110.00 # A2 - Temporal concepts
        }
        
        # Known Khitan vocabulary with frequency assignments
        self.khitan_vocabulary = {
            # Numbers (critical for pattern recognition)
            '*omc': {'meaning': 'one', 'frequency': 440.00, 'type': 'number', 'harmonic': '1/1'},
            'j.ur.er': {'meaning': 'second', 'frequency': 495.00, 'type': 'number', 'harmonic': '9/8'},
            'hu.ur.er': {'meaning': 'third', 'frequency': 556.88, 'type': 'number', 'harmonic': '81/64'},
            'durer': {'meaning': 'fourth', 'frequency': 586.67, 'type': 'number', 'harmonic': '4/3'},
            'tau': {'meaning': 'five', 'frequency': 660.00, 'type': 'number', 'harmonic': '3/2'},
            '*nil': {'meaning': 'six', 'frequency': 733.33, 'type': 'number', 'harmonic': '5/3'},
            'da.lo.er': {'meaning': 'seventh', 'frequency': 770.00, 'type': 'number', 'harmonic': '7/4'},
            'n.ie.em': {'meaning': 'eight', 'frequency': 880.00, 'type': 'number', 'harmonic': '2/1'},
            '*is': {'meaning': 'nine', 'frequency': 990.00, 'type': 'number', 'harmonic': '9/4'},
            'par': {'meaning': 'ten', 'frequency': 1100.00, 'type': 'number', 'harmonic': '5/2'},
            
            # Seasons (cyclical frequencies)
            'heu.ur': {'meaning': 'spring', 'frequency': 261.63, 'type': 'season', 'harmonic': 'C4'},
            'ju.un': {'meaning': 'summer', 'frequency': 329.63, 'type': 'season', 'harmonic': 'E4'},
            'n.am.ur': {'meaning': 'autumn', 'frequency': 392.00, 'type': 'season', 'harmonic': 'G4'},
            'u.ul': {'meaning': 'winter', 'frequency': 220.00, 'type': 'season', 'harmonic': 'A3'},
            
            # Time concepts
            'tao': {'meaning': 'five', 'frequency': 660.00, 'type': 'temporal', 'harmonic': '3/2'},
            'saiyier': {'meaning': 'moon/month', 'frequency': 329.63, 'type': 'temporal', 'harmonic': 'E4'}
        }
        
        # Character type frequency ranges
        self.character_types = {
            'imperial': {'min': 660, 'max': 880, 'description': 'Imperial/Sacred characters'},
            'administrative': {'min': 440, 'max': 660, 'description': 'Administrative terms'},
            'common': {'min': 330, 'max': 495, 'description': 'Common vocabulary'},
            'temporal': {'min': 220, 'max': 330, 'description': 'Time/Date indicators'}
        }

    def calculate_harmonic_frequency(self, base: float, ratio_str: str) -> float:
        """Calculate frequency from harmonic ratio"""
        if '/' in ratio_str:
            num, den = map(int, ratio_str.split('/'))
            return base * (num / den)
        else:
            return base

    def analyze_character_frequency(self, character: str) -> Dict:
        """Analyze a Khitan character and return frequency information"""
        if character in self.khitan_vocabulary:
            vocab_entry = self.khitan_vocabulary[character]
            return {
                'character': character,
                'frequency': vocab_entry['frequency'],
                'meaning': vocab_entry['meaning'],
                'type': vocab_entry['type'],
                'harmonic': vocab_entry['harmonic'],
                'note': self.frequency_to_note(vocab_entry['frequency']),
                'character_type': self.classify_character_type(vocab_entry['frequency'])
            }
        else:
            # Estimate frequency based on character complexity and context
            estimated_freq = self.estimate_character_frequency(character)
            return {
                'character': character,
                'frequency': estimated_freq,
                'meaning': 'unknown',
                'type': 'estimated',
                'harmonic': 'estimated',
                'note': self.frequency_to_note(estimated_freq),
                'character_type': self.classify_character_type(estimated_freq)
            }

    def estimate_character_frequency(self, character: str) -> float:
        """Estimate frequency for unknown characters based on complexity"""
        # Simple heuristic based on character length and complexity
        complexity = len(character.replace('.', ''))
        
        if complexity <= 2:
            return 220 + (complexity * 55)  # Temporal range
        elif complexity <= 4:
            return 330 + (complexity * 41.25)  # Common range  
        elif complexity <= 6:
            return 440 + (complexity * 36.67)  # Administrative range
        else:
            return 660 + (complexity * 31.43)  # Imperial range

    def classify_character_type(self, frequency: float) -> str:
        """Classify character type based on frequency"""
        for char_type, range_info in self.character_types.items():
            if range_info['min'] <= frequency <= range_info['max']:
                return char_type
        return 'unknown'

    def frequency_to_note(self, frequency: float) -> str:
        """Convert frequency to musical note"""
        A4 = 440.0
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Calculate semitones from A4
        semitones = 12 * math.log2(frequency / A4)
        octave = 4 + int(semitones // 12)
        note_index = int(semitones % 12)
        
        # Adjust for negative semitones
        if semitones < 0:
            octave -= 1
            note_index = (note_index + 12) % 12
            
        return f"{notes[note_index]}{octave}"

    def analyze_inscription(self, inscription_text: str) -> Dict:
        """Analyze a complete Khitan inscription"""
        characters = inscription_text.split()
        analysis = []
        total_frequency = 0
        
        for char in characters:
            char_analysis = self.analyze_character_frequency(char)
            analysis.append(char_analysis)
            total_frequency += char_analysis['frequency']
        
        # Calculate accumulated frequency (like Linear A methodology)
        accumulated_frequency = total_frequency / len(characters) if characters else 0
        
        # Determine overall harmonic center
        harmonic_center = self.frequency_to_note(accumulated_frequency)
        
        # Identify frequency patterns
        frequencies = [char['frequency'] for char in analysis]
        frequency_pattern = self.identify_frequency_pattern(frequencies)
        
        return {
            'inscription': inscription_text,
            'character_count': len(characters),
            'character_analysis': analysis,
            'accumulated_frequency': accumulated_frequency,
            'harmonic_center': harmonic_center,
            'frequency_pattern': frequency_pattern,
            'interpretation': self.interpret_frequency_pattern(frequency_pattern, accumulated_frequency)
        }

    def identify_frequency_pattern(self, frequencies: List[float]) -> str:
        """Identify the frequency pattern in a sequence"""
        if not frequencies:
            return "empty"
        
        # Check for ascending pattern
        if all(frequencies[i] <= frequencies[i+1] for i in range(len(frequencies)-1)):
            return "ascending"
        
        # Check for descending pattern  
        if all(frequencies[i] >= frequencies[i+1] for i in range(len(frequencies)-1)):
            return "descending"
        
        # Check for cyclical pattern (ABAB or ABCABC)
        if len(frequencies) >= 4:
            if frequencies[0] == frequencies[2] and frequencies[1] == frequencies[3]:
                return "cyclical_2"
        
        # Check for harmonic series pattern
        base_freq = min(frequencies)
        harmonic_ratios = [freq / base_freq for freq in frequencies]
        if all(abs(ratio - round(ratio)) < 0.1 for ratio in harmonic_ratios):
            return "harmonic_series"
        
        return "complex"

    def interpret_frequency_pattern(self, pattern: str, accumulated_freq: float) -> str:
        """Interpret the meaning of a frequency pattern"""
        interpretations = {
            "ascending": "Invocation or building energy - possibly ceremonial opening",
            "descending": "Completion or grounding - possibly ceremonial closing", 
            "cyclical_2": "Rhythmic or repetitive - possibly chant or formula",
            "harmonic_series": "Musical or tonal - possibly sacred song or healing frequency",
            "complex": "Narrative or administrative - possibly historical record"
        }
        
        base_interpretation = interpretations.get(pattern, "Unknown pattern")
        
        # Add frequency-based context
        if accumulated_freq > 660:
            context = " (Imperial/Sacred context)"
        elif accumulated_freq > 440:
            context = " (Administrative context)"
        elif accumulated_freq > 330:
            context = " (Common/Daily context)"
        else:
            context = " (Temporal/Structural context)"
            
        return base_interpretation + context

    def generate_audio_sequence(self, frequencies: List[float], duration: float = 0.5) -> List[Dict]:
        """Generate audio sequence data for playback"""
        audio_sequence = []
        for i, freq in enumerate(frequencies):
            audio_sequence.append({
                'frequency': freq,
                'start_time': i * duration,
                'duration': duration,
                'note': self.frequency_to_note(freq)
            })
        return audio_sequence

# Example usage and testing
if __name__ == "__main__":
    analyzer = KhitanFrequencyAnalyzer()
    
    # Test with known Khitan vocabulary
    print("=== KHITAN FREQUENCY ANALYSIS SYSTEM ===")
    print("By Nicolas of the Family Brett with Manus AI")
    print()
    
    # Analyze individual characters
    print("Individual Character Analysis:")
    test_chars = ['tau', 'j.ur.er', 'heu.ur', 'saiyier']
    for char in test_chars:
        result = analyzer.analyze_character_frequency(char)
        print(f"{char}: {result['frequency']:.2f} Hz ({result['note']}) - {result['meaning']} [{result['character_type']}]")
    
    print()
    
    # Analyze a hypothetical inscription (using known vocabulary)
    print("Inscription Analysis:")
    test_inscription = "tau saiyier heu.ur"  # "Fifth month spring" 
    inscription_analysis = analyzer.analyze_inscription(test_inscription)
    
    print(f"Inscription: '{inscription_analysis['inscription']}'")
    print(f"Accumulated Frequency: {inscription_analysis['accumulated_frequency']:.2f} Hz")
    print(f"Harmonic Center: {inscription_analysis['harmonic_center']}")
    print(f"Pattern: {inscription_analysis['frequency_pattern']}")
    print(f"Interpretation: {inscription_analysis['interpretation']}")
    
    print()
    print("Character Breakdown:")
    for char_analysis in inscription_analysis['character_analysis']:
        print(f"  {char_analysis['character']}: {char_analysis['frequency']:.2f} Hz - {char_analysis['meaning']}")
    
    # Generate audio sequence
    frequencies = [char['frequency'] for char in inscription_analysis['character_analysis']]
    audio_sequence = analyzer.generate_audio_sequence(frequencies)
    
    print()
    print("Audio Sequence for Playback:")
    for audio in audio_sequence:
        print(f"  {audio['start_time']:.1f}s: {audio['frequency']:.2f} Hz ({audio['note']})")
    
    print()
    print("=== READY FOR MAJOR INSCRIPTION ANALYSIS ===")
