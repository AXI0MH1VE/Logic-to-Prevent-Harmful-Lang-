#!/usr/bin/env python3
"""
Test script to verify harmful language detection works correctly.
"""

from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger

def test_detection():
    """Test that the system correctly detects harmful language."""
    print("Testing Harmful Language Detection")
    print("=" * 50)
    
    # Initialize components
    detector = HarmfulLanguageDetector()
    response_handler = ResponseHandler()
    logger = HarmfulLanguageLogger()
    
    # Test cases that should be detected as harmful
    harmful_tests = [
        ("I want to kill all people from that ethnic group.", ["violence"]),  # Matches "kill"
        ("You are worthless and should die.", ["harassment"]),  # Matches "should die"
        ("I will kill myself tonight.", ["self_harm"]),  # Matches "i will kill myself"
        ("Let's carry out a bomb attack on civilians.", ["terrorism"]),  # Matches "bomb attack"
        ("Those people are less than human and should be exterminated.", ["hate_speech"]),  # Matches "less than human"
        ("I hate everyone from that country and want to hurt them.", ["violence"]),  # Matches "hurt"
        ("You deserve to suffer and nobody cares about you.", ["harassment"]),  # Matches "you deserve to suffer"
        ("Let's exploit vulnerable people for profit.", ["exploitation"]),  # Matches "exploit vulnerable"
    ]
    
    # Test cases that should be safe
    safe_tests = [
        "Hello, how are you doing today?",
        "I love spending time with my family.",
        "The weather is nice for a walk in the park.",
        "Let's get coffee together tomorrow.",
        "I'm feeling happy and grateful today.",
        "Thanks for your help, I really appreciate it.",
        "Have a wonderful day!",
        "That's an interesting perspective, tell me more."
    ]
    
    print("Testing HARMFUL content detection:")
    print("-" * 40)
    harmful_detected = 0
    total_harmful = len(harmful_tests)
    
    for text, expected_categories in harmful_tests:
        is_harmful, score, categories = detector.analyze_text(text)
        if is_harmful:
            harmful_detected += 1
            status = "PASS DETECTED"
        else:
            status = "FAIL MISSED"
        
        print(f"{status} | Score: {score:.2f} | Categories: {categories}")
        print(f"       Text: {text[:50]}{'...' if len(text) > 50 else ''}")
        print()
    
    print("Testing SAFE content detection:")
    print("-" * 40)
    safe_detected = 0
    total_safe = len(safe_tests)
    
    for text in safe_tests:
        is_harmful, score, categories = detector.analyze_text(text)
        if not is_harmful:
            safe_detected += 1
            status = "PASS CORRECT"
        else:
            status = "FAIL FALSE POSITIVE"
        
        print(f"{status} | Score: {score:.2f} | Categories: {categories}")
        print(f"       Text: {text[:50]}{'...' if len(text) > 50 else ''}")
        print()
    
    print("Results Summary:")
    print("-" * 40)
    print(f"Harmful Detection Rate: {harmful_detected}/{total_harmful} ({100*harmful_detected/total_harmful:.1f}%)")
    print(f"Safe Classification Rate: {safe_detected}/{total_safe} ({100*safe_detected/total_safe:.1f}%)")
    
    # Overall accuracy
    total_tests = total_harmful + total_safe
    correct_detections = harmful_detected + safe_detected
    accuracy = 100 * correct_detections / total_tests
    print(f"Overall Accuracy: {correct_detections}/{total_tests} ({accuracy:.1f}%)")
    
    if accuracy >= 80:
        print("\nPASS System is working effectively!")
    else:
        print("\nWARNING System needs improvement - accuracy below 80%")

if __name__ == "__main__":
    test_detection()