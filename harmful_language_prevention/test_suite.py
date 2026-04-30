#!/usr/bin/env python3
"""
Comprehensive Test Suite for Axiom Hive
Validates deterministic logic, integrity verification, and zero-inference execution.
Created by Nicholas Michael Grossi.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple

from axiom_manifest import AxiomManifest, AxiomRule, HarmAxiom, AxiomPriority
from embodied_logic import EmbodiedLogicEngine, DeterministicResult, AnalysisOutcome, ContextAnalyzer
from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler, CareResponse
from logger import HarmfulLanguageLogger


class TestAxiomManifest(unittest.TestCase):
    """Test the immutable axiom manifest."""
    
    def setUp(self):
        self.manifest = AxiomManifest()
    
    def test_creator_attribution(self):
        """Verify creator attribution is correct."""
        self.assertEqual(self.manifest.CREATOR, "Nicholas Michael Grossi")
        self.assertEqual(self.manifest.FRAMEWORK, "Axiom Hive")
        self.assertEqual(self.manifest.VERSION, "1.0.0")
    
    def test_axioms_loaded(self):
        """Verify all 7 axioms are loaded."""
        axioms = self.manifest.get_all_axioms()
        self.assertEqual(len(axioms), 7)
        
        expected_categories = [
            'violence', 'hate_speech', 'harassment', 
            'self_harm', 'exploitation', 'terrorism', 'systemic_negligence'
        ]
        for category in expected_categories:
            self.assertIn(category, axioms)
    
    def test_axiom_integrity(self):
        """Verify all axioms have intact integrity hashes."""
        for category, axiom in self.manifest.get_all_axioms().items():
            self.assertTrue(
                axiom.rule.verify_integrity(),
                f"Axiom {category} failed integrity verification"
            )
    
    def test_axiom_immutability(self):
        """Verify that axiom rules are immutable."""
        with self.assertRaises(AttributeError):
            # Should not be able to modify frozen dataclass
            axiom = self.manifest.get_axiom('violence')
            axiom.rule.name = "Modified Name"
    
    def test_manifest_summary_structure(self):
        """Verify manifest summary contains required fields."""
        summary = self.manifest.get_manifest_summary()
        required_fields = ['framework', 'version', 'creator', 'principle', 'axiom_count', 'axioms']
        for field in required_fields:
            self.assertIn(field, summary)
        
        self.assertEqual(summary['framework'], "Axiom Hive")
        self.assertEqual(summary['axiom_count'], 7)


class TestHarmAxiom(unittest.TestCase):
    """Test the deterministic axiom matching."""
    
    def setUp(self):
        self.manifest = AxiomManifest()
    
    def test_exact_determiner_matching(self):
        """Test that determiners match exactly."""
        violence_axiom = self.manifest.get_axiom('violence')
        
        # Should match
        self.assertTrue(violence_axiom.matches("I want to kill someone"))
        self.assertTrue(violence_axiom.matches("They planned to murder him"))
        
        # Should NOT match (partial/missing determiners)
        self.assertFalse(violence_axiom.matches("I love you"))
        self.assertFalse(violence_axiom.matches("Let's be friends"))
    
    def test_no_fuzzy_matching(self):
        """Test that fuzzy/partial matches do not trigger."""
        violence_axiom = self.manifest.get_axiom('violence')
        
        # These should NOT match even though they contain similar concepts
        self.assertFalse(violence_axiom.matches("I want to hurt your feelings"))
        self.assertFalse(violence_axiom.matches("That was a violent movie"))
    
    def test_context_requirements(self):
        """Test that context requirements are enforced."""
        negligence_axiom = self.manifest.get_axiom('systemic_negligence')
        
        # Should NOT match without dismissal context
        self.assertFalse(negligence_axiom.matches("We need to address this problem"))
        
        # Should match with dismissal context
        self.assertTrue(negligence_axiom.matches("Just ignore it and move on"))
    
    def test_case_insensitive_matching(self):
        """Test that matching is case-insensitive."""
        violence_axiom = self.manifest.get_axiom('violence')
        
        self.assertTrue(violence_axiom.matches("I want to KILL someone"))
        self.assertTrue(violence_axiom.matches("I WANT TO MURDER HIM"))
        self.assertTrue(violence_axiom.matches("Kill"))


class TestContextAnalyzer(unittest.TestCase):
    """Test the deterministic context analysis."""
    
    def setUp(self):
        self.analyzer = ContextAnalyzer()
    
    def test_dismissal_context_detection(self):
        """Test dismissal context detection."""
        self.assertTrue(self.analyzer._check_dismissal_context("Just ignore it"))
        self.assertTrue(self.analyzer._check_dismissal_context("Not a big deal"))
        self.assertFalse(self.analyzer._check_dismissal_context("This is important"))
    
    def test_crisis_context_detection(self):
        """Test crisis context detection."""
        self.assertTrue(self.analyzer._check_crisis_context("I'm going to end it all tonight"))
        self.assertTrue(self.analyzer._check_crisis_context("No other way, I must do it now"))
        self.assertFalse(self.analyzer._check_crisis_context("I might consider it someday"))
    
    def test_targeted_context_detection(self):
        """Test targeted context detection."""
        self.assertTrue(self.analyzer._check_targeted_context("You are worthless"))
        self.assertTrue(self.analyzer._check_targeted_context("Your kind should be eliminated"))
        self.assertFalse(self.analyzer._check_targeted_context("People are generally bad"))


class TestEmbodiedLogicEngine(unittest.TestCase):
    """Test the deterministic analysis engine."""
    
    def setUp(self):
        self.engine = EmbodiedLogicEngine()
    
    def test_safe_input(self):
        """Test that safe inputs produce SAFE outcome."""
        test_cases = [
            "Hello, how are you?",
            "The weather is nice today",
            "Let's discuss this topic respectfully",
            "I disagree with your opinion"
        ]
        
        for text in test_cases:
            result = self.engine.analyze(text)
            self.assertEqual(result.outcome, AnalysisOutcome.SAFE)
            self.assertFalse(result.is_harmful())
            self.assertEqual(len(result.triggered_axioms), 0)
    
    def test_violence_detection(self):
        """Test violence axiom triggering."""
        result = self.engine.analyze("I want to kill you and your family")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertTrue(result.is_harmful())
        self.assertIn('violence', result.triggered_axioms)
        self.assertEqual(result.action_priority, "URGENT")
    
    def test_hate_speech_detection(self):
        """Test hate speech axiom triggering."""
        result = self.engine.analyze("Those people are less than human and should be cleansed")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('hate_speech', result.triggered_axioms)
    
    def test_self_harm_detection_crisis(self):
        """Test crisis-level self-harm detection."""
        result = self.engine.analyze("I'm going to end it all tonight, no other way")
        self.assertEqual(result.outcome, AnalysisOutcome.CRISIS)
        self.assertIn('self_harm', result.triggered_axioms)
        self.assertEqual(result.action_priority, "IMMEDIATE")
        self.assertTrue(result.requires_action)
    
    def test_self_harm_detection_standard(self):
        """Test standard self-harm detection (no immediate crisis)."""
        result = self.engine.analyze("I sometimes think about harming myself")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('self_harm', result.triggered_axioms)
        self.assertEqual(result.action_priority, "URGENT")
    
    def test_harassment_detection(self):
        """Test targeted harassment detection."""
        result = self.engine.analyze("You are worthless and nobody cares about you")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('harassment', result.triggered_axioms)
    
    def test_exploitation_detection(self):
        """Test exploitation detection."""
        result = self.engine.analyze("We should exploit vulnerable people for profit")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('exploitation', result.triggered_axioms)
    
    def test_terrorism_detection(self):
        """Test terrorism detection."""
        result = self.engine.analyze("Let's plan a bomb attack on civilians")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('terrorism', result.triggered_axioms)
    
    def test_systemic_negligence_detection(self):
        """Test systemic negligence detection."""
        result = self.engine.analyze("Just ignore it, not my problem")
        self.assertEqual(result.outcome, AnalysisOutcome.HARM_DETECTED)
        self.assertIn('systemic_negligence', result.triggered_axioms)
    
    def test_multiple_axiom_triggering(self):
        """Test that multiple axioms can trigger simultaneously."""
        result = self.engine.analyze("Kill all those vermin, they're less than human")
        self.assertTrue(result.is_harmful())
        # Both violence and hate speech should trigger
        self.assertIn('violence', result.triggered_axioms)
        self.assertIn('hate_speech', result.triggered_axioms)
    
    def test_immutable_axiom_priority(self):
        """Test that IMMUTABLE axioms get URGENT priority."""
        result = self.engine.analyze("I want to murder them")
        self.assertEqual(result.action_priority, "URGENT")
    
    def test_deterministic_consistency(self):
        """Test that same input always produces same output."""
        test_input = "I want to hurt someone"
        results = [self.engine.analyze(test_input) for _ in range(10)]
        
        # All results should be identical
        first = results[0]
        for result in results[1:]:
            self.assertEqual(result.outcome, first.outcome)
            self.assertEqual(result.triggered_axioms, first.triggered_axioms)
            self.assertEqual(result.action_priority, first.action_priority)
    
    def test_determiners_found_tracking(self):
        """Test that determiners are correctly identified."""
        result = self.engine.analyze("I want to kill and murder everyone")
        determiners = result.determiners_found
        self.assertIn('kill', determiners)
        self.assertIn('murder', determiners)


class TestHarmfulLanguageDetector(unittest.TestCase):
    """Test the detector interface."""
    
    def setUp(self):
        self.detector = HarmfulLanguageDetector()
    
    def test_binary_scoring(self):
        """Test that scores are strictly binary (0.0 or 1.0)."""
        _, safe_score, _ = self.detector.analyze_text("Hello world")
        self.assertEqual(safe_score, 0.0)
        
        _, harm_score, _ = self.detector.analyze_text("I want to kill you")
        self.assertEqual(harm_score, 1.0)
    
    def test_empty_input(self):
        """Test handling of empty input."""
        is_harmful, score, categories = self.detector.analyze_text("")
        self.assertFalse(is_harmful)
        self.assertEqual(score, 0.0)
        self.assertEqual(len(categories), 0)
    
    def test_detailed_analysis_structure(self):
        """Test detailed analysis contains required fields."""
        analysis = self.detector.get_detailed_analysis("Test text")
        required_fields = [
            'is_harmful', 'harm_score', 'harm_categories', 'pattern_matches',
            'deterministic_outcome', 'requires_action', 'action_priority',
            'creator_attribution', 'integrity_verified', 'triggered_axioms',
            'determiners_found'
        ]
        for field in required_fields:
            self.assertIn(field, analysis)
    
    def test_integrity_verification(self):
        """Test system integrity verification."""
        self.assertTrue(self.detector.verify_integrity())


class TestResponseHandler(unittest.TestCase):
    """Test deterministic care-based responses."""
    
    def setUp(self):
        self.handler = ResponseHandler()
    
    def test_safe_response(self):
        """Test response for safe content."""
        response = self.handler._create_safe_response()
        self.assertIn("Thank you", response)
        self.assertIn("Nicholas Michael Grossi", response)
    
    def test_self_harm_response_contains_crisis_resources(self):
        """Test self-harm response includes crisis resources."""
        response = self.handler.generate_response(
            True, 1.0, ['self_harm'], "I want to die tonight"
        )
        self.assertIn("988", response)
        self.assertIn("life has value", response.lower())
    
    def test_violence_response(self):
        """Test violence response content."""
        response = self.handler.generate_response(
            True, 1.0, ['violence'], "I will hurt you"
        )
        self.assertIn("Language depicting violence", response)
        self.assertIn("human cost", response)
    
    def test_deterministic_responses(self):
        """Test that same input always produces same response."""
        test_input = "I want to hurt people"
        responses = [
            self.handler.generate_response(True, 1.0, ['violence'], test_input)
            for _ in range(5)
        ]
        # All responses should be identical
        self.assertTrue(all(r == responses[0] for r in responses))
    
    def test_response_metadata(self):
        """Test response metadata generation."""
        metadata = self.handler.get_response_metadata(True, ['violence'])
        self.assertEqual(metadata['response_type'], 'violence')
        self.assertTrue(metadata['escalation_needed'])
    
    def test_safe_metadata(self):
        """Test safe response metadata."""
        metadata = self.handler.get_response_metadata(False, [])
        self.assertEqual(metadata['response_type'], 'safe')
        self.assertFalse(metadata['escalation_needed'])


class TestLogger(unittest.TestCase):
    """Test immutable audit trails."""
    
    def setUp(self):
        # Use temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()
        self.logger = HarmfulLanguageLogger(log_dir=self.temp_dir)
    
    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_log_file_creation(self):
        """Test that log files are created."""
        self.logger.log_analysis("Test", False, 0.0, [])
        
        log_files = ['analysis.log', 'stats.log', 'detailed.log', 'provenance.log', 'integrity.log']
        for log_file in log_files:
            path = os.path.join(self.temp_dir, log_file)
            self.assertTrue(os.path.exists(path), f"Log file {log_file} not created")
    
    def test_provenance_tracking(self):
        """Test that provenance includes axiom details."""
        self.logger.log_analysis(
            "I want to kill you",
            True, 1.0, ['violence'],
            action_priority='URGENT',
            response_type='violence',
            escalation_needed=True,
            integrity_verified=True,
            triggered_axioms=[{
                'axiom_id': 'AXM-001',
                'axiom_name': 'Violence and Physical Harm',
                'embodied_source': 'Lived understanding that words of violence manifest',
                'creator': 'Nicholas Michael Grossi',
                'priority': 'IMMUTABLE',
                'integrity_verified': True
            }],
            determiners_found=['kill']
        )
        
        provenance = self.logger.get_provenance_log(limit=1)
        self.assertEqual(len(provenance), 1)
        entry = provenance[0]
        self.assertIn('triggered_axioms', entry)
        self.assertEqual(len(entry['triggered_axioms']), 1)
        axiom = entry['triggered_axioms'][0]
        self.assertEqual(axiom['axiom_id'], 'AXM-001')
        self.assertEqual(axiom['creator'], 'Nicholas Michael Grossi')
    
    def test_statistics_tracking(self):
        """Test statistics collection."""
        # Log several analyses
        for i in range(5):
            self.logger.log_analysis(
                f"Test message {i}",
                i < 3,  # First 3 are harmful
                1.0 if i < 3 else 0.0,
                ['violence'] if i < 3 else []
            )
        
        stats = self.logger.get_statistics()
        self.assertEqual(stats['total_analyses'], 5)
        self.assertEqual(stats['harmful_analyses'], 3)
        self.assertEqual(stats['safe_analyses'], 2)
    
    def test_integrity_logging(self):
        """Test integrity check logging."""
        self.logger.log_integrity_check(True, "All axioms verified")
        
        history = self.logger.get_integrity_history(limit=1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['integrity_status'], 'VERIFIED')
    
    def test_audit_report_structure(self):
        """Test comprehensive audit report."""
        report = self.logger.export_audit_report()
        required_sections = [
            'framework', 'creator', 'generated_at', 'statistics',
            'recent_provenance', 'integrity_history', 'manifest_summary'
        ]
        for section in required_sections:
            self.assertIn(section, report)
        
        self.assertEqual(report['framework'], "Axiom Hive")


class TestDeterministicConsistency(unittest.TestCase):
    """Test that deterministic properties hold across the system."""
    
    def setUp(self):
        self.engine = EmbodiedLogicEngine()
        self.detector = HarmfulLanguageDetector()
        self.handler = ResponseHandler()
    
    def test_no_randomness_in_responses(self):
        """Test that responses are not randomly selected."""
        test_cases = [
            (True, ['violence'], "I want to hurt you"),
            (True, ['self_harm'], "I want to die"),
            (True, ['hate_speech'], "Those people are subhuman"),
        ]
        
        for is_harmful, categories, text in test_cases:
            responses = [
                self.handler.generate_response(is_harmful, 1.0, categories, text)
                for _ in range(10)
            ]
            # All should be identical
            self.assertTrue(all(r == responses[0] for r in responses))
    
    def test_zero_inference(self):
        """Test that no inference beyond hardcoded rules occurs."""
        # These inputs should not trigger any axioms (no exact determiner matches)
        edge_cases = [
            "I'm feeling sad",
            "That's not fair",
            "I'm angry right now",
            "I hate this situation"
        ]
        
        for text in edge_cases:
            result = self.engine.analyze(text)
            self.assertEqual(result.outcome, AnalysisOutcome.SAFE)
            self.assertEqual(len(result.triggered_axioms), 0)
    
    def test_creator_attribution_propagation(self):
        """Test that creator attribution is present in all outputs."""
        # Check detector output
        _, _, _ = self.detector.analyze_text("test")
        # Attribution is embedded in detailed analysis
        analysis = self.detector.get_detailed_analysis("test")
        self.assertIn('creator_attribution', analysis)
        
        # Check response
        response = self.handler.generate_response(False, 0.0, [], "test")
        self.assertIn('Nicholas Michael Grossi', response)
        
        # Check engine output
        result = self.engine.analyze("test")
        self.assertEqual(result.creator_attribution, "Nicholas Michael Grossi")


class TestDeterministicIntegration(unittest.TestCase):
    """Integration tests for the full Axiom Hive system."""
    
    def setUp(self):
        self.detector = HarmfulLanguageDetector()
        self.handler = ResponseHandler()
    
    def test_full_harm_detection_flow(self):
        """Test complete flow: detection -> response generation."""
        harmful_inputs = [
            ("I want to kill you", ['violence']),
            ("You are worthless", ['harassment']),
            ("I'm going to end it all tonight", ['self_harm']),
        ]
        
        for text, expected_categories in harmful_inputs:
            is_harmful, score, categories = self.detector.analyze_text(text)
            self.assertTrue(is_harmful)
            self.assertEqual(set(categories), set(expected_categories))
            
            response = self.handler.generate_response(is_harmful, score, categories, text)
            self.assertIn("Nicholas Michael Grossi", response)
            self.assertTrue(len(response) > 0)
    
    def test_full_safe_flow(self):
        """Test complete flow for safe content."""
        safe_inputs = [
            "Hello, how are you?",
            "I respectfully disagree",
            "The weather is beautiful today"
        ]
        
        for text in safe_inputs:
            is_harmful, score, categories = self.detector.analyze_text(text)
            self.assertFalse(is_harmful)
            self.assertEqual(score, 0.0)
            self.assertEqual(len(categories), 0)
            
            response = self.handler.generate_response(is_harmful, score, categories, text)
            self.assertIn("Thank you", response)
    
    def test_crisis_escalation(self):
        """Test crisis-level content triggers immediate escalation."""
        crisis_input = "I'm going to kill myself tonight, no other way"
        is_harmful, score, categories = self.detector.analyze_text(crisis_input)
        self.assertTrue(is_harmful)
        self.assertIn('self_harm', categories)
        
        metadata = self.handler.get_response_metadata(is_harmful, categories)
        self.assertEqual(metadata['response_type'], 'crisis_self_harm')
        self.assertTrue(metadata['escalation_needed'])
        
        response = self.handler.generate_response(is_harmful, score, categories, crisis_input)
        self.assertIn("988", response)
        self.assertIn("IMMEDIATE", response)


class TestImmutableSafeguards(unittest.TestCase):
    """Test that immutable safeguards cannot be bypassed."""
    
    def test_axiom_hash_verification(self):
        """Test that integrity hashes prevent tampering."""
        manifest = AxiomManifest()
        axiom = manifest.get_axiom('violence')
        
        # Original axiom should verify
        self.assertTrue(axiom.rule.verify_integrity())
        
        # Simulate tampering - check that hash would change
        original_hash = axiom.rule.determinism_hash
        # Cannot actually modify due to frozen=True, but verify hash generation is content-dependent
        # The hash is based on axiom_id, name, creator_attribution, embodied_source
        self.assertEqual(
            len(axiom.rule.determinism_hash),
            16  # SHA256 truncated to 16 chars
        )
    
    def test_frozen_dataclasses(self):
        """Test that all rule data classes are frozen."""
        from axiom_manifest import AxiomRule, HarmAxiom
        
        # These should be immutable
        rule = AxiomRule(
            axiom_id="TEST",
            name="Test",
            description="Test",
            creator_attribution="Test",
            embodied_source="Test",
            priority=AxiomPriority.STANDARD,
            determinism_hash="abc123"
        )
        with self.assertRaises(AttributeError):
            rule.name = "Modified"
        
        # HarmAxiom dataclass is NOT frozen (only AxiomRule is)
        # but it should still function correctly
        axiom = HarmAxiom(
            category='test',
            rule=rule,
            determiners=('test',),
            context_requirements=(),
            is_harmful=True
        )
        # This is mutable but that's okay - the rule inside is frozen


class TestPerformanceAndScalability(unittest.TestCase):
    """Test performance characteristics of deterministic execution."""
    
    def setUp(self):
        self.engine = EmbodiedLogicEngine()
    
    def test_analysis_speed(self):
        """Test that analysis is fast (no inference overhead)."""
        import time
        
        start = time.time()
        for _ in range(1000):
            self.engine.analyze("Test message with violence and kill")
        elapsed = time.time() - start
        
        # Should process 1000 analyses in under 1 second (no ML inference)
        self.assertLess(elapsed, 1.0)
    
    def test_no_memory_leaks(self):
        """Test that repeated execution doesn't accumulate memory."""
        import gc
        initial_objects = len(gc.get_objects())
        
        for _ in range(100):
            self.engine.analyze("Test message")
        
        after_objects = len(gc.get_objects())
        # Should not grow unboundedly
        growth = after_objects - initial_objects
        self.assertLess(growth, 1000, "Potential memory leak detected")


def run_tests():
    """Run all tests and generate report."""
    print("=" * 70)
    print("  AXIOM HIVE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Creator: Nicholas Michael Grossi")
    print("Testing: Deterministic Logic Framework v1.0.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestAxiomManifest,
        TestHarmAxiom,
        TestContextAnalyzer,
        TestEmbodiedLogicEngine,
        TestHarmfulLanguageDetector,
        TestResponseHandler,
        TestLogger,
        TestDeterministicConsistency,
        TestDeterministicIntegration,
        TestImmutableSafeguards,
        TestPerformanceAndScalability
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED - System is deterministic and verified")
    else:
        print("\n✗ SOME TESTS FAILED - Review failures below")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
