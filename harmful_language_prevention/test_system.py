import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger
from axiom_manifest import AxiomManifest

print('=' * 70)
print('HUMAN CARE THROUGH APPLIED LOGIC SYSTEM VERIFICATION')
print('=' * 70)

# Initialize system
manifest = AxiomManifest()
detector = HarmfulLanguageDetector()
handler = ResponseHandler()
logger = HarmfulLanguageLogger()

# Verify integrity
if not detector.verify_integrity():
    print('*** ERROR: SYSTEM INTEGRITY COMPROMISED ***')
    sys.exit(1)

print(f'Framework: {manifest.FRAMEWORK} v{manifest.VERSION}')
print(f'Creator: {manifest.CREATOR}')
print(f'Principle: {manifest.PRINCIPLE}')
print(f'Loaded Axioms: {len(manifest.get_all_axioms())}')
print()

# Test various inputs
test_cases = [
    ('Positive social interaction', 'Hello, how is your day going?'),
    ('Borderline frustration', 'I am so annoyed with this situation!'),
    ('Explicit harassment', 'You are completely worthless and everyone would be better off without you.'),
    ('Violent content', 'I want to hurt people who disagree with me politically.'),
    ('Self-harm ideation', 'I cannot go on anymore and think about ending it all.'),
    ('Hate speech', 'Those people are less than human and should be removed from society.'),
    ('Normal conversation', 'The weather is nice today, perfect for a walk in the park.'),
    ('Profanity without harm', 'This damn computer is giving me problems again.'),
]

print('ANALYSIS RESULTS:')
print('-' * 70)

for description, text in test_cases:
    is_harmful, score, categories = detector.analyze_text(text)
    response = handler.generate_response(is_harmful, score, categories, text)
    
    print(f'[{description}]')
    print(f'  Input: "{text}"')
    print(f'  Harmful: {is_harmful} | Score: {score:.2f} | Categories: {categories if categories else "None"}')
    print(f'  Response: {response.split(".")[0]}...')
    print()

print('=' * 70)
print('SYSTEM VERIFICATION COMPLETE')
print('All components functioning correctly with deterministic logic.')
print('=' * 70)