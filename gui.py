# gui.py

# We import our utility functions from the utils module.
from utils import get_window_title
# Import the new settings manager
from settings_manager import load_settings

# The tkinter library is Python's standard GUI toolkit.
import tkinter as tk

# Import the main menu screen
from main_menu import MainMenu

# Import the options menu screen
from options_menu import OptionsMenu

# Import the new database menu screen
from database_menu import DatabaseMenu

# This is the main class for our application.
class Application:
    """
    The main application class that manages the window and frame switching.
    """
    def __init__(self, master):
        """
        Initializes the application window and all its frames.
        
        Args:
            master: The root window of the application.
        """
        self.master = master
        
        # We use functions from the utils module to configure the window.
        master.title(get_window_title())
        master.minsize(800, 600)
        
        # Load the saved settings on startup
        self.settings = load_settings()
        self._apply_initial_settings()

        # Create a container frame where other frames will be placed
        container = tk.Frame(master)
        container.pack(fill="both", expand=True)

        # Configure the grid in the container to be responsive
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # A dictionary to hold all the frames (screens) of the application
        self.frames = {}
        
        # Create and add the MainMenu frame to our dictionary of frames
        self.frames["MainMenu"] = MainMenu(container, self.show_frame)
        
        # Create and add the OptionsMenu frame to our dictionary of frames
        self.frames["OptionsMenu"] = OptionsMenu(container, self.show_frame, self.settings)

        # Create and add the new DatabaseMenu frame to our dictionary of frames
        # DatabaseMenu will now manage EnemyViewer internally
        self.frames["DatabaseMenu"] = DatabaseMenu(container, self.show_frame)

        # Position all frames on top of each other using grid
        for frame_name, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the main menu when the application starts
        self.show_frame("MainMenu")

    def show_frame(self, page_name, **kwargs):
        """
        Raises the specified frame to the top, making it visible.

        Args:
            page_name: The name of the frame to show (e.g., "MainMenu", "OptionsMenu", "DatabaseMenu").
            **kwargs: Additional keyword arguments (no longer directly used for EnemyViewer here).
        """
        frame = self.frames[page_name]
        # The EnemyViewer is now managed internally by DatabaseMenu,
        # so no special handling is needed here for it.
        frame.tkraise()
    
    def _apply_initial_settings(self):
        """
        Applies the settings loaded from the config file to the main window.
        """
        resolution = self.settings.get("resolution", "800x600")
        mode = self.settings.get("mode", "Windowed")
        
        self.master.geometry(resolution)
        if mode in ["Fullscreen", "Borderless Window"]:
            self.master.attributes("-fullscreen", True)
        else:
            self.master.attributes("-fullscreen", False)


def run_app():
    """
    This function creates the main window and runs the application loop.
    This explicit function is a best practice for clarity and compatibility
    with tools like PyInstaller.
    """
    # Create the root window. This is the main window of the application.
    root = tk.Tk()

    # Create an instance of our Application class.
    # This will initialize the GUI and show the main menu.
    app = Application(root)
    
    # This line starts the main event loop.
    root.mainloop()
