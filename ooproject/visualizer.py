"""
Visualizer

A minimal Visualizer class that delegates to the existing visualize.py
script (which already produces confirm_top4.html). 
This wrapper provides a small OO-approach. 
"""
from .data_loader import DataLoader
import visualize as viz_script


class Visualizer:
    """OO wrapper for the existing visualization script.
    No realy logic is added here.
    """

    def __init__(self, loader: DataLoader):
        self.loader = loader

    def confirm_top4(self):
        """Run the existing visualization script's main() function.

        This will generate confirm_top4.html as the original script does.
        """
        viz_script.main()
