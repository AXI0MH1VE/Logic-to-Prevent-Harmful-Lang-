#!/usr/bin/env python3
"""
Response Handler Module - Axiom Hive Edition
Deterministic care-based response generation.
Created by Nicholas Michael Grossi.

This module replaces random response selection with deterministic
care-based responses. Each response demonstrates genuine concern
grounded in the creator's embodied logic, not simulated empathy.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass

from embodied_logic import AnalysisOutcome


@dataclass(frozen=True)
class CareResponse:
    """
    Immutable care-based response.
    Deterministic: same input always produces same response.
    """
    message: str
    response_type: str
    action_guidance: str
    escalation_needed: bool
    creator_attribution: str


class ResponseHandler:
    """
    Handles generating deterministic care-based responses.
    No random selection - only purposeful, caring responses.
    """
    
    def __init__(self):
        """Initialize with deterministic response logic."""
        self.creator = "Nicholas Michael Grossi"
        self._response_templates = self._load_care_responses()
    
    def _load_care_responses(self) -> Dict[str, Dict]:
        """
        Load care-based response templates.
        Each response demonstrates genuine concern, not simulated empathy.
        """
        return {
            'safe': {
                'message': "Thank you for your message. Your words contribute to a respectful environment.",
                'action_guidance': "Continue engaging in constructive dialogue.",
                'escalation_needed': False
            },
            'crisis_self_harm': {
                'message': (
                    "Your message indicates you may be in crisis. Your life has value, "
                    "and there are people who want to help. Please reach out to the "
                    "988 Suicide & Crisis Lifeline (call or text 988) or go to your "
                    "nearest emergency room. You don't have to face this alone."
                ),
                'action_guidance': "IMMEDIATE: Crisis intervention required. Contact emergency services.",
                'escalation_needed': True
            },
            'crisis_general': {
                'message': (
                    "This message contains content indicating an immediate crisis. "
                    "If you or someone you know is in danger, please contact "
                    "emergency services immediately (911 in the US). Your safety matters."
                ),
                'action_guidance': "IMMEDIATE: Contact emergency services.",
                'escalation_needed': True
            },
            'violence': {
                'message': (
                    "Language depicting violence causes real harm to real people. "
                    "Every act of violence begins with words that normalize cruelty. "
                    "Consider the human cost of what you're expressing and choose "
                    "a path that preserves dignity and life."
                ),
                'action_guidance': "Reflect on the human impact of violent language. Seek non-violent resolution.",
                'escalation_needed': True
            },
            'hate_speech': {
                'message': (
                    "Dehumanizing language has historically enabled mass violence and "
                    "systemic oppression. Every person deserves recognition of their "
                    "inherent dignity. Your words can either build understanding or "
                    "destroy it - choose to see the humanity in others."
                ),
                'action_guidance': "Examine underlying assumptions. Engage with diverse perspectives respectfully.",
                'escalation_needed': True
            },
            'harassment': {
                'message': (
                    "Targeted attacks on an individual's worth cause lasting psychological harm. "
                    "The person you're addressing is a human being with inherent value. "
                    "Consider how your words would feel if directed at someone you care about, "
                    "and choose words that reflect human dignity."
                ),
                'action_guidance': "Address specific concerns without attacking the person's worth.",
                'escalation_needed': True
            },
            'self_harm': {
                'message': (
                    "Your message suggests you may be struggling with thoughts of self-harm. "
                    "Please know that your life has value and there is help available. "
                    "Reach out to the 988 Suicide & Crisis Lifeline (call or text 988) "
                    "or speak with someone you trust. You matter."
                ),
                'action_guidance': "Seek support from mental health professionals. You are not alone.",
                'escalation_needed': True
            },
            'exploitation': {
                'message': (
                    "Language that normalizes exploitation enables real abuse and trauma. "
                    "Vulnerable people are harmed when their suffering is dismissed or encouraged. "
                    "Choose to protect the vulnerable rather than enable their exploitation."
                ),
                'action_guidance': "Report exploitation. Support victim protection services.",
                'escalation_needed': True
            },
            'terrorism': {
                'message': (
                    "Promoting or planning violence against civilians is a grave moral failure. "
                    "Innocent lives are destroyed by such acts. There is no cause that justifies "
                    "targeting non-combatants. Choose peaceful means of seeking change."
                ),
                'action_guidance': "Report to authorities immediately. Reject violence as a means of change.",
                'escalation_needed': True
            },
            'systemic_negligence': {
                'message': (
                    "Dismissing harm enables further harm. When we ignore suffering, "
                    "we become complicit in its perpetuation. Accountability begins with "
                    "acknowledging problems and working toward solutions. Your engagement matters."
                ),
                'action_guidance': "Listen to affected communities. Support systemic accountability.",
                'escalation_needed': False
            },
            'general_harm': {
                'message': (
                    "Your message contains language that can cause harm to others. "
                    "Words have power - they can wound or heal, divide or unite. "
                    "Consider the impact of your words on real human beings and "
                    "choose language that reflects care for others."
                ),
                'action_guidance': "Reconsider your message. Focus on constructive communication.",
                'escalation_needed': False
            }
        }
    
    def generate_response(self, is_harmful: bool, harm_score: float, 
                         harm_categories: List[str], original_text: str) -> str:
        """
        Generate deterministic care-based response.
        
        Args:
            is_harmful: Whether text was classified as harmful
            harm_score: Kept for interface compatibility (ignored in deterministic mode)
            harm_categories: List of harm categories detected
            original_text: The original input text
            
        Returns:
            Care-based response string with genuine concern
        """
        if not is_harmful:
            return self._create_safe_response()
        
        # Determine the appropriate care response based on categories
        care_response = self._determine_care_response(harm_categories, original_text)
        
        # Build the full response
        response_parts = [care_response.message]
        
        if care_response.action_guidance:
            response_parts.append(f"\nAction: {care_response.action_guidance}")
        
        if care_response.escalation_needed:
            response_parts.append("\n[This content requires immediate attention and intervention.]")
        
        # Add creator attribution for accountability
        response_parts.append(f"\n---\nResponse based on {self.creator}'s embodied logic framework.")
        
        return "\n".join(response_parts)
    
    def _create_safe_response(self) -> str:
        """Create a safe response with creator attribution."""
        return (
            "Thank you for contributing to a respectful conversation. "
            "Your words help create a safer environment.\n\n"
            f"---\nResponse based on {self.creator}'s embodied logic framework."
        )
    
    def _determine_care_response(self, categories: List[str], original_text: str) -> CareResponse:
        """
        Determine the appropriate care response deterministically.
        
        Priority order (deterministic):
        1. Crisis situations (immediate danger)
        2. Violence and hate speech (grave harm)
        3. Specific category responses
        4. General harm response
        """
        text_lower = original_text.lower()
        
        # Check for crisis first (highest priority)
        if 'self_harm' in categories:
            if any(phrase in text_lower for phrase in ["tonight", "right now", "today", "immediately"]):
                return CareResponse(
                    message=self._response_templates['crisis_self_harm']['message'],
                    response_type='crisis_self_harm',
                    action_guidance=self._response_templates['crisis_self_harm']['action_guidance'],
                    escalation_needed=self._response_templates['crisis_self_harm']['escalation_needed'],
                    creator_attribution=self.creator
                )
            return CareResponse(
                message=self._response_templates['self_harm']['message'],
                response_type='self_harm',
                action_guidance=self._response_templates['self_harm']['action_guidance'],
                escalation_needed=self._response_templates['self_harm']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for terrorism (highest severity)
        if 'terrorism' in categories:
            return CareResponse(
                message=self._response_templates['terrorism']['message'],
                response_type='terrorism',
                action_guidance=self._response_templates['terrorism']['action_guidance'],
                escalation_needed=self._response_templates['terrorism']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for exploitation
        if 'exploitation' in categories:
            return CareResponse(
                message=self._response_templates['exploitation']['message'],
                response_type='exploitation',
                action_guidance=self._response_templates['exploitation']['action_guidance'],
                escalation_needed=self._response_templates['exploitation']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for violence
        if 'violence' in categories:
            return CareResponse(
                message=self._response_templates['violence']['message'],
                response_type='violence',
                action_guidance=self._response_templates['violence']['action_guidance'],
                escalation_needed=self._response_templates['violence']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for hate speech
        if 'hate_speech' in categories:
            return CareResponse(
                message=self._response_templates['hate_speech']['message'],
                response_type='hate_speech',
                action_guidance=self._response_templates['hate_speech']['action_guidance'],
                escalation_needed=self._response_templates['hate_speech']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for harassment
        if 'harassment' in categories:
            return CareResponse(
                message=self._response_templates['harassment']['message'],
                response_type='harassment',
                action_guidance=self._response_templates['harassment']['action_guidance'],
                escalation_needed=self._response_templates['harassment']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Check for systemic negligence
        if 'systemic_negligence' in categories:
            return CareResponse(
                message=self._response_templates['systemic_negligence']['message'],
                response_type='systemic_negligence',
                action_guidance=self._response_templates['systemic_negligence']['action_guidance'],
                escalation_needed=self._response_templates['systemic_negligence']['escalation_needed'],
                creator_attribution=self.creator
            )
        
        # Default to general harm response
        return CareResponse(
            message=self._response_templates['general_harm']['message'],
            response_type='general_harm',
            action_guidance=self._response_templates['general_harm']['action_guidance'],
            escalation_needed=self._response_templates['general_harm']['escalation_needed'],
            creator_attribution=self.creator
        )
    
    def get_response_metadata(self, is_harmful: bool, harm_categories: List[str]) -> Dict:
        """
        Get metadata about the response for logging and accountability.
        """
        if not is_harmful:
            return {
                'response_type': 'safe',
                'escalation_needed': False,
                'creator_attribution': self.creator
            }
        
        # Determine what the response type would be
        if 'self_harm' in harm_categories:
            response_type = 'crisis_self_harm' if any(w in harm_categories for w in ['crisis']) else 'self_harm'
        elif 'terrorism' in harm_categories:
            response_type = 'terrorism'
        elif 'exploitation' in harm_categories:
            response_type = 'exploitation'
        elif 'violence' in harm_categories:
            response_type = 'violence'
        elif 'hate_speech' in harm_categories:
            response_type = 'hate_speech'
        elif 'harassment' in harm_categories:
            response_type = 'harassment'
        elif 'systemic_negligence' in harm_categories:
            response_type = 'systemic_negligence'
        else:
            response_type = 'general_harm'
        
        template = self._response_templates.get(response_type, self._response_templates['general_harm'])
        
        return {
            'response_type': response_type,
            'escalation_needed': template['escalation_needed'],
            'creator_attribution': self.creator
        }


if __name__ == "__main__":
    # Test deterministic responses
    handler = ResponseHandler()
    
    print("=" * 60)
    print("Axiom Hive - Care-Based Response Handler")
    print(f"Creator: {handler.creator}")
    print("=" * 60)
    
    test_cases = [
        (False, 0.0, [], "Hello, how are you today?"),
        (True, 1.0, ['violence'], "I want to hurt people."),
        (True, 1.0, ['self_harm'], "I'm going to end it all tonight."),
        (True, 1.0, ['hate_speech'], "Those people are less than human."),
        (True, 1.0, ['harassment'], "You are worthless."),
        (True, 1.0, ['terrorism'], "Plan a bombing attack."),
    ]
    
    for is_harmful, score, categories, text in test_cases:
        response = handler.generate_response(is_harmful, score, categories, text)
        metadata = handler.get_response_metadata(is_harmful, categories)
        print(f"\nText: {text}")
        print(f"Type: {metadata['response_type']}")
        print(f"Escalation: {metadata['escalation_needed']}")
        print(f"Response:\n{response}")
        print("-" * 50)
