"""
DBClient
Also a wrapper class.
Makes a connection to the database and provides reads/writes into tables.
"""
from sqlalchemy import create_engine
import pandas as pd


class DBClient:
    """Simple DB client for reading/writing SQLite tables
    We connect with DBClient to SQLite and we are using pandas to read and write tabless
    """

    def __init__(self, db_path: str = 'database.db'): #_init_ = constructor
        """Initialize the DBClient with a connection to the given database path."""
        from .exceptions import DataLoadError
        # My connection to the database
        self.db_path = db_path
        try:
            self.engine = create_engine(f'sqlite:///{db_path}') #Builds a SQLAlchemy-Engine -> used to connect to the database
        except Exception as e:
            raise DataLoadError(f"Failed to create database engine for {db_path}: {e}")

    def read_table(self, table_name: str) -> pd.DataFrame:
        """Read the whole table from the SQLite database."""
        from .exceptions import DataLoadError
        try:
            return pd.read_sql(f'SELECT * FROM {table_name}', con=self.engine)
        except Exception as e:
            raise DataLoadError(f"Failed to read table '{table_name}': {e}")

    def write_table(self, table_name: str, df: pd.DataFrame, if_exists: str = 'replace') -> None:
        """Write a DataFrame into the database using pandas"""
        from .exceptions import DataLoadError
        try:
            df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
        except Exception as e:
            raise DataLoadError(f"Failed to write table '{table_name}': {e}")
