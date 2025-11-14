"""
Bare minimum unit tests for IdealSelector - just test core calculations work.
"""
import pytest
from ooproject import IdealSelector
from ooproject.data_loader import DataLoader
from ooproject.db_client import DBClient


class TestIdealSelector:
    """Minimal tests for IdealSelector."""

    def test_select_top_k_returns_results(self):
        """Test that select_top_k returns some results from real database."""
        db_client = DBClient('database.db')
        loader = DataLoader(db_client)
        loader.load_from_db()
        
        selector = IdealSelector(loader)
        top4 = selector.select_top_k(k=4)
        
        # Just check we got 4 results
        assert len(top4) == 4
        
        # Check each result is a tuple with (name, sse)
        for name, sse in top4:
            assert isinstance(name, str)
            assert isinstance(sse, (int, float))
            assert sse >= 0  # SSE should be non-negative

    def test_results_sorted_by_sse(self):
        """Test that results are sorted by SSE ascending."""
        db_client = DBClient('database.db')
        loader = DataLoader(db_client)
        loader.load_from_db()
        
        selector = IdealSelector(loader)
        top4 = selector.select_top_k(k=4)
        
        sses = [sse for _, sse in top4]
        # Check sorted
        assert sses == sorted(sses)

    def test_k_validation(self):
        """Test that invalid k raises error."""
        db_client = DBClient('database.db')
        loader = DataLoader(db_client)
        loader.load_from_db()
        
        selector = IdealSelector(loader)
        
        with pytest.raises(ValueError):
            selector.select_top_k(k=0)
