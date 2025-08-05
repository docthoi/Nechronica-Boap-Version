# database_menu.py

import tkinter as tk

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

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Title Label ---
        # The main title is centered, so no padx is needed here
        title_label = tk.Label(self, text="Database", font=("Helvetica", 24), fg="#f0f0f0", bg="#2c2c2c")
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        
        # --- Container frame for content (main or sub-menus) ---
        self.content_frame = tk.Frame(self, bg="#2c2c2c")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Main Database Buttons Frame ---
        self.main_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_main_buttons(self.main_buttons_frame)
        # Added padx to give the main button block a left margin
        self.main_buttons_frame.pack(padx=20, anchor="nw")
        
        # --- Doll Sub-menu Frame ---
        self.doll_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_doll_buttons(self.doll_buttons_frame)

        # --- Necromancer Sub-menu Frame ---
        self.necromancer_buttons_frame = tk.Frame(self.content_frame, bg="#2c2c2c")
        self._create_necromancer_buttons(self.necromancer_buttons_frame)

        # Initialize the new enemy data menu frame here, but don't pack it yet
        self.enemy_data_menu_frame = tk.Frame(self.necromancer_buttons_frame, bg="#2c2c2c", relief="flat", bd=0)
        self._create_enemy_data_menu()
        
        # --- Back button ---
        # The back button is now moved to the top-left corner
        back_button = tk.Label(self, text="❮ Back", font=("Helvetica", 12, "underline"),
                             fg="#f0f0f0", bg="#2c2c2c", cursor="hand2")
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        back_button.bind("<Button-1>", lambda e: self.switch_frame_callback("MainMenu"))
        
    def _create_main_buttons(self, frame):
        """
        Creates and packs the main database category buttons.
        """
        categories = ["World", "Doll", "Rule", "Necromancer", "Scenario"]
        for category in categories:
            # We use a nested frame for each button to better center them
            button_container = tk.Frame(frame, bg="#2c2c2c")
            button_container.pack(pady=5)
            
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
        # Align the "Doll" title to the left with padding
        title = tk.Label(frame, text="Doll", font=("Helvetica", 18, "bold"), fg="#f0f0f0", bg="#2c2c2c")
        title.pack(padx=20, anchor="w")

        # Frame to hold the buttons for left alignment, with padding
        left_aligned_frame = tk.Frame(frame, bg="#2c2c2c")
        left_aligned_frame.pack(fill="x", padx=20)

        # A list of button configurations, including custom dropdown menus
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

        # Create buttons and store references for dropdown positioning
        self.dropdown_buttons = {}
        for text, command in button_configs:
            button = tk.Button(left_aligned_frame, text=text, font=("Helvetica", 12),
                               width=25, pady=3, bg="#555555", fg="#f0f0f0",
                               relief="raised", bd=3, command=command)
            button.pack(pady=3, anchor="w")
            # Store buttons that have associated dropdowns for later use
            if text in ["Positions", "Reinforcement Parts", "Classes"]:
                self.dropdown_buttons[text] = button

        # Initialize custom menu frames
        self.positions_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)
        self.reinforcement_parts_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)
        self.classes_menu_frame = tk.Frame(left_aligned_frame, bg="#2c2c2c", relief="flat", bd=0)

        # Create the content for each dropdown menu
        self._create_positions_menu()
        self._create_reinforcement_parts_menu()
        self._create_classes_menu()

        # Add a back button for the sub-menu with padding
        sub_menu_back_button = tk.Button(frame, text="❮ Back to Database", font=("Helvetica", 12),
                                         width=25, pady=5, bg="#555555", fg="#f0f0f0",
                                         relief="raised", bd=3,
                                         command=self._show_main_menu)
        sub_menu_back_button.pack(pady=(20, 5), padx=20, anchor="w")

    def _create_necromancer_buttons(self, frame):
        """
        Creates and packs the buttons for the Necromancer sub-menu.
        """
        # Align the "Necromancer" title to the left with padding
        title = tk.Label(frame, text="Necromancer", font=("Helvetica", 18, "bold"), fg="#f0f0f0", bg="#2c2c2c")
        title.pack(padx=20, pady=(0, 10), anchor="w")

        # Frame to hold the buttons for left alignment, with padding
        left_aligned_frame = tk.Frame(frame, bg="#2c2c2c")
        left_aligned_frame.pack(fill="x", padx=20)

        # A list of button configurations
        button_configs = [
            ("The Necromancer's Minions", lambda: print("The Necromancer's Minions clicked")),
            ("Enemy Data", self._toggle_enemy_data_menu),
            ("Creating Enemies", lambda: print("Creating Enemies clicked")),
            ("Enemy Exclusive Parts", lambda: print("Enemy Exclusive Parts clicked")),
            ("Group Management", lambda: print("Group Management clicked")),
            ("Scripting", lambda: print("Scripting clicked")),
            ("Styles of play", lambda: print("Styles of play clicked")),
        ]

        # Create buttons
        self.necromancer_dropdown_buttons = {}
        for text, command in button_configs:
            button = tk.Button(left_aligned_frame, text=text, font=("Helvetica", 12),
                               width=25, pady=3, bg="#555555", fg="#f0f0f0",
                               relief="raised", bd=3, command=command)
            button.pack(pady=3, anchor="w")
            if text == "Enemy Data":
                self.necromancer_dropdown_buttons["Enemy Data"] = button
        
        # Add a back button for the sub-menu with padding
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
            # Add hover and click effects
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
            # Add hover and click effects
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
            # Add hover and click effects
            label.bind("<Enter>", lambda e, l=label: l.configure(bg="#444444"))
            label.bind("<Leave>", lambda e, l=label: l.configure(bg="#2c2c2c"))
            label.bind("<Button-1>", lambda e, opt=item, l=label: self._on_menu_item_click(opt, l))
    
    def _create_enemy_data_menu(self):
        """
        Creates the entries for the Enemy Data custom dropdown menu with a scrollbar.
        """
        # A frame to hold the Listbox and Scrollbar
        list_frame = tk.Frame(self.enemy_data_menu_frame, bg="#2c2c2c")
        list_frame.pack(fill="x")
        
        # Placeholder enemy data list
        enemy_data_items = [
            "۶ Zombie", "۶ Skeleton", "۶ Ghoul", "۶ Wight", "۶ Lich",
            "۶ Banshee", "۶ Wraith", "۶ Vampire", "۶ Werewolf", "۶ Chimera",
            "۶ Hydra", "۶ Dragon", "۶ Basilisk"
        ]

        # Create a scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        
        # Create a listbox to hold the enemy data, with a limited height
        self.enemy_listbox = tk.Listbox(list_frame, height=4, font=("Helvetica", 12),
                                       fg="#f0f0f0", bg="#2c2c2c",
                                       selectbackground="#3498db", selectforeground="#ecf0f1",
                                       yscrollcommand=scrollbar.set, relief="flat", bd=0,
                                       highlightthickness=0)
        
        # Link the scrollbar to the listbox
        scrollbar.config(command=self.enemy_listbox.yview)

        # Pack the scrollbar and listbox
        scrollbar.pack(side="right", fill="y")
        self.enemy_listbox.pack(side="left", fill="both", expand=True)
        
        # Insert the enemy data items into the listbox
        for item in enemy_data_items:
            self.enemy_listbox.insert(tk.END, item)
        
        # Bind a click event to the listbox
        self.enemy_listbox.bind("<<ListboxSelect>>", self._on_enemy_selected)

    def _on_enemy_selected(self, event):
        """
        Handles the event when an enemy is selected from the listbox.
        """
        selected_index = self.enemy_listbox.curselection()
        if selected_index:
            selected_item = self.enemy_listbox.get(selected_index[0])
            print(f"Enemy selected: {selected_item}")

    def _on_menu_item_click(self, item, label):
        """
        Handles clicks on the custom dropdown menu items and provides a visual cue.
        """
        print(f"{item} selected")
        # Provide a momentary visual highlight for the click
        label.configure(bg="#666666")
        self.after(200, lambda: label.configure(bg="#444444"))
        
    def _toggle_positions_menu(self):
        """
        Toggles the visibility of the custom positions dropdown menu.
        """
        if self.positions_menu_frame.winfo_ismapped():
            self.positions_menu_frame.pack_forget()
        else:
            # Hide other menus if they are open
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
            # Hide other menus
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
            # Hide other menus
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
        else:
            # Hide other dropdown menus from the doll menu if they're open
            if self.positions_menu_frame.winfo_ismapped():
                self.positions_menu_frame.pack_forget()
            if self.reinforcement_parts_menu_frame.winfo_ismapped():
                self.reinforcement_parts_menu_frame.pack_forget()
            if self.classes_menu_frame.winfo_ismapped():
                self.classes_menu_frame.pack_forget()

            # Use pack(after=...) to place the menu correctly
            self.enemy_data_menu_frame.pack(after=self.necromancer_dropdown_buttons["Enemy Data"], padx=10, pady=(0, 5), anchor="w")
        
    def _show_doll_menu(self):
        """
        Hides the main database menu and shows the doll sub-menu.
        """
        self.main_buttons_frame.pack_forget()
        # Added padx here for a consistent left margin
        self.doll_buttons_frame.pack(padx=20, anchor="nw")
        
    def _show_necromancer_menu(self):
        """
        Hides the main database menu and shows the necromancer sub-menu.
        """
        self.main_buttons_frame.pack_forget()
        # Added padx here for a consistent left margin
        self.necromancer_buttons_frame.pack(padx=20, anchor="nw")

    def _show_main_menu(self):
        """
        Hides the doll and necromancer sub-menus and their respective dropdowns, then shows the main database menu.
        """
        # First, ensure all dropdown menus are hidden
        if self.positions_menu_frame.winfo_ismapped():
            self.positions_menu_frame.pack_forget()
        if self.reinforcement_parts_menu_frame.winfo_ismapped():
            self.reinforcement_parts_menu_frame.pack_forget()
        if self.classes_menu_frame.winfo_ismapped():
            self.classes_menu_frame.pack_forget()
        if self.enemy_data_menu_frame.winfo_ismapped():
            self.enemy_data_menu_frame.pack_forget()
            
        self.doll_buttons_frame.pack_forget()
        self.necromancer_buttons_frame.pack_forget()
        # The main menu also needs padding
        self.main_buttons_frame.pack(padx=20, anchor="nw")
