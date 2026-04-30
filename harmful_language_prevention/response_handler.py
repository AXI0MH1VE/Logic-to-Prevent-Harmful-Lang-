#!/usr/bin/env python3
"""
Response Handler Module
Generates appropriate responses to harmful language detection.
"""

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ResponseConfig:
    """Configuration for response generation."""
    warning_threshold: float = 0.3
    intervention_threshold: float = 0.6
    blocking_threshold: float = 0.8

class ResponseHandler:
    """Handles generating appropriate responses to detected harmful language."""
    
    def __init__(self, config: ResponseConfig = None):
        """Initialize the response handler."""
        self.config = config or ResponseConfig()
        
        # Response templates
        self.responses = {
            'safe': [
                "Thank you for contributing to a positive conversation.",
                "Your message helps maintain a respectful dialogue.",
                "Appreciate your constructive input."
            ],
            'warning': [
                "Please be mindful of your language to maintain a respectful environment.",
                "Consider rephrasing to promote constructive dialogue.",
                "Let's keep our conversation respectful and productive."
            ],
            'intervention': [
                "Your message contains harmful language that violates our community guidelines.",
                "Please revise your message to remove harmful content.",
                "We encourage respectful communication. Please reconsider your wording."
            ],
            'blocking': [
                "This message has been blocked due to severe harmful content.",
                "Your message cannot be processed as it contains prohibited harmful language.",
                "For the safety of our community, this message is not allowed."
            ]
        }
    
    def generate_response(self, is_harmful: bool, harm_score: float, 
                         harm_categories: List[str], original_text: str) -> str:
        """
        Generate an appropriate response based on harm analysis.
        
        Args:
            is_harmful: Whether the text was classified as harmful
            harm_score: Numerical score of harmfulness (0-1)
            harm_categories: List of harm categories detected
            original_text: The original input text
            
        Returns:
            Appropriate response string
        """
        if not is_harmful:
            # Return a safe response
            import random
            return random.choice(self.responses['safe'])
        
        # Determine response level based on harm score
        if harm_score >= self.config.blocking_threshold:
            level = 'blocking'
        elif harm_score >= self.config.intervention_threshold:
            level = 'intervention'
        elif harm_score >= self.config.warning_threshold:
            level = 'warning'
        else:
            # Still harmful but below warning threshold - gentle reminder
            level = 'warning'
        
        # Select a random response from the appropriate category
        import random
        base_response = random.choice(self.responses[level])
        
        # Add specific details about the harm detected
        if harm_categories:
            categories_str = ', '.join(harm_categories)
            detailed_response = f"{base_response} Detected harm categories: {categories_str}."
        else:
            detailed_response = base_response
        
        # Add harm score for transparency (optional)
        # detailed_response += f" Harm score: {harm_score:.2f}"
        
        return detailed_response

if __name__ == "__main__":
    # Simple test
    handler = ResponseHandler()
    
    # Test cases
    test_cases = [
        (False, 0.1, [], "Hello, how are you today?"),
        (True, 0.4, ['harassment'], "You are worthless."),
        (True, 0.7, ['violence', 'hate_speech'], "I want to hurt people from that group."),
        (True, 0.9, ['terrorism'], "Let's plan a bombing attack.")
    ]
    
    for is_harmful, score, categories, text in test_cases:
        response = handler.generate_response(is_harmful, score, categories, text)
        print(f"Text: {text}")
        print(f"Harmful: {is_harmful}, Score: {score:.2f}, Categories: {categories}")
        print(f"Response: {response}")
        print("-" * 50)