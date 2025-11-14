from typing import Optional
import pandas as pd
import numpy as np
from .db_client import DBClient
""" The Dataloader class is responsible for loading and caching data from the database
and CSV files. It provides methods to load training and ideal datasets from the database,
as well as loading test data from a CSV file. We also do some caching."""

class DataLoader:
    def __init__(self, db_client: Optional[DBClient] = None, db_path: str = 'database.db'):
        #  If no database client is given, create one using the given database path
        if db_client is not None:
            self.db_client = db_client
            self.db_path = db_client.db_path  # Use the path from the provided client
        else:
            self.db_client = DBClient(db_path)
            self.db_path = db_path  # Use the provided path

        # Create empty placeholders for data (will be filled later)
        self.train_df: Optional[pd.DataFrame] = None #training data table
        self.ideal_df: Optional[pd.DataFrame] = None #ideal data table
        self.test_df: Optional[pd.DataFrame] = None #test data table

        #  Create empty placeholders for arrays (will be also filled later)
        self.x_train: Optional[np.ndarray] = None # For X values from training data
        self.x_ideal_sorted: Optional[np.ndarray] = None # For X values from training data
        self.ideal_sort_idx: Optional[np.ndarray] = None # For sorted X values from ideal

    def load_from_db(self, table_train: str = 'Table1', table_ideal: str = 'Table2') -> None:
        """Load training and ideal tables from DB and prepare cached arrays"""
        from .exceptions import DataLoadError, ValidationError

        try:
            #Read training table from database
            self.train_df = self.db_client.read_table(table_train)
            #Read ideal table from database
            self.ideal_df = self.db_client.read_table(table_ideal)
        except Exception as e:
            raise DataLoadError(f"Failed to load tables from database: {e}")

        # Validate tables have data
        if self.train_df.empty or self.ideal_df.empty:
            raise ValidationError("Training or ideal table is empty")

        try:
            # Create empty placeholders for arrays (will be also filled later)
            self.x_train = self.train_df.iloc[:, 0].values # Get the first column (X values) from training data
            x_ideal = self.ideal_df.iloc[:, 0].values # Get the first column (X values) from ideal data
            self.ideal_sort_idx = np.argsort(x_ideal) #  Sort the ideal X values and store the sort order (indices)
            self.x_ideal_sorted = x_ideal[self.ideal_sort_idx] # Store the sorted ideal X values
        except Exception as e:
            raise ValidationError(f"Failed to prepare cached arrays: {e}")

    def load_test_csv(self, test_csv: str = 'Datasets/test.csv') -> None:
        """Load test CSV and optimize some things"""
        from .exceptions import DataLoadError, ValidationError

        try:
            df = pd.read_csv(test_csv) # Load test CSV file
        except FileNotFoundError:
            raise DataLoadError(f"Test CSV file not found: {test_csv}")
        except Exception as e:
            raise DataLoadError(f"Failed to read test CSV {test_csv}: {e}")

        if df.empty:
            raise ValidationError(f"Test CSV file is empty: {test_csv}")

        # If columns are named 'x' and 'y', rename them to 'X' and 'Y' like the tables in the written assignment
        if 'x' in df.columns: #rename columns if needed
            df = df.rename(columns={'x': 'X', 'y': 'Y'}) #rename columns to match others
        else:
            df.columns = ['X', 'Y']
        #For safety convert to numeric (no strings allowed)
        df['X'] = pd.to_numeric(df['X'], errors='coerce') #convert to numeric
        df['Y'] = pd.to_numeric(df['Y'], errors='coerce') #convert to numeric
        self.test_df = df #Save cleaned data in cache

    def get_train_arrays(self):
        # Return X values from training data and names of Y columns
        return self.x_train, list(self.train_df.columns[1:])

    def get_ideal_grid(self):
        # Return sorted X values from ideal data and their sort indices
        return self.x_ideal_sorted, self.ideal_sort_idx
