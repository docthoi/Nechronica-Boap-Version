# database_menu.py

import tkinter as tk
import json # Import json for file operations
import os # Import os for path checking

from enemy_viewer import EnemyViewer # Import EnemyViewer
from game_data import MOCK_ZOMBIE_DATA # Import mock data from the new file

# Define the path for the enemy data file
ENEMY_DATA_FILE = "zombie_data.json"

class DatabaseMenu(tk.Frame):
    """
    A frame representing the database menu, with nested sub-menus.
    """
    def __init__(self, master, switch_frame_callback):
        """
        Initializes the DatabaseMenu frame.

        Args:
            master: The parent widget (the main application window).
            switch_frame_callback: A function to call to switch to another frame.
        """
        super().__init__(master)
        self.master = master
        self.switch_frame_callback = switch_frame_callback
        self.configure(bg="#2c2c2c")

        # Load or create the enemy data file on initialization
        self.zombie_data = self._load_or_create_zombie_data()

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Title Label ---
        title_label = tk.Label(self, text="Database", font=("Helvetica", 24), fg="#f0f0f0", bg="#2c2c2c")
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        
        # --- Container frame for content (main or sub-menus) ---
        self.content_frame = tk.Frame(self, bg="#2c2c2c")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Configure content_frame to hold main buttons on left, viewer on right
        self.content_frame.grid_columnconfigure(0, weight=1) # For main/necromancer buttons
        self.content_frame.grid_columnconfigure(1, weight=2) # For EnemyViewer
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Main Database Buttons Frame ---
        self.main_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_main_buttons(self.main_buttons_frame)
        self.main_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew") 

        # --- Doll Sub-menu Frame ---
        self.doll_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_doll_buttons(self.doll_buttons_frame)

        # --- Necromancer Sub-menu Frame ---
        self.necromancer_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_necromancer_buttons(self.necromancer_buttons_frame)

        # Initialize the new enemy data menu frame (the listbox dropdown)
        self.enemy_data_menu_frame = tk.Frame(self.necromancer_buttons_frame, bg="#2c2c2c", relief="flat", bd=0)
        self._create_enemy_data_menu()

        # --- EnemyViewer Frame (initially hidden) ---
        # Pass self._hide_enemy_viewer as the callback for EnemyViewer's back button
        # Pass the loaded zombie_data to the EnemyViewer
        self.enemy_viewer_frame = EnemyViewer(self.content_frame, self._hide_enemy_viewer, enemy_data=self.zombie_data)
        self.enemy_viewer_frame.grid_forget() # Ensure it starts hidden
        
        # --- Back button for DatabaseMenu itself ---
        back_button = tk.Label(self, text="❮ Back", font=("Helvetica", 12, "underline"),
                             fg="#f0f0f0", bg="#2c2c2c", cursor="hand2")
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        back_button.bind("<Button-1>", lambda e: self.switch_frame_callback("MainMenu"))
        
    def _load_or_create_zombie_data(self):
        """
        Loads zombie data from ENEMY_DATA_FILE or creates it if it doesn't exist.
        """
        if not os.path.exists(ENEMY_DATA_FILE):
            print(f"INFO: {ENEMY_DATA_FILE} not found. Creating with default mock data.")
            try:
                with open(ENEMY_DATA_FILE, 'w') as f:
                    json.dump(MOCK_ZOMBIE_DATA, f, indent=4)
                return MOCK_ZOMBIE_DATA.copy() # Return a copy to avoid direct modification
            except IOError as e:
                print(f"ERROR: Could not create {ENEMY_DATA_FILE}: {e}. Using default mock data in memory.")
                return MOCK_ZOMBIE_DATA.copy()
        else:
            print(f"INFO: {ENEMY_DATA_FILE} found. Loading data.")
            try:
                with open(ENEMY_DATA_FILE, 'r') as f:
                    data = json.load(f)
                return data
            except (IOError, json.JSONDecodeError) as e:
                print(f"ERROR: Could not load {ENEMY_DATA_FILE}: {e}. Using default mock data.")
                return MOCK_ZOMBIE_DATA.copy()

    def _create_main_buttons(self, frame):
        """
        Creates and packs the main database category buttons.
        """
        categories = ["World", "Doll", "Rule", "Necromancer", "Scenario"]
        for category in categories:
            button_container = tk.Frame(frame, bg="#2c2c2c")
            button_container.pack(pady=5, anchor="nw") # Anchor to northwest
            
            if category == "Doll":
                button = tk.Button(button_container, text=category, font=("Helvetica", 16),
                                   width=20, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=self._show_doll_menu)
            elif category == "Necromancer":
                button = tk.Button(button_container, text=category, font=("Helvetica", 16),
                                   width=20, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=self._show_necromancer_menu)
            else:
                button = tk.Button(button_container, text=category, font=("Helvetica", 16),
                                   width=20, pady=5, bg="#555555", fg="#f0f0f0",
                                   relief="raised", bd=3,
                                   command=lambda cat=category: print(f"{cat} button clicked"))
            
            button.pack()
            
    def _create_doll_buttons(self, frame):
        """
        Creates and packs the buttons for the Doll sub-menu.
        """
        title = tk.Label(frame, text="Doll", font=("Helvetica", 18, "bold"), fg="#f0f0f0", bg="#2c2c2c")
        title.pack(padx=20, anchor="w")

        left_aligned_frame = tk.Frame(frame, bg="#2c2c2c")
        left_aligned_frame.pack(fill="x", padx=20)

        button_configs = [
            ("Sample Characters", lambda: print("Sample Characters clicked")),
            ("Doll Creation", lambda: print("Doll Creation clicked")),
            ("Fragments of Memory", lambda: print("Fragments of Memory clicked")),
            ("Classes", self._toggle_classes_menu),
            ("Maneuvers", lambda: print("Maneuvers clicked")),
            ("Basic Parts", lambda: print("Basic Parts clicked")),
            ("Reinforcement Parts", self._toggle_reinforcement_parts_menu),
            ("Positions", self._toggle_positions_menu),
        ]

        self.dropdown_buttons = {}
        for text, command in button_configs:
            button = tk.Button(left_aligned_frame, text=text, font=("Helvetica", 12),
                               width=25, pady=3, bg="#555555", fg="#f0f0f0",
                               relief="raised", bd=3, command=command)
            button.pack(pady=3, anchor="w")
            if text in ["Positions", "Reinforcement Parts", "Classes"]:
                self.dropdown_buttons[text] = button

        self.positions_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)
        self.reinforcement_parts_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)
        self.classes_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)

        self._create_positions_menu()
        self._create_reinforcement_parts_menu()
        self._create_classes_menu()

        sub_menu_back_button = tk.Button(frame, text="❮ Back to Database", font=("Helvetica", 12),
                                         width=25, pady=5, bg="#555555", fg="#f0f0f0",
                                         relief="raised", bd=3,
                                         command=self._show_main_menu)
        sub_menu_back_button.pack(pady=(20, 5), padx=20, anchor="w")

    def _create_necromancer_buttons(self, frame):
        """
        Creates and packs the buttons for the Necromancer sub-menu.
        """
        title = tk.Label(frame, text="Necromancer", font=("Helvetica", 18, "bold"), fg="#f0f0f0", bg="#2c2c2c")
        title.pack(padx=20, pady=(0, 10), anchor="w")

        left_aligned_frame = tk.Frame(frame, bg="#2c2c2c")
        left_aligned_frame.pack(fill="x", padx=20)

        button_configs = [
            ("The Necromancer's Minions", lambda: print("The Necromancer's Minions clicked")),
            ("Enemy Data", self._toggle_enemy_data_menu),
            ("Creating Enemies", lambda: print("Creating Enemies clicked")),
            ("Enemy Exclusive Parts", lambda: print("Enemy Exclusive Parts clicked")),
            ("Group Management", lambda: print("Group Management clicked")),
            ("Scripting", lambda: print("Scripting clicked")),
            ("Styles of play", lambda: print("Styles of play clicked")),
        ]

        self.necromancer_dropdown_buttons = {}
        for text, command in button_configs:
            button = tk.Button(left_aligned_frame, text=text, font=("Helvetica", 12),
                               width=25, pady=3, bg="#555555", fg="#f0f0f0",
                               relief="raised", bd=3, command=command)
            button.pack(pady=3, anchor="w")
            if text == "Enemy Data":
                self.necromancer_dropdown_buttons[text] = button # Store reference to the button
        
        sub_menu_back_button = tk.Button(frame, text="❮ Back to Database", font=("Helvetica", 12),
                                         width=25, pady=5, bg="#555555", fg="#f0f0f0",
                                         relief="raised", bd=3,
                                         command=self._show_main_menu)
        sub_menu_back_button.pack(pady=(20, 5), padx=20, anchor="w")

    def _create_positions_menu(self):
        """
        Creates the entries for the Positions custom dropdown menu.
        """
        positions_menu_items = [
            "۶ Alice", "۶ Automaton", "۶ Court", "۶ Dolls", "۶ Junk", "۶ Sorority"
        ]
        
        for item in positions_menu_items:
            label = tk.Label(self.positions_menu_frame, text=item, font=("Helvetica", 12),
                             fg="#f0f0f0", bg="#2c2c2c", anchor="w", cursor="hand2")
            label.pack(fill="x", padx=5)
            label.bind("<Enter>", lambda e, l=label: l.configure(bg="#444444"))
            label.bind("<Leave>", lambda e, l=label: l.configure(bg="#2c2c2c"))
            label.bind("<Button-1>", lambda e, opt=item, l=label: self._on_menu_item_click(opt, l))

    def _create_reinforcement_parts_menu(self):
        """
        Creates the entries for the Reinforcement Parts custom dropdown menu.
        """
        reinforcement_parts_menu_items = [
            "۶ Armaments", "۶ Mutations", "۶ Enhancements"
        ]

        for item in reinforcement_parts_menu_items:
            label = tk.Label(self.reinforcement_parts_menu_frame, text=item, font=("Helvetica", 12),
                             fg="#f0f0f0", bg="#2c2c2c", anchor="w", cursor="hand2")
            label.pack(fill="x", padx=5)
            label.bind("<Enter>", lambda e, l=label: l.configure(bg="#444444"))
            label.bind("<Leave>", lambda e, l=label: l.configure(bg="#2c2c2c"))
            label.bind("<Button-1>", lambda e, opt=item, l=label: self._on_menu_item_click(opt, l))

    def _create_classes_menu(self):
        """
        Creates the entries for the Classes custom dropdown menu.
        """
        classes_menu_items = [
            "۶ Baroque", "۶ Gothic", "۶ Requiem", "۶ Romanesque", "۶ Stacy", "۶ Thanatos"
        ]

        for item in classes_menu_items:
            label = tk.Label(self.classes_menu_frame, text=item, font=("Helvetica", 12),
                             fg="#f0f0f0", bg="#2c2c2c", anchor="w", cursor="hand2")
            label.pack(fill="x", padx=5)
            label.bind("<Enter>", lambda e, l=label: l.configure(bg="#444444"))
            label.bind("<Leave>", lambda e, l=label: l.configure(bg="#2c2c2c"))
            label.bind("<Button-1>", lambda e, opt=item, l=label: self._on_menu_item_click(opt, l))
    
    def _create_enemy_data_menu(self):
        """
        Creates the entries for the Enemy Data custom dropdown menu with a scrollbar.
        """
        list_frame = tk.Frame(self.enemy_data_menu_frame, bg="#2c2c2c")
        list_frame.pack(fill="x")
        
        enemy_data_items = [
            "۶ Zombie", "۶ Skeleton", "۶ Ghoul", "۶ Wight", "۶ Lich",
            "۶ Banshee", "۶ Wraith", "۶ Vampire", "۶ Werewolf", "۶ Chimera",
            "۶ Hydra", "۶ Dragon", "۶ Basilisk"
        ]

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        
        self.enemy_listbox = tk.Listbox(list_frame, height=4, font=("Helvetica", 12),
                                       fg="#f0f0f0", bg="#2c2c2c",
                                       selectbackground="#3498db", selectforeground="#ecf0f0",
                                       yscrollcommand=scrollbar.set, relief="flat", bd=0,
                                       highlightthickness=0)
        
        scrollbar.config(command=self.enemy_listbox.yview)

        scrollbar.pack(side="right", fill="y")
        self.enemy_listbox.pack(side="left", fill="both", expand=True)
        
        for item in enemy_data_items:
            self.enemy_listbox.insert(tk.END, item)
        
        self.enemy_listbox.bind("<<ListboxSelect>>", self._on_enemy_selected)

    def _on_enemy_selected(self, event):
        """
        Handles the event when an enemy is selected from the listbox.
        """
        selected_index = self.enemy_listbox.curselection()
        if selected_index:
            selected_item = self.enemy_listbox.get(selected_index[0])
            print(f"Enemy selected: {selected_item}")

            # Check if the selected item is "۶ Zombie" and display its data
            if selected_item == "۶ Zombie":
                # Pass the loaded zombie_data to the viewer
                self._show_enemy_viewer(self.zombie_data)
            else:
                print(f"Viewer for {selected_item} not yet implemented.")


    def _on_menu_item_click(self, item, label):
        """
        Handles clicks on the custom dropdown menu items and provides a visual cue.
        """
        print(f"{item} selected")
        label.configure(bg="#666666")
        self.after(200, lambda: label.configure(bg="#444444"))
        
    def _toggle_positions_menu(self):
        """
        Toggles the visibility of the custom positions dropdown menu.
        """
        if self.positions_menu_frame.winfo_ismapped():
            self.positions_menu_frame.pack_forget()
        else:
            if self.reinforcement_parts_menu_frame.winfo_ismapped():
                self.reinforcement_parts_menu_frame.pack_forget()
            if self.classes_menu_frame.winfo_ismapped():
                self.classes_menu_frame.pack_forget()
            self.positions_menu_frame.pack(padx=10, pady=(0, 5), anchor="w")

    def _toggle_reinforcement_parts_menu(self):
        """
        Toggles the visibility of the custom reinforcement parts dropdown menu.
        """
        if self.reinforcement_parts_menu_frame.winfo_ismapped():
            self.reinforcement_parts_menu_frame.pack_forget()
        else:
            if self.positions_menu_frame.winfo_ismapped():
                self.positions_menu_frame.pack_forget()
            if self.classes_menu_frame.winfo_ismapped():
                self.classes_menu_frame.pack_forget()
            self.reinforcement_parts_menu_frame.pack(padx=10, pady=(0, 5), anchor="w")

    def _toggle_classes_menu(self):
        """
        Toggles the visibility of the custom classes dropdown menu.
        """
        if self.classes_menu_frame.winfo_ismapped():
            self.classes_menu_frame.pack_forget()
        else:
            if self.positions_menu_frame.winfo_ismapped():
                self.positions_menu_frame.pack_forget()
            if self.reinforcement_parts_menu_frame.winfo_ismapped():
                self.reinforcement_parts_menu_frame.pack_forget()
            self.classes_menu_frame.pack(padx=10, pady=(0, 5), anchor="w")

    def _toggle_enemy_data_menu(self):
        """
        Toggles the visibility of the custom enemy data dropdown menu.
        """
        if self.enemy_data_menu_frame.winfo_ismapped():
            self.enemy_data_menu_frame.pack_forget()
            self._hide_enemy_viewer() # If hiding enemy data list, hide viewer too
        else:
            if self.positions_menu_frame.winfo_ismapped():
                self.positions_menu_frame.pack_forget()
            if self.reinforcement_parts_menu_frame.winfo_ismapped():
                self.reinforcement_parts_menu_frame.pack_forget()
            if self.classes_menu_frame.winfo_ismapped():
                self.classes_menu_frame.pack_forget()

            self.enemy_data_menu_frame.pack(after=self.necromancer_dropdown_buttons["Enemy Data"], padx=10, pady=(0, 5), anchor="w")
        
    def _show_doll_menu(self):
        """
        Hides all other content and shows the doll sub-menu.
        """
        print("DEBUG: _show_doll_menu called.")
        self._hide_all_main_content_frames()
        self.doll_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        print(f"DEBUG: doll_buttons_frame gridded. Is mapped: {self.doll_buttons_frame.winfo_ismapped()}")
        print(f"DEBUG: Children of doll_buttons_frame: {[w.winfo_class() for w in self.doll_buttons_frame.winfo_children()]}")

    def _show_necromancer_menu(self):
        """
        Hides all other content and shows the necromancer sub-menu.
        """
        print("DEBUG: _show_necromancer_menu called.")
        self._hide_all_main_content_frames()
        self.necromancer_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        print(f"DEBUG: necromancer_buttons_frame gridded. Is mapped: {self.necromancer_buttons_frame.winfo_ismapped()}")

    def _show_main_menu(self):
        """
        Hides all other content and displays the main database menu.
        """
        print("DEBUG: _show_main_menu called.")
        self._hide_all_main_content_frames() # This now hides everything cleanly
        self.main_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        print(f"DEBUG: main_buttons_frame gridded. Is mapped: {self.main_buttons_frame.winfo_ismapped()}")

    def _hide_all_main_content_frames(self):
        """Helper to hide all main content frames (main, doll, necromancer, enemy viewer) and their dropdowns."""
        print("DEBUG: _hide_all_main_content_frames called.")
        self.main_buttons_frame.grid_forget()
        self.doll_buttons_frame.grid_forget()
        self.necromancer_buttons_frame.grid_forget()
        self.enemy_viewer_frame.grid_forget()
        # Also hide any currently open dropdowns, regardless of which main menu is active
        if self.positions_menu_frame.winfo_ismapped():
            self.positions_menu_frame.pack_forget()
        if self.reinforcement_parts_menu_frame.winfo_ismapped():
            self.reinforcement_parts_menu_frame.pack_forget()
        if self.classes_menu_frame.winfo_ismapped():
            self.classes_menu_frame.pack_forget()
        if self.enemy_data_menu_frame.winfo_ismapped():
            self.enemy_data_menu_frame.pack_forget()
        print("DEBUG: All main content frames and dropdowns hidden.")

    def _show_enemy_viewer(self, enemy_data):
        """
        Displays the EnemyViewer in the right column.
        The necromancer buttons frame remains visible in the left column.
        """
        # Ensure the necromancer menu is visible in column 0
        self.necromancer_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.enemy_viewer_frame.display_enemy_data(enemy_data) # Update viewer with data
        # Grid the viewer into column 1, leaving column 0 for the necromancer menu
        self.enemy_viewer_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew") 

    def _hide_enemy_viewer(self):
        """
        Hides the EnemyViewer frame.
        """
        self.enemy_viewer_frame.grid_forget()
        # When the viewer is hidden, ensure the necromancer menu is visible on the left
        self.necromancer_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # Also ensure the enemy data list is visible if it was open
        if not self.enemy_data_menu_frame.winfo_ismapped():
             self.enemy_data_menu_frame.pack(after=self.necromancer_dropdown_buttons["Enemy Data"], padx=10, pady=(0, 5), anchor="w")

    def _hide_all_dropdown_menus_in_necromancer(self):
        """Helper to hide all dropdown menus within the necromancer section."""
        if self.enemy_data_menu_frame.winfo_ismapped():
            self.enemy_data_menu_frame.pack_forget()
