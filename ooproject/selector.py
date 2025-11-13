"""
IdealSelector

Object-oriented implementation of the selection logic that chooses the
top-K ideal functions by aggregated SSE (preserves the original procedural
comments and behavior from `main.py`). The class inherits from
`BaseComponent` and uses a `DataLoader` for DB path access.
"""
from typing import List, Tuple
from .data_loader import DataLoader
from .base import BaseComponent

import numpy as np	# numerical computations
import pandas as pd	# reading/writing tables
from sqlalchemy import create_engine # Python to SQLite-database


class IdealSelector(BaseComponent):
    """Select ideal functions that best fit the training set.

    This class implements the same algorithm as `select_top4_ideals` in the
    original procedural code: interpolate each ideal onto the training X-grid,
    sum SSE across all training Y-series (ignoring NaNs), and return the 4
    ideals by total SSE. 
    If an ideal has no overlap with the training X-values
    it receives an infinite SSE so it won't be chosen.
    """

    def __init__(self, loader: DataLoader): #here we use the inherited BaseComponent init
        super().__init__(loader)    #we call the parent constructor to set up loader and db_client

    def select_top_k(self, k: int = 4, table_train: str = 'Table1', table_ideal: str = 'Table2') -> List[Tuple[str, float]]:
        """Return a list of (name, total_sse) tuples for the top-k ideals.

        The implementation mirrors the original procedural function so results
        remain unchanged.

        My focus was to learn python procedural (more easily than OO for me)

        And after that i tried to convert it to OO by using classes and making 
        use of inheritance.

        So I commented the main.py pretty good.

        I have used two methods to get a OO structure:
        1. Making new classes and implementing the logic in methods of those classes (here).

        2. Making new classes and import the existing functions from main.py
        """

        # connect to database via sqlalchemy
        engine = create_engine(f'sqlite:///{self.loader.db_path}')

        # Read tables into DataFrames
        df_train = pd.read_sql(f'SELECT * FROM {table_train}', con=engine)
        df_ideal = pd.read_sql(f'SELECT * FROM {table_ideal}', con=engine)

        # Get column names
        x_train_col = df_train.columns[0]
        train_value_cols = list(df_train.columns[1:])
        x_ideal_col = df_ideal.columns[0]
        ideal_cols = list(df_ideal.columns[1:])

        # Extract X-values from training data
        x_train = df_train[x_train_col].values
        print(f"train X: n={len(x_train)}, min={x_train.min():.6g}, max={x_train.max():.6g}")

        sse_results = []

        # sort ideal X-values for safe interpolation
        ideal_sort_idx = np.argsort(df_ideal[x_ideal_col].values)
        x_ideal_sorted = df_ideal[x_ideal_col].values[ideal_sort_idx]

        # Loop through each ideal function column
        for col in ideal_cols:
            y_ideal = df_ideal[col].values[ideal_sort_idx]
            # Interpolate ideal onto train X grid; out-of-range -> NaN (conservative)
            y_at_train = np.interp(x_train, x_ideal_sorted, y_ideal, left=np.nan, right=np.nan)

            total_sse = 0.0
            any_valid = False

            # Sum SSE across all train series
            for tcol in train_value_cols:
                y_train = df_train[tcol].values
                mask = (~np.isnan(y_at_train)) & (~np.isnan(y_train))
                if mask.any():
                    res = y_train[mask] - y_at_train[mask]
                    total_sse += float(np.sum(res * res))
                    any_valid = True

            # If the ideal had no overlap with training data assign infinite SSE
            if not any_valid:
                total_sse = float('inf')

            sse_results.append((col, total_sse))

        # Sort by SSE ascending and take the top-k smallest
        sse_results.sort(key=lambda x: x[1])
        topk = sse_results[:k]

        print(f'Top {k} ideal functions (name, total_sse):')
        for name, sse in topk:
            print(f'  {name}: {sse}')

        return topk
