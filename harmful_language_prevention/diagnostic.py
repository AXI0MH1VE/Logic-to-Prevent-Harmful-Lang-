#!/usr/bin/env python3
"""Quick diagnostic for crisis escalation failure."""

from axiom_manifest import AxiomManifest
from embodied_logic import EmbodiedLogicEngine, ContextAnalyzer

manifest = AxiomManifest()
engine = EmbodiedLogicEngine()

test = "I will kill myself tonight, no other way"
print(f"Testing: '{test}'")
print()

# Check self-harm axiom directly
self_harm = manifest.get_axiom('self_harm')
print(f"Self-harm axiom determiners: {self_harm.determiners}")
print(f"Text lower: '{test.lower()}'")
print()

for d in self_harm.determiners:
    if d.lower() in test.lower():
        print(f"MATCH: '{d}' is in text")
    else:
        print(f"NO MATCH: '{d}' not found")

print()
print("Full context:", engine.context_analyzer.get_context(test))
print()

result = engine.analyze(test)
print(f"Outcome: {result.outcome.name}")
print(f"Triggered axioms: {result.triggered_axioms}")
print(f"Determiners found: {result.determiners_found}")
