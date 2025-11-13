"""
Base is a parent class for the ideal selector,
which inherits from this class
"""
from typing import Optional

from .data_loader import DataLoader


class BaseComponent:
    """
    Common base class for pipeline components 
    that avoids repeating the same setup code in every class.
    """

    def __init__(self, loader: Optional[DataLoader]):
        self.loader = loader #stores the given DataLoader
        self.db_client = loader.db_client if loader is not None else None
