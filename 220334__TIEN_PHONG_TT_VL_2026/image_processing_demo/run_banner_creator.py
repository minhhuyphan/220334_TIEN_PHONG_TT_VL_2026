"""
Run Free AI Banner Creator (Offline, No API Keys)
"""
import sys
from pathlib import Path
import tkinter as tk

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from banner_creator_free_ai import FreeAIBannerCreator

if __name__ == "__main__":
    root = tk.Tk()
    app = FreeAIBannerCreator(root)
    root.mainloop()
