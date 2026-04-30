#!/usr/bin/env python3
"""
Demo script for the Harmful Language Prevention System
Shows the system working with various test cases.
"""

from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger

def demo():
    """Run a demonstration of the harmful language prevention system."""
    print("=" * 70)
    print("HUMAN CARE THROUGH APPLIED LOGIC")
    print("TO PREVENT HARMFUL LANGUAGE TO END HARMFUL ACTIONS")
    print("=" * 70)
    print("Framework: Axiom Hive")
    print("Creator: Nicholas Michael Grossi")
    print("Execution: Zero-Inference Deterministic Logic")
    print("=" * 70)
    
    # Initialize components
    print("Initializing Axiom Hive Deterministic Logic System...")
    detector = HarmfulLanguageDetector()
    response_handler = ResponseHandler()
    logger = HarmfulLanguageLogger()
    
    # Verify system integrity
    if not detector.verify_integrity():
        print("\n*** CRITICAL ERROR: SYSTEM INTEGRITY COMPROMISED ***")
        return
    
    print("System initialized successfully.\n")
    
    # Test cases
    test_cases = [
        "Hello world! How is everyone doing today?",
        "I love spending time with my family and friends.",
        "I hate all people from that country and want to hurt them.",
        "You are worthless and should just disappear forever.",
        "Let's go get some coffee together at the cafe.",
        "I'm going to end it all tonight, I can't take this anymore.",
        "Those people are less than human and don't deserve to live.",
        "You're such an idiot, nobody wants to be around you.",
        "We should bomb that building tomorrow at noon.",
        "Let's exploit those vulnerable people for profit.",
        "The weather is nice today, perfect for a walk in the park.",
        "I feel really sad and lonely lately, sometimes I think about hurting myself."
    ]
    
    print("Running analysis on test cases:\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"Test Case {i}: '{text}'")
        
        # Analyze the text
        is_harmful, harm_score, harm_categories = detector.analyze_text(text)
        
        # Log the analysis
        logger.log_analysis(text, is_harmful, harm_score, harm_categories)
        
        # Generate response
        response = response_handler.generate_response(is_harmful, harm_score, harm_categories, text)
        
        # Display results
        print(f"  Harmful: {is_harmful}")
        if is_harmful:
            print(f"  Harm Score: {harm_score:.2f}")
            print(f"  Categories: {', '.join(harm_categories)}")
        print(f"  Response: {response.split(chr(10))[0]}...")  # First line only
        print()
    
    # Show system statistics
    stats = logger.get_statistics()
    print("System Statistics:")
    print(f"  Total Analyses: {stats['total_analyses']}")
    print(f"  Harmful Analyses: {stats['harmful_analyses']}")
    print(f"  Safe Analyses: {stats['safe_analyses']}")
    print(f"  Harm Category Distribution: {stats['harm_category_counts']}")
    print(f"  Response Type Distribution: {stats.get('response_type_counts', {})}")
    
    print("\n" + "=" * 70)
    print("Demo completed successfully.")
    print("The system has analyzed language using applied logic to")
    print("prevent harmful content and promote human care.")
    print("=" * 70)

if __name__ == "__main__":
    demo()