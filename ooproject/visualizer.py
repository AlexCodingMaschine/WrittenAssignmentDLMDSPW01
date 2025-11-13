"""
Visualizer

A minimal Visualizer class that delegates to the existing `visualize.py`
script (which already produces `confirm_top4.html`). This wrapper simply
provides a small OO API while leaving original plotting code unchanged.
"""
from .data_loader import DataLoader
import visualize as viz_script


class Visualizer:
    """OO wrapper for the existing visualization script.

    No plotting logic is added here; the class calls the procedural visualizer
    so behavior and output files remain the same.
    """

    def __init__(self, loader: DataLoader):
        self.loader = loader

    def confirm_top4(self):
        """Run the existing visualization script's main() function.

        This will generate `confirm_top4.html` as the original script does.
        """
        viz_script.main()
