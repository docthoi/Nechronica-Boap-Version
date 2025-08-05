# main_menu.py

import tkinter as tk
from tkinter import PhotoImage
import os # Import the os module to handle file paths
import sys # Import the sys module to get the script's path

class MainMenu(tk.Frame):
    """
    A frame representing the main menu of the game.
    """
    def __init__(self, master, switch_frame_callback):
        """
        Initializes the MainMenu frame.

        Args:
            master: The parent widget (the main application window).
            switch_frame_callback: A function to call to switch to another frame.
        """
        # Call the constructor of the parent class (tk.Frame)
        super().__init__(master)
        self.master = master
        self.switch_frame_callback = switch_frame_callback

        # Set the background color
        self.configure(bg="#2c2c2c")

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Image at the top ---
        # A try-except block is used for error handling in case the image file is not found.
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            image_path = os.path.join(base_path, 'Pictures', 'Title.png')
            
            self.menu_image = PhotoImage(file=image_path)
            image_label = tk.Label(self, image=self.menu_image, bg="#2c2c2c")
            image_label.grid(row=0, column=0, pady=(20, 10), sticky="s")
        except tk.TclError as e:
            print(f"Warning: Image not found. Attempted path was '{image_path}'. Error: {e}")
            image_label = tk.Label(self, text="Nechronica", font=("Helvetica", 36), fg="#f0f0f0", bg="#2c2c2c")
            image_label.grid(row=0, column=0, pady=(20, 10), sticky="s")

        # --- Buttons frame ---
        # A separate frame to hold the buttons, for better layout control
        button_frame = tk.Frame(self, bg="#2c2c2c")
        button_frame.grid(row=1, column=0, pady=20)
        
        # --- Button creation ---
        # New Game button
        new_game_button = tk.Button(button_frame, text="New Game", font=("Helvetica", 16),
                                   width=15, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=lambda: print("New Game button clicked"))
        new_game_button.pack(pady=10)
        
        # Database button - Added to switch to the new DatabaseMenu frame
        database_button = tk.Button(button_frame, text="Database", font=("Helvetica", 16),
                                   width=15, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=lambda: self.switch_frame_callback("DatabaseMenu"))
        database_button.pack(pady=10)

        # Options button - Modified to switch to the OptionsMenu frame
        options_button = tk.Button(button_frame, text="Options", font=("Helvetica", 16),
                                   width=15, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=lambda: self.switch_frame_callback("OptionsMenu"))
        options_button.pack(pady=10)
