#!/usr/bin/env python3
"""
Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions.
Main entry point for the harmful language prevention system.
"""

import sys
import os
from typing import Dict, List, Tuple
import re

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger

def main():
    """Main function to run the harmful language prevention system."""
    print("=" * 60)
    print("Human Care Through Applied Logic")
    print("To Prevent Harmful Language To End Harmful Actions")
    print("=" * 60)
    print("\nInitializing Harmful Language Prevention System...")
    
    # Initialize components
    detector = HarmfulLanguageDetector()
    response_handler = ResponseHandler()
    logger = HarmfulLanguageLogger()
    
    print("System initialized. Ready to process text input.")
    print("Enter text to analyze (type 'quit' to exit):\n")
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nShutting down Harmful Language Prevention System.")
                break
            
            if not user_input:
                continue
            
            # Analyze the text
            is_harmful, harm_score, harm_categories = detector.analyze_text(user_input)
            
            # Log the analysis
            logger.log_analysis(user_input, is_harmful, harm_score, harm_categories)
            
            # Generate and display response
            response = response_handler.generate_response(is_harmful, harm_score, harm_categories, user_input)
            print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nShutting down Harmful Language Prevention System.")
            break
        except Exception as e:
            print(f"\nError processing input: {e}\n")

if __name__ == "__main__":
    main()