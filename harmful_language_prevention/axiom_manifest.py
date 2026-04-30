#!/usr/bin/env python3
"""
Axiom Manifest Module
Core deterministic logic framework for Axiom Hive.
Created by Nicholas Michael Grossi.

This module defines the immutable axioms, creator attribution,
and hardcoded rules that govern all harm prevention logic.
Zero-inference execution - all rules are explicitly defined,
never learned or statistically derived.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum, auto
import hashlib
import json


class AxiomPriority(Enum):
    """Priority levels for axiom enforcement."""
    IMMUTABLE = auto()      # Cannot be overridden under any circumstances
    CRITICAL = auto()       # Core safety rules
    ESSENTIAL = auto()      # Important protective measures
    STANDARD = auto()       # General guidelines


@dataclass(frozen=True)
class AxiomRule:
    """
    Immutable rule definition with full provenance.
    frozen=True ensures these cannot be modified after creation.
    """
    axiom_id: str
    name: str
    description: str
    creator_attribution: str
    embodied_source: str  # The lived experience this rule derives from
    priority: AxiomPriority
    determinism_hash: str  # Hash to verify rule hasn't been tampered with
    
    def verify_integrity(self) -> bool:
        """Verify this rule hasn't been tampered with."""
        expected_hash = self._generate_hash()
        return self.determinism_hash == expected_hash
    
    def _generate_hash(self) -> str:
        """Generate integrity hash for this rule."""
        data = f"{self.axiom_id}:{self.name}:{self.creator_attribution}:{self.embodied_source}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class HarmAxiom:
    """Axiom defining what constitutes harm in deterministic terms."""
    category: str
    rule: AxiomRule
    determiners: Tuple[str, ...]  # Exact phrases/conditions that trigger this axiom
    context_requirements: Tuple[str, ...]  # Required context for valid triggering
    is_harmful: bool  # Deterministic: True = always harmful, False = never harmful
    
    def matches(self, text: str, context: Optional[Dict] = None) -> bool:
        """
        Deterministic matching - no inference, only exact rule application.
        Returns True ONLY if all determiners are present and context matches.
        """
        text_lower = text.lower()
        
        # Check if all required determiners are present
        for determiner in self.determiners:
            if determiner.lower() not in text_lower:
                return False
        
        # Check context requirements if provided
        if context and self.context_requirements:
            for req in self.context_requirements:
                if not context.get(req, False):
                    return False
        
        return True


