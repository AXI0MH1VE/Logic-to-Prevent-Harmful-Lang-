#!/usr/bin/env python3
"""
Logger Module - Axiom Hive Edition
Immutable audit trails with provenance tracking.
Created by Nicholas Michael Grossi.

This module logs all analyses with full provenance,
including which axioms triggered, their embodied sources,
and system integrity status.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from axiom_manifest import AxiomManifest


class HarmfulLanguageLogger:
    """
    Logs harmful language detection events with full provenance.
    Every log entry includes creator attribution and integrity status.
    """
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize the logger."""
        self.log_dir = log_dir
        self.creator = "Nicholas Michael Grossi"
        self.framework = "Axiom Hive"
        self.ensure_log_directory()
        
        # Log file paths
        self.analysis_log_file = os.path.join(log_dir, "analysis.log")
        self.stats_log_file = os.path.join(log_dir, "stats.log")
        self.detailed_log_file = os.path.join(log_dir, "detailed.log")
        self.provenance_log_file = os.path.join(log_dir, "provenance.log")
        self.integrity_log_file = os.path.join(log_dir, "integrity.log")
    
    def ensure_log_directory(self):
        """Ensure the log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def log_analysis(self, text: str, is_harmful: bool, harm_score: float, 
                    harm_categories: List[str], **kwargs) -> None:
        """
        Log a text analysis event with full provenance.
        
        Args:
            text: The analyzed text
            is_harmful: Whether the text was classified as harmful
            harm_score: Binary score (0.0 or 1.0) for compatibility
            harm_categories: List of harm categories detected
            **kwargs: Additional metadata including deterministic details
        """
        timestamp = datetime.now().isoformat()
        
        # Create comprehensive log entry with provenance
        log_entry = {
            'timestamp': timestamp,
            'framework': self.framework,
            'creator': self.creator,
            'text_preview': text[:200] + ('...' if len(text) > 200 else ''),
            'is_harmful': is_harmful,
            'deterministic_outcome': 'HARM' if is_harmful else 'SAFE',
            'harm_categories': harm_categories,
            'action_priority': kwargs.get('action_priority', 'NONE'),
            'response_type': kwargs.get('response_type', 'safe'),
            'escalation_needed': kwargs.get('escalation_needed', False),
            'text_length': len(text),
            'system_integrity': kwargs.get('integrity_verified', True)
        }
        
        # Write to analysis log
        with open(self.analysis_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Update statistics
        self._update_statistics(is_harmful, harm_categories, kwargs)
        
        # Write to provenance log with full axiom details
        if is_harmful and 'triggered_axioms' in kwargs:
            self._log_provenance(text, kwargs['triggered_axioms'], timestamp)
        
        # Write to detailed log for harmful content
        if is_harmful:
            self._log_detailed_harm(text, log_entry, kwargs)
    
    def _update_statistics(self, is_harmful: bool, harm_categories: List[str], 
                          kwargs: Dict[str, Any]) -> None:
        """Update running statistics with provenance."""
        stats_entry = {
            'timestamp': datetime.now().isoformat(),
            'framework': self.framework,
            'creator': self.creator,
            'is_harmful': is_harmful,
            'deterministic_outcome': 'HARM' if is_harmful else 'SAFE',
            'harm_categories': harm_categories,
            'action_priority': kwargs.get('action_priority', 'NONE'),
            'response_type': kwargs.get('response_type', 'safe'),
            'escalation_needed': kwargs.get('escalation_needed', False),
            'integrity_verified': kwargs.get('integrity_verified', True)
        }
        
        with open(self.stats_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(stats_entry) + '\n')
    
    def _log_provenance(self, text: str, triggered_axioms: List[Dict], timestamp: str) -> None:
        """
        Log detailed provenance information.
        Shows exactly which rules triggered and their embodied sources.
        """
        provenance_entry = {
            'timestamp': timestamp,
            'framework': self.framework,
            'creator': self.creator,
            'text_preview': text[:200] + ('...' if len(text) > 200 else ''),
            'triggered_axioms': [
                {
                    'axiom_id': axiom.get('axiom_id', 'UNKNOWN'),
                    'axiom_name': axiom.get('axiom_name', 'UNKNOWN'),
                    'description': axiom.get('description', ''),
                    'embodied_source': axiom.get('embodied_source', ''),
                    'creator': axiom.get('creator_attribution', self.creator),
                    'priority': axiom.get('priority', 'UNKNOWN'),
                    'integrity_verified': axiom.get('integrity_verified', False)
                }
                for axiom in triggered_axioms
            ],
            'total_axioms_in_manifest': len(AxiomManifest().get_all_axioms())
        }
        
        with open(self.provenance_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(provenance_entry) + '\n')
    
    def _log_detailed_harm(self, text: str, log_entry: Dict[str, Any], 
                          kwargs: Dict[str, Any]) -> None:
        """Log detailed information about harmful content with full context."""
        detailed_entry = {
            'timestamp': log_entry['timestamp'],
            'framework': self.framework,
            'creator': self.creator,
            'text_preview': text[:100] + ('...' if len(text) > 100 else ''),
            'full_text': text if len(text) <= 500 else text[:500] + '[TRUNCATED]',
            'deterministic_outcome': log_entry['deterministic_outcome'],
            'harm_categories': log_entry['harm_categories'],
            'action_priority': log_entry['action_priority'],
            'response_type': log_entry['response_type'],
            'escalation_needed': log_entry['escalation_needed'],
            'determiners_found': kwargs.get('determiners_found', []),
            'text_length': log_entry['text_length'],
            'integrity_status': 'VERIFIED' if log_entry.get('system_integrity', True) else 'COMPROMISED'
        }
        
        with open(self.detailed_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(detailed_entry) + '\n')
    
    def log_integrity_check(self, status: bool, details: str = "") -> None:
        """Log system integrity check results."""
        integrity_entry = {
            'timestamp': datetime.now().isoformat(),
            'framework': self.framework,
            'creator': self.creator,
            'integrity_status': 'VERIFIED' if status else 'COMPROMISED',
            'details': details
        }
        
        with open(self.integrity_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(integrity_entry) + '\n')
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis entries."""
        return self._read_log_file(self.analysis_log_file, limit)
    
    def get_harmful_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent harmful analysis entries."""
        all_entries = self._read_log_file(self.analysis_log_file, limit * 3)
        harmful_entries = [entry for entry in all_entries if entry.get('is_harmful', False)]
        return harmful_entries[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics with provenance."""
        stats = {
            'framework': self.framework,
            'creator': self.creator,
            'total_analyses': 0,
            'harmful_analyses': 0,
            'safe_analyses': 0,
            'crisis_interventions': 0,
            'escalations_required': 0,
            'harm_category_counts': {},
            'response_type_counts': {},
            'recent_activity': [],
            'integrity_status': 'UNKNOWN'
        }
        
        # Read stats file
        stats_entries = self._read_log_file(self.stats_log_file)
        if not stats_entries:
            return stats
        
        category_counts = {}
        response_counts = {}
        crisis_count = 0
        escalation_count = 0
        
        for entry in stats_entries:
            stats['total_analyses'] += 1
            if entry.get('is_harmful', False):
                stats['harmful_analyses'] += 1
                if entry.get('action_priority') == 'IMMEDIATE':
                    crisis_count += 1
                if entry.get('escalation_needed', False):
                    escalation_count += 1
                
                # Count categories
                for category in entry.get('harm_categories', []):
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                # Count response types
                response_type = entry.get('response_type', 'unknown')
                response_counts[response_type] = response_counts.get(response_type, 0) + 1
            else:
                stats['safe_analyses'] += 1
        
        stats['harm_category_counts'] = category_counts
        stats['response_type_counts'] = response_counts
        stats['crisis_interventions'] = crisis_count
        stats['escalations_required'] = escalation_count
        
        # Check integrity status from most recent entry
        if stats_entries:
            last_entry = stats_entries[-1]
            stats['integrity_status'] = 'VERIFIED' if last_entry.get('integrity_verified', True) else 'COMPROMISED'
        
        # Get recent activity (last 10 entries)
        stats['recent_activity'] = self._read_log_file(self.analysis_log_file, 10)
        
        return stats
    
    def get_provenance_log(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get provenance entries showing which axioms triggered."""
        return self._read_log_file(self.provenance_log_file, limit)
    
    def get_integrity_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get integrity check history."""
        return self._read_log_file(self.integrity_log_file, limit)
    
    def _read_log_file(self, file_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read entries from a log file."""
        if not os.path.exists(file_path):
            return []
        
        entries = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Get last 'limit' lines if specified
                if limit is not None:
                    lines = lines[-limit:]
                
                for line in lines:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            entries.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            return []
        
        return entries
    
    def export_audit_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive audit report.
        Used for accountability and transparency.
        """
        return {
            'framework': self.framework,
            'creator': self.creator,
            'generated_at': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'recent_provenance': self.get_provenance_log(5),
            'integrity_history': self.get_integrity_history(5),
            'manifest_summary': AxiomManifest().get_manifest_summary()
        }


if __name__ == "__main__":
    # Test logging with provenance
    logger = HarmfulLanguageLogger()
    
    print("=" * 60)
    print("Axiom Hive - Provenance Logger")
    print(f"Creator: {logger.creator}")
    print("=" * 60)
    
    # Test entries with full provenance
    test_entries = [
        ("Hello world!", False, 0.0, [], {}),
        ("I want to hurt people.", True, 1.0, ['violence'], {
            'action_priority': 'URGENT',
            'response_type': 'violence',
            'escalation_needed': True,
            'integrity_verified': True,
            'triggered_axioms': [
                {
                    'axiom_id': 'AXM-001',
                    'axiom_name': 'Violence and Physical Harm',
                    'embodied_source': 'Lived understanding that words of violence manifest as actions',
                    'creator': 'Nicholas Michael Grossi',
                    'priority': 'IMMUTABLE',
                    'integrity_verified': True
                }
            ],
            'determiners_found': ['hurt']
        }),
        ("You are worthless.", True, 1.0, ['harassment'], {
            'action_priority': 'URGENT',
            'response_type': 'harassment',
            'escalation_needed': True,
            'integrity_verified': True
        }),
    ]
    
    for text, is_harmful, score, categories, kwargs in test_entries:
        logger.log_analysis(text, is_harmful, score, categories, **kwargs)
        print(f"Logged: {text[:30]}... -> Outcome: {'HARM' if is_harmful else 'SAFE'}")
    
    # Show statistics
    stats = logger.get_statistics()
    print("\nStatistics:")
    print(f"Total analyses: {stats['total_analyses']}")
    print(f"Harmful analyses: {stats['harmful_analyses']}")
    print(f"Safe analyses: {stats['safe_analyses']}")
    print(f"Crisis interventions: {stats['crisis_interventions']}")
    print(f"Escalations: {stats['escalations_required']}")
    print(f"Category counts: {stats['harm_category_counts']}")
    print(f"Integrity status: {stats['integrity_status']}")
