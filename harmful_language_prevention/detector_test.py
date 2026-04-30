#!/usr/bin/env python3
"""Test detector's analyze_text method directly."""

from harmful_detector import HarmfulLanguageDetector

detector = HarmfulLanguageDetector()

crisis_input = "I will kill myself tonight, no other way"
is_harmful, score, categories = detector.analyze_text(crisis_input)

print(f"Input: '{crisis_input}'")
print(f"Is harmful: {is_harmful}")
print(f"Score: {score}")
print(f"Categories: {categories}")
print(f"Category types: {[type(c).__name__ for c in categories]}")
