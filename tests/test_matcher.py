"""
Core calculation tests for Matcher
"""
import pytest 
from ooproject import Matcher
from ooproject.data_loader import DataLoader
from ooproject.db_client import DBClient


class TestMatcher:
    """Core calculation tests for Matcher"""

    def test_compute_deviations_returns_dict(self):
        """Test that compute_deviations returns a dictionary"""
        db_client = DBClient('database.db') #Connecting to our real database
        loader = DataLoader(db_client) #Dataloader gets access to the DB
        loader.load_from_db() #Load data into the database
        
        # Use the actual top-4 ideal functions from real database
        matcher = Matcher(loader, ['Y48', 'Y44', 'Y50', 'Y2']) #Using known ideal functions
        deviations = matcher.compute_deviations() #From matcher.py
        
        # Should return a dictionary with ideal names
        assert isinstance(deviations, dict)
        assert len(deviations) == 4
        
        # All deviations should be non-negative numbers
        for name, dev in deviations.items():
            assert isinstance(dev, (int, float)) #Deviations should be numbers
            assert dev >= 0 # Deviations should be non-negative

    def test_match_and_write_table3_runs(self): #Checks that the functions does not CRASH
        """Test that match_and_write_table3 executes without error"""
        db_client = DBClient('database.db') # Use real database
        loader = DataLoader(db_client) 
        loader.load_from_db()
        
        matcher = Matcher(loader, ['Y48', 'Y44']) 
        
        # Should run without raising exception
        matcher.match_and_write_table3() #Double delegate to main.py
