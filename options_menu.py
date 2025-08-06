# options_menu.py

import tkinter as tk
from settings_manager import save_settings

class OptionsMenu(tk.Frame):
    """
    A frame representing the options menu of the game.
    """
    def __init__(self, master, switch_frame_callback, initial_settings):
        """
        Initializes the OptionsMenu frame.

        Args:
            master: The parent widget (the main application window).
            switch_frame_callback: A function to call to switch to another frame.
            initial_settings (dict): The settings loaded from the config file.
        """
        super().__init__(master)
        self.master = master
        self.switch_frame_callback = switch_frame_callback
        self.configure(bg="#2c2c2c")

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Title Label ---
        title_label = tk.Label(self, text="Options", font=("Helvetica", 24), fg="#f0f0f0", bg="#2c2c2c")
        title_label.grid(row=0, column=0, pady=(20, 20), sticky="n")

        # --- Options frame ---
        # A separate frame to hold the options, for better layout control
        options_frame = tk.Frame(self, bg="#3c3c3c")
        options_frame.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)

        # --- Display Settings Heading ---
        display_heading_label = tk.Label(options_frame, text="Display Settings", font=("Helvetica", 18, "bold"),
                                         fg="#f0f0f0", bg="#3c3c3c")
        display_heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), sticky="ew")

        # --- Screen Resolution Option ---
        resolution_label = tk.Label(options_frame, text="Screen Resolution", font=("Helvetica", 12),
                                    fg="#f0f0f0", bg="#3c3c3c")
        resolution_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Dropdown menu for screen resolutions
        resolutions = ["800x600", "1280x720", "1920x1080"]
        self.resolution_var = tk.StringVar(self)
        self.resolution_var.set(initial_settings.get("resolution", "800x600")) # Use initial settings
        resolution_menu = tk.OptionMenu(options_frame, self.resolution_var, *resolutions)
        resolution_menu.config(bg="#555555", fg="#f0f0f0", activebackground="#666666", activeforeground="#f0f0f0")
        resolution_menu["menu"].config(bg="#555555", fg="#f0f0f0")
        resolution_menu.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        # --- Display Mode Option ---
        display_mode_label = tk.Label(options_frame, text="Display Mode", font=("Helvetica", 12),
                                     fg="#f0f0f0", bg="#3c3c3c")
        display_mode_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        # Dropdown menu for display modes
        display_modes = ["Windowed", "Fullscreen", "Borderless Window"]
        self.display_mode_var = tk.StringVar(self)
        self.display_mode_var.set(initial_settings.get("mode", "Windowed")) # Use initial settings
        display_mode_menu = tk.OptionMenu(options_frame, self.display_mode_var, *display_modes)
        display_mode_menu.config(bg="#555555", fg="#f0f0f0", activebackground="#666666", activeforeground="#f0f0f0")
        display_mode_menu["menu"].config(bg="#555555", fg="#f0f0f0")
        display_mode_menu.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        
        # --- Save Settings button ---
        save_button = tk.Button(options_frame, text="Save Settings", font=("Helvetica", 12),
                                width=15, pady=5, bg="#444444", fg="#f0f0f0",
                                relief="raised", bd=3,
                                command=self.save_settings)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # --- Back button ---
        back_button = tk.Button(self, text="Back", font=("Helvetica", 16),
                                width=15, pady=5, bg="#555555", fg="#f0f0f0",
                                relief="raised", bd=3,
                                command=lambda: self.switch_frame_callback("MainMenu"))
        back_button.grid(row=2, column=0, pady=20)

    def _apply_resolution(self, resolution):
        """
        Applies the selected window resolution.
        """
        # We need to disable fullscreen before applying a new resolution.
        self.master.master.attributes("-fullscreen", False)
        self.master.master.geometry(resolution)
        print(f"Window resolution set to: {resolution}")

    def _apply_display_mode(self, mode):
        """
        Applies the selected display mode.
        """
        # The main window is the master of the master (the container frame).
        root = self.master.master
        
        # First, we reset all attributes to a normal windowed state.
        root.attributes("-fullscreen", False)
        root.overrideredirect(False)
        
        if mode == "Fullscreen" or mode == "Borderless Window":
            # In Tkinter, the best way to achieve a managed, tabbable borderless window
            # is to use the native fullscreen attribute. This removes all borders and
            # title bars while keeping the window under OS control.
            root.attributes("-fullscreen", True)
            root.bind("<Escape>", self._exit_fullscreen)
            print(f"Display mode set to: {mode}. Press 'Esc' to exit.")
        else: # Windowed mode
            root.unbind("<Escape>")
            print("Display mode set to: Windowed")

    def _exit_fullscreen(self, event):
        """
        Exits fullscreen mode when the Escape key is pressed.
        """
        self.master.master.attributes("-fullscreen", False)
        self.master.master.unbind("<Escape>")
        print("Exited fullscreen mode.")

    def save_settings(self):
        """
        Saves and applies the display settings.
        This is where you would connect the UI to the game logic.
        """
        # Get the current selected values from the dropdowns
        selected_resolution = self.resolution_var.get()
        selected_mode = self.display_mode_var.get()

        print(f"Applying settings...")

        # Apply the resolution change (this also disables fullscreen temporarily)
        self._apply_resolution(selected_resolution)

        # Apply the display mode change
        self._apply_display_mode(selected_mode)
        
        # Save the current settings to the config file
        settings = {"resolution": selected_resolution, "mode": selected_mode}
        save_settings(settings)
