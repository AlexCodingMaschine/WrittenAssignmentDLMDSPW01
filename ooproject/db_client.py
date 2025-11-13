"""
DBClient

Wraps a simple SQLite connection using SQLAlchemy and provides read/write
helpers for the CSV <-> DB workflow used by the project. This is intentionally
kept thin and delegates to pandas for IO so behavior matches the original
scripts exactly.
"""
from sqlalchemy import create_engine
import pandas as pd


class DBClient:
    """Simple DB client for reading/writing SQLite tables.

    This mirrors how the original scripts used SQLAlchemy + pandas.to_sql /
    pandas.read_sql. No logic is added; this is a small OO wrapper around
    the same behavior.
    """

    def __init__(self, db_path: str = 'database.db'):
        # My connection to the database
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')

    def read_table(self, table_name: str) -> pd.DataFrame:
        """Read the whole table from the SQLite database."""
        return pd.read_sql(f'SELECT * FROM {table_name}', con=self.engine)

    def write_table(self, table_name: str, df: pd.DataFrame, if_exists: str = 'replace') -> None:
        """Write a DataFrame into the database (delegates to pandas.to_sql)."""
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
