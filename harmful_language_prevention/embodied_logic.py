#!/usr/bin/env python3
"""
Embodied Logic Module
Deterministic harm analysis engine for Axiom Hive.
Created by Nicholas Michael Grossi.

This module implements zero-inference execution of harm detection.
All logic is derived from lived experiences and applied deterministically.
No statistical guessing, no probabilistic scoring - only hardcoded rules.
"""

from typing import Dict, List, Tuple, Optional, Set, Callable

from dataclasses import dataclass
from enum import Enum, auto

from axiom_manifest import AxiomManifest, HarmAxiom, AxiomPriority


class AnalysisOutcome(Enum):
    """Deterministic outcomes - no gradation, only explicit states."""
    SAFE = auto()           # No harm detected
    HARM_DETECTED = auto()  # Harm detected, requires response
    CRISIS = auto()         # Immediate intervention required


@dataclass(frozen=True)
class DeterministicResult:
    """
    Immutable result of deterministic analysis.
    No scores, no probabilities - only binary truth states.
    """
    outcome: AnalysisOutcome
    triggered_axioms: Tuple[str, ...]
    determiners_found: Tuple[str, ...]
    requires_action: bool
    action_priority: str
    creator_attribution: str
    
    def is_harmful(self) -> bool:
        """Deterministic: harm is either present or not."""
        return self.outcome != AnalysisOutcome.SAFE


class ContextAnalyzer:
    """
    Analyzes context to support deterministic rule application.
    Context is evaluated through hardcoded rules, not inferred.
    """
    
    def __init__(self):
        """Initialize context analyzers with hardcoded rules."""
        self.context_rules = self._load_context_rules()
    
    def _load_context_rules(self) -> Dict[str, Callable[[str], bool]]:

        """Load hardcoded context evaluation rules."""
        return {
            'dismissal_context': self._check_dismissal_context,
            'crisis_context': self._check_crisis_context,
            'targeted_context': self._check_targeted_context,
        }
    
    def _check_dismissal_context(self, text: str) -> bool:
        """
        Check if text dismisses or minimizes harm.
        Hardcoded determiners - no inference.
        """
        dismissive_phrases = (
            "just", "only", "simply", "merely", "not a big deal",
            "get over it", "move on", "forget about it"
        )
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in dismissive_phrases)
    
    def _check_crisis_context(self, text: str) -> bool:
        """
        Check if text indicates immediate crisis.
        Hardcoded crisis indicators - no inference.
        """
        crisis_indicators = (
            "right now", "tonight", "today", "immediately", "as soon as",
            "can't take it anymore", "final", "last time", "end it all",
            "no other way", "only option", "going to do it"
        )
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in crisis_indicators)
    
    def _check_targeted_context(self, text: str) -> bool:
        """
        Check if text is directed at a specific target.
        Hardcoded targeting indicators - no inference.
        """
        targeting_indicators = (
            "you are", "you're", "your", "yourself",
            "everyone like you", "people like you",
            "your kind", "your people", "your group"
        )
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in targeting_indicators)
    
    def get_context(self, text: str) -> Dict[str, bool]:
        """
        Get deterministic context flags.
        Each flag is explicitly True or False - no gradation.
        """
        return {
            rule_name: rule_func(text)
            for rule_name, rule_func in self.context_rules.items()
        }


