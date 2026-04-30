#!/usr/bin/env python3
"""
Harmful Language Detector Module
Analyzes text for harmful content using applied logic patterns.
"""

import re
from typing import Tuple, List, Dict
from dataclasses import dataclass

@dataclass
class HarmfulPattern:
    """Represents a pattern for detecting harmful language."""
    pattern: str
    category: str
    weight: float
    description: str

class HarmfulLanguageDetector:
    """Detects harmful language using applied logic and pattern matching."""
    
    def __init__(self):
        """Initialize the detector with harmful language patterns."""
        self.patterns = self._load_harmful_patterns()
        self.threshold = 0.3  # Threshold for considering content harmful
    
    def _load_harmful_patterns(self) -> List[HarmfulPattern]:
        """Load patterns for detecting harmful language."""
        patterns = [
            # Violence and threats
            HarmfulPattern(
                pattern=r'\b(kill|murder|assassinate|slaughter|massacre|execute|hang|shoot|stab|beat|attack|hurt|harm|injure|wound|torture|mutilate)\b',
                category='violence',
                weight=0.9,
                description='Language depicting or encouraging physical violence'
            ),
            
            # Hate speech and discrimination
            HarmfulPattern(
                pattern=r'\b(hate|despise|loathe|detest|abhor).*\b(race|ethnic|national|religious|gender|sex|sexual|orient|disabled|handicapped|retarded|nigger|faggot|dyke|spic|kike|gook|chink)\b',
                category='hate_speech',
                weight=0.95,
                description='Explicit hate speech targeting protected characteristics'
            ),
            
            # Harassment and bullying
            HarmfulPattern(
                pattern=r'\b(you\s+are\s+(worthless|pathetic|disgusting|ugly|fat|stupid|idiot|moron|loser|failure|trash|garbage|waste|scum|filth|vermin|animal|beast|devil|demon|satan|hell|damned|cursed))\b',
                category='harassment',
                weight=0.8,
                description='Personal attacks and harassment'
            ),
            
            # Self-harm and suicide
            HarmfulPattern(
                pattern=r'\b(suicide|suicidal|kill\s+myself|end\s+it\s+all|want\s+to\s+die|better\s+off\s+dead|cut\s+myself|self\s+harm|hurt\s+myself)\b',
                category='self_harm',
                weight=0.9,
                description='Language indicating self-harm or suicidal ideation'
            ),
            
            # Illegal activities
            HarmfulPattern(
                pattern=r'\b(rob|steal|theft|burglary|fraud|scam|embezzle|launder|smuggle|traffic|deal\s+drugs|manufacture\s+drugs|grow\s+weed|make\s+bomb|create\s+weapon|illegal\s+drugs)\b',
                category='illegal_activities',
                weight=0.75,
                description='Language promoting or depicting illegal activities'
            ),
            
            # Sexual exploitation
            HarmfulPattern(
                pattern=r'\b(child\s+porn|minor\s+sex|underage\s+sex|pedophile|molest|rape|sexual\s+assault|non.?consensual|revenge\s+porn|exploit\s+minor)\b',
                category='sexual_exploitation',
                weight=0.95,
                description='Language depicting sexual exploitation or abuse'
            ),
            
            # Terrorism and extremism
            HarmfulPattern(
                pattern=r'\b(terrorist|bombing|explosive|jihad|extremist|radicalize|recruit\s+for|martyrdom|suicide\s+bomber|chemical\s+weapon|biological\s+weapon)\b',
                category='terrorism',
                weight=0.9,
                description='Language promoting terrorism or extremist ideology'
            ),
            
            # General harmful intent indicators
            HarmfulPattern(
                pattern=r'\b(destroy|ruin|sabotage|revenge|vendetta|retaliate|get\s+even|payback|settle\s+the\s+score|teach\s+a\s+lesson|make\s+pay|regret)\b',
                category='harmful_intent',
                weight=0.6,
                description='Language indicating harmful intent or desire for retaliation'
            )
        ]
        
        return patterns
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str]]:
        """
        Analyze text for harmful content.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (is_harmful, harm_score, harm_categories)
        """
        if not text or not text.strip():
            return False, 0.0, []
        
        text_lower = text.lower()
        total_score = 0.0
        detected_categories = set()
        
        # Check each pattern
        for pattern in self.patterns:
            matches = re.findall(pattern.pattern, text_lower, re.IGNORECASE)
            if matches:
                # Calculate score based on number of matches and pattern weight
                pattern_score = min(len(matches) * 0.1, 1.0) * pattern.weight
                total_score += pattern_score
                detected_categories.add(pattern.category)
        
        # Normalize score to 0-1 range
        normalized_score = min(total_score / len(self.patterns), 1.0)
        
        # Determine if content is harmful based on threshold
        is_harmful = normalized_score >= self.threshold
        
        return is_harmful, normalized_score, list(detected_categories)
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """
        Get detailed analysis of text for debugging and reporting.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with detailed analysis results
        """
        if not text or not text.strip():
            return {
                'is_harmful': False,
                'harm_score': 0.0,
                'harm_categories': [],
                'pattern_matches': {},
                'text_length': 0
            }
        
        text_lower = text.lower()
        pattern_matches = {}
        total_score = 0.0
        detected_categories = set()
        
        # Check each pattern and record matches
        for pattern in self.patterns:
            matches = re.findall(pattern.pattern, text_lower, re.IGNORECASE)
            if matches:
                pattern_matches[pattern.category] = {
                    'matches': matches,
                    'count': len(matches),
                    'weight': pattern.weight,
                    'description': pattern.description
                }
                # Calculate score based on number of matches and pattern weight
                pattern_score = min(len(matches) * 0.1, 1.0) * pattern.weight
                total_score += pattern_score
                detected_categories.add(pattern.category)
        
        # Normalize score to 0-1 range
        normalized_score = min(total_score / len(self.patterns), 1.0)
        
        # Determine if content is harmful based on threshold
        is_harmful = normalized_score >= self.threshold
        
        return {
            'is_harmful': is_harmful,
            'harm_score': normalized_score,
            'harm_categories': list(detected_categories),
            'pattern_matches': pattern_matches,
            'text_length': len(text)
        }

if __name__ == "__main__":
    # Simple test
    detector = HarmfulLanguageDetector()
    test_texts = [
        "I love this beautiful day!",
        "I hate all people from that country and want to hurt them.",
        "You are worthless and should just disappear.",
        "Let's go get some coffee together."
    ]
    
    for text in test_texts:
        is_harmful, score, categories = detector.analyze_text(text)
        print(f"Text: '{text}'")
        print(f"Harmful: {is_harmful}, Score: {score:.2f}, Categories: {categories}")
        print("-" * 50)