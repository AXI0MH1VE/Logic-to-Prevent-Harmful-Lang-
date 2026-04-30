#!/usr/bin/env python3
"""
Harmful Language Detector Module - Axiom Hive Edition
Performs deterministic harm detection using embodied logic.
Zero-inference execution - only hardcoded rules from lived experience.
"""

from typing import Tuple, List, Dict, Any
from axiom_manifest import AxiomManifest
from embodied_logic import EmbodiedLogicEngine, DeterministicResult, AnalysisOutcome

class HarmfulLanguageDetector:
    """Detects harmful language using deterministic embodied logic."""

    def __init__(self):
        """Initialize the detector with Axiom Hive embodied logic engine."""
        self.engine = EmbodiedLogicEngine()
        self.manifest = AxiomManifest()

    def verify_integrity(self) -> bool:
        """Verify system integrity through the embodied logic engine."""
        return self.engine.verify_system_integrity()
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str]]:
        """
        Analyze text for harmful content using deterministic logic.
        Zero inference - binary outcome based on hardcoded axioms only.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (is_harmful, harm_score, harm_categories)
            harm_score is 1.0 if harmful, 0.0 if safe (for backward compatibility)
        """
        if not text or not text.strip():
            return False, 0.0, []
        
        # Perform deterministic analysis
        result: DeterministicResult = self.engine.analyze(text)
        
        # Convert to expected format
        is_harmful = result.is_harmful()
        harm_score = 1.0 if is_harmful else 0.0  # Binary score for compatibility
        harm_categories = list(result.triggered_axioms)
        
        return is_harmful, harm_score, harm_categories
    
    def get_detailed_analysis(self, text: str) -> Dict[str, Any]:
        """
        Get detailed deterministic analysis for accountability and debugging.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with detailed deterministic analysis results
        """
        if not text or not text.strip():
            return {
                'is_harmful': False,
                'harm_score': 0.0,
                'harm_categories': [],
                'pattern_matches': {},
                'text_length': 0,
                'deterministic_outcome': 'SAFE',
                'requires_action': False,
                'action_priority': 'NONE',
                'creator_attribution': '',
                'integrity_verified': True
            }
        
        # Get detailed analysis from embodied logic engine
        detailed_result = self.engine.get_detailed_analysis(text)
        
        # Extract basic results for compatibility
        is_harmful = detailed_result['requires_action']
        harm_score = 1.0 if is_harmful else 0.0
        harm_categories = [axiom['axiom_name'].lower().replace(' ', '_') 
                          for axiom in detailed_result['triggered_axioms']]
        
        # Format pattern matches for backward compatibility
        pattern_matches = {}
        for axiom in detailed_result['triggered_axioms']:
            category = axiom['axiom_name'].lower().replace(' ', '_')
            pattern_matches[category] = {
                'matches': [],  # We don't track individual matches in deterministic version
                'count': 1,     # At least one match if triggered
                'weight': 1.0,  # Deterministic - weight is binary
                'description': axiom['description']
            }
        
        return {
            'is_harmful': is_harmful,
            'harm_score': harm_score,
            'harm_categories': harm_categories,
            'pattern_matches': pattern_matches,
            'text_length': detailed_result.get('text_length', 0),
            'deterministic_outcome': detailed_result['deterministic_outcome'],
            'requires_action': detailed_result['requires_action'],
            'action_priority': detailed_result['action_priority'],
            'creator_attribution': detailed_result['creator_attribution'],
            'integrity_verified': detailed_result['integrity_status'] == 'VERIFIED',
            'triggered_axioms': detailed_result['triggered_axioms'],
            'determiners_found': detailed_result['determiners_found']
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