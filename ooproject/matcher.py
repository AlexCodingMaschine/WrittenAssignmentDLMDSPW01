from typing import List, Dict
from .data_loader import DataLoader
from main import compute_deviation_for_ideals, match_test_to_table3
#Here we import the already implemented functions from main.py an call them
#In this class i decided to wrap the existing functions without changing their logic

class Matcher:

    def __init__(self, loader: DataLoader, chosen_names: List[str]):
        self.loader = loader
        self.chosen_names = chosen_names

    def compute_deviations(self) -> Dict[str, float]:

        return compute_deviation_for_ideals(db_path=self.loader.db_path, table_train='Table1', table_ideal='Table2', ideal_names=self.chosen_names)

    def match_and_write_table3(self, multiplier: float = None) -> None:
        if multiplier is None:
            match_test_to_table3(self.chosen_names)
        else:
            # pass multiplier through to keep behavior explicit
            match_test_to_table3(self.chosen_names, multiplier=multiplier)
