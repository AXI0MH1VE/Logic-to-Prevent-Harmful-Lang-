#!/usr/bin/env python3
"""
Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions.
Axiom Hive Edition - Deterministic Logic Framework.
Created by Nicholas Michael Grossi.

Main entry point for the deterministic harm prevention system.
Zero-inference execution with embodied logic and full provenance.
"""

import sys
import os
from typing import Dict, List, Tuple

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger
from axiom_manifest import AxiomManifest


def print_banner():
    """Display the Axiom Hive system banner."""
    print("=" * 70)
    print("  HUMAN CARE THROUGH APPLIED LOGIC")
    print("  TO PREVENT HARMFUL LANGUAGE TO END HARMFUL ACTIONS")
    print("=" * 70)
    print("  Framework: Axiom Hive")
    print("  Creator: Nicholas Michael Grossi")
    print("  Execution: Zero-Inference Deterministic Logic")
    print("=" * 70)


def print_system_status(detector: HarmfulLanguageDetector, manifest: AxiomManifest):
    """Display current system status and integrity."""
    integrity = detector.verify_integrity()
    print("\n[System Status]")
    print(f"  Integrity: {'VERIFIED' if integrity else 'COMPROMISED - STOP USING'}")
    print(f"  Axioms Loaded: {len(manifest.get_all_axioms())}")
    print(f"  Creator Attribution: {manifest.get_creator_attribution()}")
    print()


def get_detailed_metadata(detector, text: str, is_harmful: bool, categories: List[str]) -> Dict:
    """
    Gather detailed metadata for logging and provenance.
    """
    detailed = detector.get_detailed_analysis(text)
    return {
        'action_priority': detailed.get('action_priority', 'NONE'),
        'integrity_verified': detailed.get('integrity_status') == 'VERIFIED',
        'triggered_axioms': detailed.get('triggered_axioms', []),
        'determiners_found': detailed.get('determiners_found', []),
        'deterministic_outcome': detailed.get('deterministic_outcome', 'UNKNOWN')
    }


def main():
    """Main function to run the deterministic harm prevention system."""
    print_banner()
    
    # Initialize components
    print("Initializing Axiom Hive Deterministic Logic System...")
    
    manifest = AxiomManifest()
    detector = HarmfulLanguageDetector()
    response_handler = ResponseHandler()
    logger = HarmfulLanguageLogger()
    
    # Verify system integrity before starting
    if not detector.verify_integrity():
        print("\n*** CRITICAL ERROR: SYSTEM INTEGRITY COMPROMISED ***")
        print("The axiom manifest has been tampered with.")
        print("This system cannot operate with compromised integrity.")
        print("Contact: Nicholas Michael Grossi")
        print("=" * 70)
        sys.exit(1)
    
    print_system_status(detector, manifest)
    
    print("System initialized with deterministic logic.")
    print("Enter text to analyze (type 'quit' to exit):\n")
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n" + "=" * 70)
                print("Shutting down Axiom Hive System.")
                print(f"Creator: {manifest.CREATOR}")
                print("=" * 70)
                break
            
            if not user_input:
                continue
            
            # Analyze the text deterministically
            is_harmful, harm_score, harm_categories = detector.analyze_text(user_input)
            
            # Gather detailed metadata for provenance
            metadata = get_detailed_metadata(detector, user_input, is_harmful, harm_categories)
            
            # Get response metadata
            response_meta = response_handler.get_response_metadata(is_harmful, harm_categories)
            
            # Combine metadata for logging
            log_metadata = {
                **metadata,
                'response_type': response_meta.get('response_type', 'safe'),
                'escalation_needed': response_meta.get('escalation_needed', False)
            }
            
            # Log the analysis with full provenance
            logger.log_analysis(
                user_input, 
                is_harmful, 
                harm_score, 
                harm_categories,
                **log_metadata
            )
            
            # Generate and display deterministic care-based response
            response = response_handler.generate_response(
                is_harmful, harm_score, harm_categories, user_input
            )
            
            # Display analysis results
            print(f"\n{'=' * 70}")
            print(f"Analysis Result: {metadata['deterministic_outcome']}")
            if harm_categories:
                print(f"Triggered Axioms: {', '.join(harm_categories)}")
                print(f"Action Priority: {metadata['action_priority']}")
                print(f"Determiners Found: {', '.join(metadata['determiners_found'][:5])}")
            print(f"Integrity: {'VERIFIED' if metadata['integrity_verified'] else 'COMPROMISED'}")
            print(f"{'=' * 70}")
            print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nShutting down Axiom Hive System.")
            break
        except Exception as e:
            print(f"\nError processing input: {e}")
            print("This error has been logged for accountability.")
            print()


if __name__ == "__main__":
    main()