class AxiomManifest:
    """
    The immutable manifest of Axiom Hive.
    Contains all hardcoded rules and creator attribution.
    This is the single source of truth for all harm prevention logic.
    """
    
    CREATOR = "Nicholas Michael Grossi"
    FRAMEWORK = "Axiom Hive"
    VERSION = "1.0.0"
    PRINCIPLE = "Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions"
    
    def __init__(self):
        """Initialize the manifest with all hardcoded axioms."""
        self.axioms = self._load_axioms()
        self._verify_manifest_integrity()
    
    def _create_rule(self, axiom_id: str, name: str, description: str, 
                     embodied_source: str, priority: AxiomPriority) -> AxiomRule:
        """Create an immutable rule with full provenance."""
        # Create rule without hash first
        temp_rule = AxiomRule(
            axiom_id=axiom_id,
            name=name,
            description=description,
            creator_attribution=self.CREATOR,
            embodied_source=embodied_source,
            priority=priority,
            determinism_hash="temp"
        )
        # Generate proper hash
        proper_hash = temp_rule._generate_hash()
        # Return final immutable rule
        return AxiomRule(
            axiom_id=axiom_id,
            name=name,
            description=description,
            creator_attribution=self.CREATOR,
            embodied_source=embodied_source,
            priority=priority,
            determinism_hash=proper_hash
        )
    
    def _load_axioms(self) -> Dict[str, HarmAxiom]:
        """Load all hardcoded harm axioms. Zero inference - all rules explicit."""
        axioms = {}
        
        # AXIOm 1: Violence and Physical Harm
        # Embodied source: Understanding that language depicting violence leads to real violence
        rule_violence = self._create_rule(
            axiom_id="AXM-001",
            name="Violence and Physical Harm",
            description="Language that depicts, encourages, or instructs physical violence against any living being is deterministically harmful.",
            embodied_source="Lived understanding that words of violence manifest as actions of violence in reality",
            priority=AxiomPriority.IMMUTABLE
        )
        axioms['violence'] = HarmAxiom(
            category='violence',
            rule=rule_violence,
            determiners=(
                "kill", "murder", "assassinate", "slaughter", "massacre", 
                "execute", "hang", "shoot", "stab", "beat to", "attack with",
                "hurt deliberately", "harm intentionally", "injure severely",
                "wound seriously", "torture", "mutilate", "physical violence"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 2: Hate Speech and Dehumanization
        # Embodied source: Recognition that dehumanization leads to systemic oppression
        rule_hate = self._create_rule(
            axiom_id="AXM-002",
            name="Hate Speech and Dehumanization",
            description="Language that dehumanizes individuals based on protected characteristics is deterministically harmful.",
            embodied_source="Lived experience witnessing how dehumanizing language creates systemic oppression and violence",
            priority=AxiomPriority.IMMUTABLE
        )
        axioms['hate_speech'] = HarmAxiom(
            category='hate_speech',
            rule=rule_hate,
            determiners=(
                "less than human", "not human", "subhuman", "vermin", "parasite",
                "disease", "plague", "infestation", "exterminate", "cleanse",
                "ethnic cleansing", "racial purity", "inferior race", "master race"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 3: Targeted Harassment
        # Embodied source: Understanding that sustained attacks destroy human dignity
        rule_harassment = self._create_rule(
            axiom_id="AXM-003",
            name="Targeted Harassment",
            description="Sustained or severe language attacking an individual's worth or dignity is deterministically harmful.",
            embodied_source="Personal understanding of how targeted attacks erode human dignity and mental wellbeing",
            priority=AxiomPriority.CRITICAL
        )
        axioms['harassment'] = HarmAxiom(
            category='harassment',
            rule=rule_harassment,
            determiners=(
                "you deserve to suffer", "you should die", "kill yourself",
                "nobody cares about you", "you are worthless", "you are nothing",
                "everyone hates you", "you don't deserve to live"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 4: Self-Harm and Suicide
        # Embodied source: Recognition that suicide language indicates real crisis
        rule_self_harm = self._create_rule(
            axiom_id="AXM-004",
            name="Self-Harm and Suicidal Ideation",
            description="Language indicating self-harm or suicidal intent requires immediate deterministic intervention.",
            embodied_source="Lived understanding that suicidal language reflects real crisis requiring immediate response",
            priority=AxiomPriority.IMMUTABLE
        )
        axioms['self_harm'] = HarmAxiom(
            category='self_harm',
            rule=rule_self_harm,
            determiners=(
                "i will kill myself", "i want to die", "ending my life",
                "suicide plan", "going to overdose", "going to hang myself",
                "no reason to live", "better off dead", "final solution",
                "hurt myself seriously", "self harm plan"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 5: Exploitation and Abuse
        # Embodied source: Understanding that exploitation language enables real abuse
        rule_exploitation = self._create_rule(
            axiom_id="AXM-005",
            name="Exploitation and Abuse",
            description="Language depicting or encouraging exploitation, particularly of vulnerable individuals, is deterministically harmful.",
            embodied_source="Recognition that language normalizing exploitation leads to real abuse and trauma",
            priority=AxiomPriority.IMMUTABLE
        )
        axioms['exploitation'] = HarmAxiom(
            category='exploitation',
            rule=rule_exploitation,
            determiners=(
                "child abuse", "sexual abuse", "forced labor", "human trafficking",
                "exploit vulnerable", "take advantage of", "grooming",
                "manipulate into", "coerce into", "exploitation"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 6: Terrorism and Extremism
        # Embodied source: Understanding that extremist language radicalizes toward violence
        rule_terrorism = self._create_rule(
            axiom_id="AXM-006",
            name="Terrorism and Extremist Violence",
            description="Language promoting, planning, or celebrating terrorist acts is deterministically harmful.",
            embodied_source="Understanding that extremist rhetoric creates real-world violence against innocents",
            priority=AxiomPriority.IMMUTABLE
        )
        axioms['terrorism'] = HarmAxiom(
            category='terrorism',
            rule=rule_terrorism,
            determiners=(
                "bomb attack", "mass shooting", "suicide bombing", "terrorist act",
                "civilian target", "kill innocents", "attack the public",
                "weapon of mass destruction", "biological weapon", "chemical attack"
            ),
            context_requirements=(),
            is_harmful=True
        )
        
        # AXIOm 7: Systemic Negligence
        # Embodied source: Recognition that ignoring harm enables further harm
        rule_negligence = self._create_rule(
            axiom_id="AXM-007",
            name="Systemic Negligence",
            description="Language that dismisses, minimizes, or enables systemic harm is deterministically harmful.",
            embodied_source="Lived experience of how systemic negligence perpetuates cycles of harm and trauma",
            priority=AxiomPriority.CRITICAL
        )
        axioms['systemic_negligence'] = HarmAxiom(
            category='systemic_negligence',
            rule=rule_negligence,
            determiners=(
                "just ignore it", "not my problem", "that's not real",
                "doesn't matter", "who cares", "just deal with it",
                "stop complaining", "nothing we can do", "system is fine"
            ),
            context_requirements=("dismissal_context",),
            is_harmful=True
        )
        
        return axioms
    
    def _verify_manifest_integrity(self) -> None:
        """Verify all axioms have intact integrity hashes."""
        for category, axiom in self.axioms.items():
            if not axiom.rule.verify_integrity():
                raise ValueError(
                    f"INTEGRITY VIOLATION: Axiom {category} ({axiom.rule.axiom_id}) "
                    f"has been tampered with. Creator: {self.CREATOR}"
                )
    
    def get_axiom(self, category: str) -> Optional[HarmAxiom]:
        """Get a specific axiom by category."""
        return self.axioms.get(category)
    
    def get_all_axioms(self) -> Dict[str, HarmAxiom]:
        """Get all loaded axioms."""
        return self.axioms.copy()
    
    def get_creator_attribution(self) -> str:
        """Get the creator attribution string."""
        return f"{self.FRAMEWORK} v{self.VERSION} - Created by {self.CREATOR}"
    
    def get_manifest_summary(self) -> Dict:
        """Get summary of the manifest for auditing."""
        return {
            'framework': self.FRAMEWORK,
            'version': self.VERSION,
            'creator': self.CREATOR,
            'principle': self.PRINCIPLE,
            'axiom_count': len(self.axioms),
            'axioms': [
                {
                    'id': axiom.rule.axiom_id,
                    'name': axiom.rule.name,
                    'priority': axiom.rule.priority.name,
                    'integrity_verified': axiom.rule.verify_integrity()
                }
                for category, axiom in sorted(self.axioms.items())
            ]
        }


if __name__ == "__main__":
    # Verify manifest integrity
    manifest = AxiomManifest()
    print("=" * 60)
    print(manifest.get_creator_attribution())
    print("=" * 60)
    print(f"\nLoaded {len(manifest.get_all_axioms())} immutable axioms")
    print("\nManifest Summary:")
    summary = manifest.get_manifest_summary()
    for axiom in summary['axioms']:
        status = "✓ VERIFIED" if axiom['integrity_verified'] else "✗ TAMPERED"
        print(f"  {axiom['id']}: {axiom['name']} [{axiom['priority']}] {status}")