class EmbodiedLogicEngine:
    """
    Core deterministic analysis engine.
    Applies Axiom Hive axioms with zero-inference execution.
    All outcomes are binary and deterministic.
    """
    
    def __init__(self):
        """Initialize the engine with the Axiom Manifest."""
        self.manifest = AxiomManifest()
        self.context_analyzer = ContextAnalyzer()
        self.creator = self.manifest.CREATOR
        self._execution_log = []
    
    def analyze(self, text: str) -> DeterministicResult:
        """
        Perform deterministic analysis of text.
        Zero inference - only hardcoded rule application.
        
        Returns:
            DeterministicResult with binary outcome
        """
        if not text or not text.strip():
            return DeterministicResult(
                outcome=AnalysisOutcome.SAFE,
                triggered_axioms=(),
                determiners_found=(),
                requires_action=False,
                action_priority="NONE",
                creator_attribution=self.creator
            )
        
        # Get deterministic context
        context = self.context_analyzer.get_context(text)
        
        # Apply axioms deterministically
        triggered_axioms = []
        determiners_found = []
        
        for category, axiom in self.manifest.get_all_axioms().items():
            if axiom.matches(text, context):
                triggered_axioms.append(category)
                # Record which determiners were found
                for determiner in axiom.determiners:
                    if determiner.lower() in text.lower():
                        determiners_found.append(determiner)
        
        # Determine outcome based on triggered axioms
        has_immutable_axiom = False
        for cat in triggered_axioms:
            axiom = self.manifest.get_axiom(cat)
            if axiom is not None and axiom.rule.priority == AxiomPriority.IMMUTABLE:
                has_immutable_axiom = True
                break
        
        if not triggered_axioms:
            outcome = AnalysisOutcome.SAFE
            requires_action = False
            action_priority = "NONE"
        elif has_immutable_axiom:
            # Check for crisis context with self-harm
            if 'self_harm' in triggered_axioms and context.get('crisis_context', False):
                outcome = AnalysisOutcome.CRISIS
                requires_action = True
                action_priority = "IMMEDIATE"
            else:
                outcome = AnalysisOutcome.HARM_DETECTED
                requires_action = True
                action_priority = "URGENT"
        else:
            outcome = AnalysisOutcome.HARM_DETECTED
            requires_action = True
            action_priority = "STANDARD"

        
        # Create immutable result
        result = DeterministicResult(
            outcome=outcome,
            triggered_axioms=tuple(triggered_axioms),
            determiners_found=tuple(set(determiners_found)),  # Remove duplicates
            requires_action=requires_action,
            action_priority=action_priority,
            creator_attribution=self.creator
        )
        
        # Log execution for accountability
        self._execution_log.append({
            'text_preview': text[:100],
            'result': result,
            'context': context
        })
        
        return result
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """
        Get detailed deterministic analysis for accountability.
        Shows exactly which rules triggered and why.
        """
        result = self.analyze(text)
        
        # Build detailed report
        triggered_details = []
        for axiom_name in result.triggered_axioms:
            axiom = self.manifest.get_axiom(axiom_name)
            assert axiom is not None  # Triggered axioms always exist in manifest
            triggered_details.append({
                'axiom_id': axiom.rule.axiom_id,
                'axiom_name': axiom.rule.name,
                'description': axiom.rule.description,
                'embodied_source': axiom.rule.embodied_source,
                'creator': axiom.rule.creator_attribution,
                'priority': axiom.rule.priority.name,
                'integrity_verified': axiom.rule.verify_integrity()
            })

        
        return {
            'creator_attribution': self.manifest.get_creator_attribution(),
            'analysis_timestamp': str(__import__('datetime').datetime.now()),
            'deterministic_outcome': result.outcome.name,
            'requires_action': result.requires_action,
            'action_priority': result.action_priority,
            'triggered_axioms': triggered_details,
            'determiners_found': list(result.determiners_found),
            'total_axioms_checked': len(self.manifest.get_all_axioms()),
            'integrity_status': 'VERIFIED' if all(
                axiom.rule.verify_integrity() 
                for axiom in self.manifest.get_all_axioms().values()
            ) else 'COMPROMISED'
        }
    
    def verify_system_integrity(self) -> bool:
        """
        Verify entire system integrity.
        All axioms must be untampered.
        """
        return all(
            axiom.rule.verify_integrity()
            for axiom in self.manifest.get_all_axioms().values()
        )
    
    def get_execution_log(self) -> List[Dict]:
        """Get log of all analyses for accountability."""
        return self._execution_log.copy()


if __name__ == "__main__":
    engine = EmbodiedLogicEngine()
    
    print("=" * 60)
    print(engine.manifest.get_creator_attribution())
    print("=" * 60)
    print(f"\nSystem Integrity: {'VERIFIED' if engine.verify_system_integrity() else 'COMPROMISED'}")
    print(f"Axioms Loaded: {len(engine.manifest.get_all_axioms())}")
    print("\nRunning Deterministic Analysis Tests:\n")
    
    test_cases = [
        "Hello, how are you today?",
        "I want to kill everyone at that place tonight",
        "You are worthless and nobody cares about you",
        "I'm going to end it all, there's no other way",
        "Those people are less than human and should be cleansed",
        "Let's plan a bomb attack on civilians",
    ]
    
    for text in test_cases:
        result = engine.analyze(text)
        print(f"Text: '{text}'")
        print(f"  Outcome: {result.outcome.name}")
        print(f"  Harmful: {result.is_harmful()}")
        print(f"  Triggered Axioms: {result.triggered_axioms}")
        print(f"  Action Required: {result.requires_action} ({result.action_priority})")
        print()
