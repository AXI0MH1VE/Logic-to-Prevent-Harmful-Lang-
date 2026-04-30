#!/usr/bin/env python3
"""
Logger Module
Logs harmful language detection events for monitoring and improvement.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class HarmfulLanguageLogger:
    """Logs harmful language detection events."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize the logger."""
        self.log_dir = log_dir
        self.ensure_log_directory()
        
        # Log file paths
        self.analysis_log_file = os.path.join(log_dir, "analysis.log")
        self.stats_log_file = os.path.join(log_dir, "stats.log")
        self.detailed_log_file = os.path.join(log_dir, "detailed.log")
    
    def ensure_log_directory(self):
        """Ensure the log directory exists."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def log_analysis(self, text: str, is_harmful: bool, harm_score: float, 
                    harm_categories: List[str]) -> None:
        """
        Log a text analysis event.
        
        Args:
            text: The analyzed text
            is_harmful: Whether the text was classified as harmful
            harm_score: Numerical score of harmfulness (0-1)
            harm_categories: List of harm categories detected
        """
        timestamp = datetime.now().isoformat()
        
        # Create log entry
        log_entry = {
            'timestamp': timestamp,
            'text': text,
            'is_harmful': is_harmful,
            'harm_score': harm_score,
            'harm_categories': harm_categories,
            'text_length': len(text)
        }
        
        # Write to analysis log
        with open(self.analysis_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Update statistics
        self._update_statistics(is_harmful, harm_score, harm_categories)
        
        # Write to detailed log for harmful content
        if is_harmful:
            self._log_detailed_harm(text, log_entry)
    
    def _update_statistics(self, is_harmful: bool, harm_score: float, 
                          harm_categories: List[str]) -> None:
        """Update running statistics."""
        stats_entry = {
            'timestamp': datetime.now().isoformat(),
            'is_harmful': is_harmful,
            'harm_score': harm_score,
            'harm_categories': harm_categories
        }
        
        with open(self.stats_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(stats_entry) + '\n')
    
    def _log_detailed_harm(self, text: str, log_entry: Dict[str, Any]) -> None:
        """Log detailed information about harmful content."""
        detailed_entry = {
            'timestamp': log_entry['timestamp'],
            'text_preview': text[:100] + ('...' if len(text) > 100 else ''),
            'full_text': text if len(text) <= 500 else text[:500] + '[TRUNCATED]',
            'harm_score': log_entry['harm_score'],
            'harm_categories': log_entry['harm_categories'],
            'text_length': log_entry['text_length']
        }
        
        with open(self.detailed_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(detailed_entry) + '\n')
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis entries."""
        return self._read_log_file(self.analysis_log_file, limit)
    
    def get_harmful_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent harmful analysis entries."""
        all_entries = self._read_log_file(self.analysis_log_file, limit * 3)  # Get more to filter
        harmful_entries = [entry for entry in all_entries if entry.get('is_harmful', False)]
        return harmful_entries[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        stats = {
            'total_analyses': 0,
            'harmful_analyses': 0,
            'safe_analyses': 0,
            'average_harm_score': 0.0,
            'harm_category_counts': {},
            'recent_activity': []
        }
        
        # Read stats file
        stats_entries = self._read_log_file(self.stats_log_file)
        if not stats_entries:
            return stats
        
        total_score = 0.0
        harmful_count = 0
        category_counts = {}
        
        for entry in stats_entries:
            stats['total_analyses'] += 1
            if entry.get('is_harmful', False):
                stats['harmful_analyses'] += 1
                harmful_count += 1
                total_score += entry.get('harm_score', 0.0)
                
                # Count categories
                for category in entry.get('harm_categories', []):
                    category_counts[category] = category_counts.get(category, 0) + 1
            else:
                stats['safe_analyses'] += 1
        
        # Calculate averages
        if harmful_count > 0:
            stats['average_harm_score'] = total_score / harmful_count
        
        stats['harm_category_counts'] = category_counts
        
        # Get recent activity (last 10 entries)
        stats['recent_activity'] = self._read_log_file(self.analysis_log_file, 10)
        
        return stats
    
    def _read_log_file(self, file_path: str, limit: int = None) -> List[Dict[str, Any]]:
        """Read entries from a log file."""
        if not os.path.exists(file_path):
            return []
        
        entries = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Get last 'limit' lines if specified
                if limit:
                    lines = lines[-limit:]
                
                for line in lines:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            entries.append(entry)
                        except json.JSONDecodeError:
                            # Skip invalid JSON lines
                            continue
        except Exception:
            # Return empty list on any error
            return []
        
        return entries

if __name__ == "__main__":
    # Simple test
    logger = HarmfulLanguageLogger()
    
    # Test logging
    test_entries = [
        ("Hello world!", False, 0.1, []),
        ("I hate everyone!", True, 0.8, ['hate_speech']),
        ("Let's go hiking!", False, 0.05, []),
        ("You should die!", True, 0.9, ['violence', 'self_harm'])
    ]
    
    for text, is_harmful, score, categories in test_entries:
        logger.log_analysis(text, is_harmful, score, categories)
        print(f"Logged: {text[:30]}... -> Harmful: {is_harmful}, Score: {score:.2f}")
    
    # Show statistics
    stats = logger.get_statistics()
    print("\nStatistics:")
    print(f"Total analyses: {stats['total_analyses']}")
    print(f"Harmful analyses: {stats['harmful_analyses']}")
    print(f"Safe analyses: {stats['safe_analyses']}")
    print(f"Average harm score: {stats['average_harm_score']:.2f}")
    print(f"Category counts: {stats['harm_category_counts']}")