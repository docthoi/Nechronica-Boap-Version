# enemy_viewer.py

import tkinter as tk
from tkinter import scrolledtext # For multi-line text with scrollbars
import json # To load and save enemy data
import os # For file path operations

# Define the path for the mock enemy data file
# In a real game, this would likely be managed by a data loading system
ENEMY_DATA_FILE = "zombie_data.json"

class EnemyViewer(tk.Frame):
    """
    A frame representing the detailed viewer for a single enemy statblock.
    Allows editing and saving of the statblock data.
    """
    def __init__(self, master, back_to_parent_callback, enemy_data=None):
        """
        Initializes the EnemyViewer frame.

        Args:
            master: The parent widget (the main application window or content frame).
            back_to_parent_callback: A function to call to return to the parent menu.
            enemy_data (dict, optional): The dictionary containing the enemy's statblock data.
                                         Defaults to None, in which case a placeholder is shown.
        """
        super().__init__(master)
        self.master = master
        self.back_to_parent_callback = back_to_parent_callback # Changed callback name for clarity
        self.current_enemy_data = enemy_data # Store the data being displayed/edited
        self.configure(bg="#2c2c2c")

        # Dictionary to hold references to editable Tkinter variables/widgets
        self.editable_fields = {}

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=0) # For the back button/title/save button
        self.grid_rowconfigure(1, weight=1) # For the main content area
        self.grid_columnconfigure(0, weight=1)

        # --- Top Bar Frame (for Back and Save buttons) ---
        top_bar_frame = tk.Frame(self, bg="#2c2c2c")
        top_bar_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        top_bar_frame.grid_columnconfigure(0, weight=1) # Back button column
        top_bar_frame.grid_columnconfigure(1, weight=1) # Save button column

        # --- Back button ---
        back_button = tk.Label(top_bar_frame, text="❮ Back to Enemy Data", font=("Helvetica", 12, "underline"),
                               fg="#f0f0f0", bg="#2c2c2c", cursor="hand2")
        back_button.grid(row=0, column=0, sticky="nw")
        back_button.bind("<Button-1>", lambda e: self.back_to_parent_callback())

        # --- Save Changes button ---
        save_button = tk.Button(top_bar_frame, text="Save Changes", font=("Helvetica", 12),
                                width=15, pady=5, bg="#444444", fg="#f0f0f0",
                                relief="raised", bd=3,
                                command=self._collect_and_save_data)
        save_button.grid(row=0, column=1, sticky="ne")


        # --- Main content frame for enemy details ---
        self.detail_frame = tk.Frame(self, bg="#cccccc", padx=20, pady=20, relief="raised", bd=3)
        self.detail_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.detail_frame.grid_columnconfigure(0, weight=1)

        self.display_enemy_data(self.current_enemy_data)

    def display_enemy_data(self, enemy_data):
        """
        Populates the viewer with the provided enemy data, creating editable fields.
        Clears previous data if any.
        """
        print("DEBUG: display_enemy_data called.")
        # Clear existing widgets in the detail_frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        self.editable_fields = {} # Reset editable fields dictionary
        print(f"DEBUG: editable_fields reset: {self.editable_fields}")

        if not enemy_data:
            tk.Label(self.detail_frame, text="No enemy data to display.", font=("Helvetica", 16),
                     fg="black", bg="#cccccc").pack(pady=50)
            return

        self.current_enemy_data = enemy_data # Update current data

        # --- Enemy Name (Editable) ---
        # The name itself is now an Entry, but the surrounding "panel" is raised
        name_frame = tk.Frame(self.detail_frame, bg="#cccccc", relief="raised", bd=3)
        name_frame.pack(pady=(0, 15), fill="x")
        name_frame.grid_columnconfigure(0, weight=1) # Allow entry to expand

        name_var = tk.StringVar(value=enemy_data.get("name", "Unknown Enemy"))
        name_entry = tk.Entry(name_frame, textvariable=name_var,
                              font=("Quantico", 22, "bold"), fg="black", bg="#cccccc",
                              justify="center", relief="flat", bd=0) # Flat relief to blend with frame
        name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.editable_fields["name"] = name_var


        # --- Basic Info Section (Horizontal Layout) ---
        basic_info_panel_frame = tk.Frame(self.detail_frame, bg="#cccccc", padx=10, pady=10, relief="raised", bd=2)
        basic_info_panel_frame.pack(fill="x", pady=5)
        
        # Use a grid for horizontal arrangement of object-value pairs
        basic_info_panel_frame.grid_columnconfigure(0, weight=1) # ID Object
        basic_info_panel_frame.grid_columnconfigure(1, weight=1) # ID Value
        basic_info_panel_frame.grid_columnconfigure(2, weight=1) # Threat Level (Base) Object
        basic_info_panel_frame.grid_columnconfigure(3, weight=1) # Threat Level (Base) Value
        basic_info_panel_frame.grid_columnconfigure(4, weight=1) # Threat Level (Per Spawn Group) Object
        basic_info_panel_frame.grid_columnconfigure(5, weight=1) # Threat Level (Per Spawn Group) Value
        basic_info_panel_frame.grid_columnconfigure(6, weight=1) # Max Action Points Object
        basic_info_panel_frame.grid_columnconfigure(7, weight=1) # Max Action Points Value

        # Explicitly create ID field to ensure it's always added
        id_obj_label = tk.Label(basic_info_panel_frame, text="ID:",
                                 font=("Quantico", 10, "bold"), fg="black", bg="#cccccc",
                                 relief="raised", bd=2)
        id_obj_label.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        
        id_value_var = tk.StringVar(value=str(enemy_data.get('id', 'N/A')))
        id_value_entry = tk.Entry(basic_info_panel_frame, textvariable=id_value_var,
                                   font=("Helvetica", 10), fg="#f0f0f0", bg="#5a5a5a",
                                   relief="sunken", bd=2, justify="center")
        id_value_entry.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.editable_fields["id"] = id_value_var
        print(f"DEBUG: 'id' key added to editable_fields (explicitly): id -> {id_value_var.get()}")
        print(f"DEBUG: editable_fields after explicit 'id' add: {list(self.editable_fields.keys())}")


        # Helper function to create an "object" (label) and its "value" (entry)
        def create_horizontal_info_pair(parent_frame, col_offset, obj_text, value_key, initial_value):
            # Object label (raised) - part of the embossed panel
            obj_label = tk.Label(parent_frame, text=obj_text,
                                 font=("Quantico", 10, "bold"), fg="black", bg="#cccccc",
                                 relief="raised", bd=2)
            obj_label.grid(row=0, column=col_offset, padx=2, pady=2, sticky="ew")
            
            # Value Entry (sunken/debossed)
            value_var = tk.StringVar(value=str(initial_value))
            value_entry = tk.Entry(parent_frame, textvariable=value_var,
                                   font=("Helvetica", 10), fg="#f0f0f0", bg="#5a5a5a",
                                   relief="sunken", bd=2, justify="center")
            value_entry.grid(row=1, column=col_offset, padx=2, pady=2, sticky="ew")
            self.editable_fields[value_key] = value_var


        threat_level = enemy_data.get("threatLevel", {})
        
        # Arrange horizontally (ID is now created explicitly above)
        create_horizontal_info_pair(basic_info_panel_frame, 2, "Threat Level (Base):", "threatLevel_base", threat_level.get('base', 'N/A'))
        create_horizontal_info_pair(basic_info_panel_frame, 4, "Threat Level (Per Spawn Group):", "threatLevel_per_spawn_group", threat_level.get('per_spawn_group', 'N/A'))
        create_horizontal_info_pair(basic_info_panel_frame, 6, "Max Action Points:", "maximumActionPoints", enemy_data.get('maximumActionPoints', 'N/A'))


        # --- Maneuvers Section ---
        maneuvers_heading = tk.Label(self.detail_frame, text="Maneuvers",
                                     font=("Quantico", 16, "bold"), fg="black", bg="#cccccc",
                                     relief="raised", bd=3)
        maneuvers_heading.pack(pady=(15, 5), anchor="w", fill="x")
        
        maneuvers_panel_frame = tk.Frame(self.detail_frame, bg="#cccccc", padx=10, pady=10, relief="raised", bd=2)
        maneuvers_panel_frame.pack(fill="x", pady=5)

        maneuvers = enemy_data.get("maneuvers", [])
        self.editable_fields["maneuvers"] = [] # Store maneuver data as a list of dicts/vars
        
        if maneuvers:
            for i, maneuver in enumerate(maneuvers):
                maneuver_data = {} # To store variables for this specific maneuver
                self.editable_fields["maneuvers"].append(maneuver_data)

                # Maneuver ID label (object - raised)
                maneuver_id_label = tk.Label(maneuvers_panel_frame, text=f"{i+1}. {maneuver.get('id', 'N/A')}",
                                             font=("Quantico", 12, "bold", "underline"), fg="black", bg="#cccccc",
                                             relief="raised", bd=2)
                maneuver_id_label.pack(anchor="w", pady=(5, 0))

                detail_frame_inner = tk.Frame(maneuvers_panel_frame, bg="#cccccc", padx=5, pady=5, relief="raised", bd=1) # Changed bg and relief
                detail_frame_inner.pack(fill="x", padx=10, pady=2)
                detail_frame_inner.grid_columnconfigure(0, weight=0)
                detail_frame_inner.grid_columnconfigure(1, weight=1)

                row_idx = 0
                def add_editable_detail_row(parent, label_text, value_key, initial_value, is_text_area=False):
                    nonlocal row_idx
                    tk.Label(parent, text=label_text, font=("Quantico", 10, "bold"), fg="black", bg="#cccccc").grid(row=row_idx, column=0, sticky="w", padx=2) # Changed font/fg/bg
                    
                    if is_text_area:
                        text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=3,
                                                               font=("Helvetica", 10), fg="#f0f0f0", bg="#5a5a5a",
                                                               insertbackground="#f0f0f0", relief="sunken", bd=1)
                        text_widget.insert(tk.END, str(initial_value))
                        text_widget.grid(row=row_idx, column=1, sticky="ew", padx=2, pady=2)
                        maneuver_data[value_key] = text_widget # Store widget reference directly
                    else:
                        value_var = tk.StringVar(value=str(initial_value))
                        value_entry = tk.Entry(parent, textvariable=value_var,
                                               font=("Helvetica", 10), fg="#f0f0f0", bg="#5a5a5a",
                                               relief="sunken", bd=1)
                        value_entry.grid(row=row_idx, column=1, sticky="ew", padx=2, pady=2)
                        maneuver_data[value_key] = value_var # Store StringVar reference
                    row_idx += 1

                add_editable_detail_row(detail_frame_inner, "Timing:", "timing", maneuver.get('timing', 'N/A'))
                add_editable_detail_row(detail_frame_inner, "Cost:", "cost", maneuver.get('cost', 'N/A'))
                add_editable_detail_row(detail_frame_inner, "Range:", "range", maneuver.get('range', 'N/A'))
                add_editable_detail_row(detail_frame_inner, "Description:", "description", maneuver.get('description', 'No description.'), is_text_area=True)
                
                damage = maneuver.get('damage', {})
                if damage:
                    add_editable_detail_row(detail_frame_inner, "Base Damage:", "damage_base_damage", damage.get('base_damage', 'N/A'))
                    add_editable_detail_row(detail_frame_inner, "Effect:", "damage_effect", damage.get('effect', 'N/A'))
                    if "formula" in damage: # Only add if formula exists
                        add_editable_detail_row(detail_frame_inner, "Formula:", "damage_formula", damage.get('formula', 'N/A'))
                
                tk.Frame(maneuvers_panel_frame, height=1, bg="#555555").pack(fill="x", pady=5) # Separator
        else:
            tk.Label(maneuvers_panel_frame, text="No maneuvers listed.", font=("Helvetica", 10),
                     fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")

        # --- Flavor Text Section ---
        flavor_heading = tk.Label(self.detail_frame, text="Flavor Text",
                                  font=("Quantico", 16, "bold"), fg="black", bg="#cccccc",
                                  relief="raised", bd=3)
        flavor_heading.pack(pady=(15, 5), anchor="w", fill="x")
        
        flavor = enemy_data.get("flavor", {})
        
        # Using ScrolledText for potentially long flavor descriptions (debossed)
        flavor_text_widget = scrolledtext.ScrolledText(self.detail_frame, wrap=tk.WORD, height=5,
                                                     font=("Helvetica", 10), fg="#f0f0f0", bg="#5a5a5a",
                                                     insertbackground="#f0f0f0", relief="sunken", bd=2)
        flavor_text_widget.pack(fill="x", pady=5)
        flavor_text_widget.insert(tk.END, f"Description:\n{flavor.get('description', 'N/A')}\n\n")
        flavor_text_widget.insert(tk.END, f"Tactics:\n{flavor.get('tactics', 'N/A')}\n\n")
        flavor_text_widget.insert(tk.END, f"Roleplay:\n{flavor.get('roleplay', 'N/A')}")
        self.editable_fields["flavor_text"] = flavor_text_widget # Store widget reference

    def _collect_and_save_data(self):
        """
        Collects data from all editable fields and saves it to the JSON file.
        """
        print(f"DEBUG: _collect_and_save_data called. Type of editable_fields: {type(self.editable_fields)}. editable_fields keys: {list(self.editable_fields.keys())}")
        updated_data = {}

        try:
            # Retrieve 'id' and 'name' before the main try block for robustness
            enemy_id = self.editable_fields["id"].get()
            enemy_name = self.editable_fields["name"].get()

            print(f"DEBUG: Retrieved ID: {enemy_id}, Name: {enemy_name}")

            updated_data["id"] = enemy_id
            updated_data["name"] = enemy_name
            
            # Safely convert to int, handle potential ValueError
            threat_base = 0
            try:
                threat_base = int(self.editable_fields["threatLevel_base"].get())
            except ValueError:
                print("Warning: Threat Level (Base) is not a valid number. Using 0.")
            
            threat_per_spawn = 0
            try:
                threat_per_spawn = int(self.editable_fields["threatLevel_per_spawn_group"].get())
            except ValueError:
                print("Warning: Threat Level (Per Spawn Group) is not a valid number. Using 0.")

            max_ap = 0
            try:
                max_ap = int(self.editable_fields["maximumActionPoints"].get())
            except ValueError:
                print("Warning: Maximum Action Points is not a valid number. Using 0.")

            updated_data["threatLevel"] = {
                "base": threat_base,
                "per_spawn_group": threat_per_spawn
            }
            updated_data["maximumActionPoints"] = max_ap

            # Collect maneuvers
            updated_maneuvers = []
            for maneuver_vars in self.editable_fields["maneuvers"]:
                maneuver = {
                    "id": maneuver_vars["id"].get() if isinstance(maneuver_vars["id"], tk.StringVar) else maneuver_vars["id"].cget("text"),
                    "timing": maneuver_vars["timing"].get(),
                    "cost": 0, # Default
                    "range": 0, # Default
                    "description": maneuver_vars["description"].get("1.0", tk.END).strip()
                }
                try:
                    maneuver["cost"] = int(maneuver_vars["cost"].get())
                except ValueError:
                    print(f"Warning: Cost for maneuver '{maneuver['id']}' is not a valid number. Using 0.")
                try:
                    maneuver["range"] = int(maneuver_vars["range"].get())
                except ValueError:
                    print(f"Warning: Range for maneuver '{maneuver['id']}' is not a valid number. Using 0.")

                damage = {}
                if "damage_base_damage" in maneuver_vars:
                    base_damage = 0
                    try:
                        base_damage = int(maneuver_vars["damage_base_damage"].get())
                    except ValueError:
                        print(f"Warning: Base Damage for maneuver '{maneuver['id']}' is not a valid number. Using 0.")
                    damage["base_damage"] = base_damage
                
                if "damage_effect" in maneuver_vars:
                    damage["effect"] = maneuver_vars["damage_effect"].get()
                if "damage_formula" in maneuver_vars:
                    damage["formula"] = maneuver_vars["damage_formula"].get()
                if damage:
                    maneuver["damage"] = damage
                updated_maneuvers.append(maneuver)
            updated_data["maneuvers"] = updated_maneuvers

            # Collect flavor text
            flavor_text_content = self.editable_fields["flavor_text"].get("1.0", tk.END).strip()
            flavor_parts = flavor_text_content.split("\n\n") 
            
            description = ""
            tactics = ""
            roleplay = ""

            if len(flavor_parts) > 0 and flavor_parts[0].startswith("Description:\n"):
                description = flavor_parts[0].replace("Description:\n", "").strip()
            if len(flavor_parts) > 1 and flavor_parts[1].startswith("Tactics:\n"):
                tactics = flavor_parts[1].replace("Tactics:\n", "").strip()
            if len(flavor_parts) > 2 and flavor_parts[2].startswith("Roleplay:\n"):
                roleplay = flavor_parts[2].replace("Roleplay:\n", "").strip()

            updated_data["flavor"] = {
                "description": description,
                "tactics": tactics,
                "roleplay": roleplay
            }
            
            # Save to JSON file
            with open(ENEMY_DATA_FILE, 'w') as f:
                json.dump(updated_data, f, indent=4)
            print(f"Enemy data saved successfully to {ENEMY_DATA_FILE}")
            self.current_enemy_data = updated_data # Update current data in memory
            print("DEBUG: Save operation completed.")
            
        except KeyError as e:
            print(f"Error: Missing expected field when saving: {e}. Please ensure all fields are correctly initialized.")
        except Exception as e:
            print(f"An unexpected error occurred during save: {e}")


# MOCK_ZOMBIE_DATA definition removed from here, now in game_data.py

# Example of how to load and display the mock data (for testing purposes)
if __name__ == "__main__":
    # Import MOCK_ZOMBIE_DATA here for standalone testing
    from game_data import MOCK_ZOMBIE_DATA

    root = tk.Tk()
    root.title("Enemy Viewer Test")
    root.geometry("800x600")
    root.configure(bg="#2c2c2c")

    # Ensure the mock data file exists for testing
    if not os.path.exists(ENEMY_DATA_FILE):
        with open(ENEMY_DATA_FILE, 'w') as f:
            json.dump(MOCK_ZOMBIE_DATA, f, indent=4)
        print(f"Created initial {ENEMY_DATA_FILE} for testing.")
    else:
        # Load existing data if available
        try:
            with open(ENEMY_DATA_FILE, 'r') as f:
                MOCK_ZOMBIE_DATA = json.load(f)
            print(f"Loaded {ENEMY_DATA_FILE} for testing.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading {ENEMY_DATA_FILE}: {e}. Using default mock data.")


    # Dummy back_to_parent_callback for testing
    def dummy_back_callback():
        print("Back to parent menu (dummy callback)")
        root.destroy() # Close the test window

    viewer_frame = EnemyViewer(root, dummy_back_callback, MOCK_ZOMBIE_DATA)
    viewer_frame.pack(fill="both", expand=True)

    root.mainloop()
