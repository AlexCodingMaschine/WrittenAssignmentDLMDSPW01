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
        self.loader = loader #stores the Dataloader we gave to the constructor
        if loader is not None:
            self.db_client = loader.db_client #When someone gives us a Dataloader we can use its DBClient
        else:
            self.db_client = None #If no loader is given, we have no DBClient either (makes sense)
"""So that every class that inherits from BaseComponent automatically gets access to the database"""
