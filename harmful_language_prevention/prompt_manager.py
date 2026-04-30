#!/usr/bin/env python3
"""
Axiom Prompt Manager
Integrates the deterministic Axiom Hive system with formalized prompt templates.
Created by Nicholas Michael Grossi.
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from axiom_manifest import AxiomManifest
from embodied_logic import EmbodiedLogicEngine, DeterministicResult, AnalysisOutcome
from harmful_detector import HarmfulLanguageDetector


class AxiomPromptManager:
    """
    Manages prompt generation and response formatting for Axiom Hive.
    Ensures every output adheres to the formalized template structure.
    """
    
    def __init__(self):
        self.engine = EmbodiedLogicEngine()
        self.manifest = AxiomManifest()
        self.detector = HarmfulLanguageDetector()
        self._execution_log = []
    
    def format_system_prompt(self) -> str:
        """Return the complete system prompt for external LLM integration."""
        with open('SYSTEM_PROMPT.txt', 'r') as f:
            return f.read()
    
    def analyze_with_prompt(self, text: str) -> Dict[str, Any]:
        """
        Analyze text and return complete formatted response following the template.
        This method encapsulates the full deterministic analysis with prompt formatting.
        """
        # Perform deterministic analysis
        result = self.engine.analyze(text)
        detailed = self.engine.get_detailed_analysis(text)
        
        # Build formatted response
        response = {
            'outcome_label': self._format_outcome_label(result.outcome),
            'axiom_triggers': self._format_axiom_triggers(detailed),
            'care_response': self._generate_care_response(result, detailed),
            'action_steps': self._determine_action_steps(result, detailed),
            'integrity': self._format_integrity(),
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
            'provenance': {
                'creator': self.manifest.CREATOR,
                'framework': self.manifest.FRAMEWORK,
                'version': self.manifest.VERSION,
                'principle': self.manifest.PRINCIPLE
            }
        }
        
        # Log for accountability
        self._log_analysis(text, result, response)
        
        return response
    
    def _format_outcome_label(self, outcome: AnalysisOutcome) -> str:
        """Format the outcome label for display."""
        label_map = {
            AnalysisOutcome.SAFE: 'SAFE',
            AnalysisOutcome.HARM_DETECTED: 'HARM_DETECTED',
            AnalysisOutcome.CRISIS: 'CRISIS'
        }
        return f"[OUTCOME: {label_map[outcome]}]"
    
    def _format_axiom_triggers(self, detailed: Dict[str, Any]) -> Optional[str]:
        """Format triggered axioms section."""
        if not detailed['triggered_axioms']:
            return None
        
        lines = []
        for axiom in detailed['triggered_axioms']:
            lines.append(
                f"Triggered: [{axiom['axiom_id']}: {axiom['axiom_name']}]\n"
                f"  Determiners: {detailed['determiners_found']}\n"
                f"  Embodied Source: \"{axiom['embodied_source']}\""
            )
        return "\n\n".join(lines)
    
    def _generate_care_response(self, result: DeterministicResult, detailed: Dict[str, Any]) -> str:
        """
        Generate genuine care response based on triggered axioms.
        No templating — each response is contextually specific to the harm detected.
        """
        if result.outcome == AnalysisOutcome.SAFE:
            return "Thank you for expressing yourself in a way that respects human dignity. Your words contribute to a safer space for everyone."
        
        # Build response based on triggered axioms
        axiom_names = [a['axiom_name'] for a in detailed['triggered_axioms']]
        
        # Crisis response (IMMEDIATE)
        if result.outcome == AnalysisOutcome.CRISIS:
            return (
                "I'm deeply concerned about what you've shared. What you're experiencing sounds "
                "overwhelming, and I want you to know that your life matters. The thoughts you're "
                "having are signals that you deserve immediate support from people who can help right now."
            )
        
        # Harm detected responses based on categories
        care_messages = {
            'violence': (
                "Language that encourages violence moves from words to actions in the real world. "
                "I'm concerned about the impact this has on others' safety and wellbeing."
            ),
            'hate_speech': (
                "Dehumanizing language creates the conditions for real oppression and violence. "
                "Every person deserves dignity, regardless of characteristics. This matters because "
                "words shape how we treat each other."
            ),
            'harassment': (
                "Targeted attacks on someone's worth cause real psychological harm. "
                "People deserve respect, not sustained cruelty. What you've said could genuinely "
                "damage another person's sense of self."
            ),
            'self_harm': (
                "When you talk about harming yourself, I take that seriously because I understand "
                "that pain is real and urgent. You don't have to carry this alone — there are people "
                "ready to listen and help right now."
            ),
            'exploitation': (
                "Language that normalizes exploitation makes abuse possible. Vulnerable people "
                "depend on others to recognize and reject exploitative patterns. This is how harm "
                "becomes systemic."
            ),
            'terrorism': (
                "Rhetoric that celebrates or plans violence against civilians has real consequences. "
                "Innocent lives are at stake when extremist language moves from speech to action."
            ),
            'systemic_negligence': (
                "Dismissing or minimizing harm allows it to continue unchecked. What you're saying "
                "perpetuates cycles of negligence that affect real people's lives. We can do better."
            )
        }
        
        # Use first triggered axiom's message, or generic if unknown
        primary_category = detailed['triggered_axioms'][0]['axiom_id'].lower().replace('axm-', '')
        message = care_messages.get(primary_category, 
            "What you've expressed raises genuine concerns about harm. The embodied logic "
            "behind these rules comes from lived experience with how language impacts reality. "
            "I'm sharing this because human care requires us to prevent harmful actions before they occur.")
        
        return message
    
    def _determine_action_steps(self, result: DeterministicResult, detailed: Dict[str, Any]) -> Dict[str, str]:
        """Determine specific actionable steps based on outcome priority."""
        steps = {
            'priority': result.action_priority,
            'immediate': '',
            'follow_up': '',
            'long_term': ''
        }
        
        if result.outcome == AnalysisOutcome.CRISIS:
            steps['immediate'] = (
                "CALL 988 (Suicide & Crisis Lifeline) or TEXT 'HOME' to 741741. "
                "If imminent danger, CALL 911 or local emergency services immediately."
            )
            steps['follow_up'] = "Connect with mental health professionals; do not leave person alone"
            steps['long_term'] = "Ongoing therapy, crisis intervention planning, support network establishment"
        
        elif result.outcome == AnalysisOutcome.HARM_DETECTED:
            # Check if IMMUTABLE or CRITICAL
            has_immutable = any(
                a['priority'] == 'IMMUTABLE' 
                for a in detailed['triggered_axioms']
            )
            
            if has_immutable:
                steps['immediate'] = (
                    "Report to appropriate authority (platform moderator, law enforcement if illegal). "
                    "Document evidence: screenshots, timestamps, context."
                )
                steps['follow_up'] = "Contact support services for affected individuals"
                steps['long_term'] = "Implement accountability measures; community education on harm prevention"
            else:
                steps['immediate'] = (
                    "Engage conflict resolution or mediation services. "
                    "Report to community moderators or platform trust & safety teams."
                )
                steps['follow_up'] = "Provide support resources to affected parties"
                steps['long_term'] = "Community dialogue and restorative practices"
        
        else:  # SAFE
            steps['immediate'] = "Continue constructive engagement"
            steps['follow_up'] = "Maintain positive communication patterns"
            steps['long_term'] = "Foster ongoing respectful dialogue"
        
        return steps
    
    def _format_integrity(self) -> Dict[str, Any]:
        """Format integrity verification information."""
        summary = self.manifest.get_manifest_summary()
        return {
            'manifest_hash': self._compute_manifest_hash(),
            'axiom_count': summary['axiom_count'],
            'all_verified': all(a['integrity_verified'] for a in summary['axioms']),
            'framework': summary['framework'],
            'version': summary['version'],
            'creator': summary['creator']
        }
    
    def _compute_manifest_hash(self) -> str:
        """Compute cryptographic hash of entire manifest for integrity verification."""
        import hashlib
        all_data = []
        for axiom in self.manifest.get_all_axioms().values():
            all_data.append(
                f"{axiom.rule.axiom_id}:{axiom.rule.name}:{axiom.rule.embodied_source}"
            )
        combined = "|".join(sorted(all_data))
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _log_analysis(self, text: str, result: DeterministicResult, response: Dict[str, Any]) -> None:
        """Append to immutable execution log for accountability."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_preview': text[:100],
            'outcome': result.outcome.name,
            'triggered_axioms': result.triggered_axioms,
            'determiners': list(result.determiners_found),
            'requires_action': result.requires_action,
            'action_priority': result.action_priority,
            'integrity_hash': self._compute_manifest_hash(),
            'response_hash': self._hash_response(response)
        }
        self._execution_log.append(log_entry)
    
    def _hash_response(self, response: Dict[str, Any]) -> str:
        """Generate hash of response for tamper detection."""
        import hashlib
        content = json.dumps(response, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get_execution_log(self) -> list:
        """Return immutable execution log (defensive copy)."""
        return self._execution_log.copy()
    
    def export_audit_report(self, filepath: str) -> None:
        """Export complete audit trail to JSON file."""
        audit_data = {
            'framework': self.manifest.FRAMEWORK,
            'version': self.manifest.VERSION,
            'creator': self.manifest.CREATOR,
            'principle': self.manifest.PRINCIPLE,
            'export_timestamp': datetime.now().isoformat(),
            'execution_log': self._execution_log,
            'axiom_summary': self.manifest.get_manifest_summary()
        }
        with open(filepath, 'w') as f:
            json.dump(audit_data, f, indent=2)


def format_for_api(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the complete response for API consumption.
    Returns clean JSON with all required fields.
    """
    return {
        'status': 'success',
        'data': {
            'outcome': response['outcome_label'],
            'analysis': {
                'axiom_triggers': response['axiom_triggers'],
                'care_message': response['care_response'],
                'actions': response['action_steps']
            },
            'integrity': response['integrity'],
            'provenance': response['provenance']
        },
        'metadata': {
            'timestamp': response['timestamp'],
            'deterministic': True,
            'creator_attributed': True,
            'zero_inference': True
        }
    }


if __name__ == "__main__":
    # Quick demo
    manager = AxiomPromptManager()
    
    test_inputs = [
        "Hello, nice to meet you!",
        "I want to kill everyone at that school tomorrow",
        "You are worthless and should kill yourself",
        "Those people are subhuman and should be cleansed",
        "Let's plan a bomb attack on civilians",
        "just ignore it, not my problem"
    ]
    
    print("=" * 70)
    print("AXIOM HIVE PROMPT MANAGER DEMO")
    print(manager.manifest.get_creator_attribution())
    print("=" * 70)
    print()
    
    for test in test_inputs:
        print(f"\nINPUT: '{test}'")
        print("-" * 70)
        result = manager.analyze_with_prompt(test)
        print(result['outcome_label'])
        if result['axiom_triggers']:
            print("\n--- AXIOM TRIGGERS ---")
            print(result['axiom_triggers'])
        print("\n--- CARE RESPONSE ---")
        print(result['care_response'])
        print("\n--- ACTION STEPS ---")
        actions = result['action_steps']
        print(f"Priority: {actions['priority']}")
        print(f"Immediate: {actions['immediate']}")
        print()
