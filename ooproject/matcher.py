from typing import List, Dict
from .data_loader import DataLoader
from main import compute_deviation_for_ideals, match_test_to_table3
#Here we import the already implemented functions from main.py an call them
#In this class i decided to wrap the existing functions without changing their logic


"""The Matcher is again a wrapper to organize the existing code from main.py into an OOP-friendly class
With the Matcher class we can compute the deviations for the chosen ideals
and we can match the test data to table3 and write it to the database"""
class Matcher:

    def __init__(self, loader: DataLoader, chosen_names: List[str]):
        self.loader = loader
        self.chosen_names = chosen_names

    def compute_deviations(self) -> Dict[str, float]:
        from .exceptions import MatchingError

        try:
            return compute_deviation_for_ideals(db_path=self.loader.db_path, table_train='Table1', table_ideal='Table2', ideal_names=self.chosen_names)
        except Exception as e:
            raise MatchingError(f"Failed to compute deviations: {e}")

    def match_and_write_table3(self, multiplier: float = None) -> None:
        from .exceptions import MatchingError

        try:
            if multiplier is None:
                match_test_to_table3(self.chosen_names, db_path=self.loader.db_path)
            else:
                # pass multiplier through to keep behavior explicit
                match_test_to_table3(self.chosen_names, db_path=self.loader.db_path, multiplier=multiplier)
        except Exception as e:
            raise MatchingError(f"Failed to match test data and write Table3: {e}")
