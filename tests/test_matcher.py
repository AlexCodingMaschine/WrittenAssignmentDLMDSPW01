"""
Bare minimum unit tests for Matcher - just test core calculations work.
"""
import pytest
from ooproject import Matcher
from ooproject.data_loader import DataLoader
from ooproject.db_client import DBClient


class TestMatcher:
    """Minimal tests for Matcher."""

    def test_compute_deviations_returns_dict(self):
        """Test that compute_deviations returns a dictionary."""
        db_client = DBClient('database.db')
        loader = DataLoader(db_client)
        loader.load_from_db()
        
        # Use the actual top-4 ideal functions from real database
        matcher = Matcher(loader, ['Y48', 'Y44', 'Y50', 'Y2'])
        deviations = matcher.compute_deviations()
        
        # Should return dict with ideal names
        assert isinstance(deviations, dict)
        assert len(deviations) == 4
        
        # All deviations should be non-negative numbers
        for name, dev in deviations.items():
            assert isinstance(dev, (int, float))
            assert dev >= 0

    def test_match_and_write_table3_runs(self):
        """Test that match_and_write_table3 executes without error."""
        db_client = DBClient('database.db')
        loader = DataLoader(db_client)
        loader.load_from_db()
        
        matcher = Matcher(loader, ['Y48', 'Y44'])
        
        # Should run without raising exception
        matcher.match_and_write_table3()
