# enemy_viewer.py

import tkinter as tk
from tkinter import scrolledtext # For multi-line text with scrollbars
import json # To load the mock enemy data

class EnemyViewer(tk.Frame):
    """
    A frame representing the detailed viewer for a single enemy statblock.
    """
    def __init__(self, master, switch_frame_callback, enemy_data=None):
        """
        Initializes the EnemyViewer frame.

        Args:
            master: The parent widget (the main application window or content frame).
            switch_frame_callback: A function to call to switch to another frame.
            enemy_data (dict, optional): The dictionary containing the enemy's statblock data.
                                         Defaults to None, in which case a placeholder is shown.
        """
        super().__init__(master)
        self.master = master
        self.switch_frame_callback = switch_frame_callback
        self.configure(bg="#2c2c2c")

        # Configure the grid to be responsive
        self.grid_rowconfigure(0, weight=0) # For the back button/title
        self.grid_rowconfigure(1, weight=1) # For the main content area
        self.grid_columnconfigure(0, weight=1)

        # --- Back button ---
        back_button = tk.Label(self, text="❮ Back to Enemy Data", font=("Helvetica", 12, "underline"),
                               fg="#f0f0f0", bg="#2c2c2c", cursor="hand2")
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        back_button.bind("<Button-1>", lambda e: self.switch_frame_callback("DatabaseMenu")) # Go back to DatabaseMenu

        # --- Main content frame for enemy details ---
        self.detail_frame = tk.Frame(self, bg="#3c3c3c", padx=20, pady=20)
        self.detail_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.detail_frame.grid_columnconfigure(0, weight=1) # Allow content to expand

        self.display_enemy_data(enemy_data)

    def display_enemy_data(self, enemy_data):
        """
        Populates the viewer with the provided enemy data.
        Clears previous data if any.
        """
        # Clear existing widgets in the detail_frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        if not enemy_data:
            tk.Label(self.detail_frame, text="No enemy data to display.", font=("Helvetica", 16),
                     fg="#f0f0f0", bg="#3c3c3c").pack(pady=50)
            return

        # --- Enemy Name ---
        name_label = tk.Label(self.detail_frame, text=enemy_data.get("name", "Unknown Enemy"),
                              font=("Helvetica", 22, "bold"), fg="#f0f0f0", bg="#3c3c3c")
        name_label.pack(pady=(0, 15))

        # --- Basic Info Frame ---
        basic_info_frame = tk.Frame(self.detail_frame, bg="#4a4a4a", padx=10, pady=10)
        basic_info_frame.pack(fill="x", pady=5)

        tk.Label(basic_info_frame, text=f"ID: {enemy_data.get('id', 'N/A')}",
                 font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
        
        threat_level = enemy_data.get("threatLevel", {})
        tk.Label(basic_info_frame, text=f"Threat Level (Base): {threat_level.get('base', 'N/A')}",
                 font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
        tk.Label(basic_info_frame, text=f"Threat Level (Per Spawn Group): {threat_level.get('per_spawn_group', 'N/A')}",
                 font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
        
        tk.Label(basic_info_frame, text=f"Max Action Points: {enemy_data.get('maximumActionPoints', 'N/A')}",
                 font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")

        # --- Maneuvers Section ---
        tk.Label(self.detail_frame, text="Maneuvers", font=("Helvetica", 16, "bold"),
                 fg="#f0f0f0", bg="#3c3c3c").pack(pady=(15, 5), anchor="w")
        
        maneuvers_frame = tk.Frame(self.detail_frame, bg="#4a4a4a", padx=10, pady=10)
        maneuvers_frame.pack(fill="x", pady=5)

        maneuvers = enemy_data.get("maneuvers", [])
        if maneuvers:
            for i, maneuver in enumerate(maneuvers):
                tk.Label(maneuvers_frame, text=f"{i+1}. {maneuver.get('id', 'N/A')}",
                         font=("Helvetica", 12, "underline"), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                tk.Label(maneuvers_frame, text=f"   Timing: {maneuver.get('timing', 'N/A')}",
                         font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                tk.Label(maneuvers_frame, text=f"   Cost: {maneuver.get('cost', 'N/A')}",
                         font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                tk.Label(maneuvers_frame, text=f"   Range: {maneuver.get('range', 'N/A')}",
                         font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                
                description = maneuver.get('description', 'No description.')
                tk.Label(maneuvers_frame, text=f"   Description: {description}",
                         font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a", wraplength=500, justify="left").pack(anchor="w")
                
                damage = maneuver.get('damage', {})
                if damage:
                    tk.Label(maneuvers_frame, text=f"   Damage: Base {damage.get('base_damage', 'N/A')} ({damage.get('effect', 'N/A')})",
                             font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                    if damage.get('formula'):
                        tk.Label(maneuvers_frame, text=f"   Formula: {damage.get('formula', 'N/A')}",
                                 font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")
                tk.Frame(maneuvers_frame, height=1, bg="#555555").pack(fill="x", pady=5) # Separator
        else:
            tk.Label(maneuvers_frame, text="No maneuvers listed.", font=("Helvetica", 10),
                     fg="#f0f0f0", bg="#4a4a4a").pack(anchor="w")

        # --- Flavor Text Section ---
        tk.Label(self.detail_frame, text="Flavor Text", font=("Helvetica", 16, "bold"),
                 fg="#f0f0f0", bg="#3c3c3c").pack(pady=(15, 5), anchor="w")
        
        flavor = enemy_data.get("flavor", {})
        
        # Using ScrolledText for potentially long flavor descriptions
        description_text = scrolledtext.ScrolledText(self.detail_frame, wrap=tk.WORD, height=5,
                                                     font=("Helvetica", 10), fg="#f0f0f0", bg="#4a4a4a",
                                                     insertbackground="#f0f0f0", relief="flat", bd=0)
        description_text.pack(fill="x", pady=5)
        description_text.insert(tk.END, f"Description:\n{flavor.get('description', 'N/A')}\n\n")
        description_text.insert(tk.END, f"Tactics:\n{flavor.get('tactics', 'N/A')}\n\n")
        description_text.insert(tk.END, f"Roleplay:\n{flavor.get('roleplay', 'N/A')}")
        description_text.config(state=tk.DISABLED) # Make it read-only


# Mock data for a Zombie, based on bestiary_schema.json
MOCK_ZOMBIE_DATA = {
    "id": "mon_zombie_basic",
    "name": "Zombie",
    "portrait": "monsters/zombie_basic.png",
    "threatLevel": {
        "base": 1,
        "per_spawn_group": 5
    },
    "maximumActionPoints": 8,
    "maneuvers": [
        {
            "id": "unarmed_attack",
            "timing": "Action",
            "cost": 2,
            "range": 0,
            "description": "Unarmed Attack 1 + Chain Attack (Number of Zombies in the same Area divided by 10) (Round down)",
            "damage": {
                "base_damage": 1,
                "effect": "bash",
                "formula": "chain_attack"
            }
        },
        {
            "id": "grapple",
            "timing": "Action",
            "cost": 3,
            "range": 0,
            "description": "Attempt to grapple a target. If successful, target is immobilized.",
            "damage": {
                "base_damage": 0,
                "effect": "grapple"
            }
        }
    ],
    "flavor": {
        "description": "Possessing no Reinforcements at all, these are the most basic of the Undead. They are slow, shambling corpses, driven only by an insatiable hunger.",
        "tactics": "The advantage of using zombies is their low cost and ability to overwhelm enemies through sheer numbers. They are best used in large groups to tie down more powerful foes.",
        "roleplay": "Zombies that appear as a group lack individual personality, acting as a single, mindless horde. Their moans and groans are the only sounds they make, a constant reminder of their decaying state."
    }
}

# Example of how to load and display the mock data (for testing purposes)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enemy Viewer Test")
    root.geometry("800x600")
    root.configure(bg="#2c2c2c")

    # Dummy switch_frame_callback for testing
    def dummy_switch_frame(frame_name, enemy_data=None):
        print(f"Switching to {frame_name} (dummy callback)")
        # In a real app, you'd hide this frame and show another
        if frame_name == "DatabaseMenu":
            viewer_frame.pack_forget()
            tk.Label(root, text="Back to Database Menu (Placeholder)", font=("Helvetica", 20), fg="white", bg="blue").pack(expand=True)
        
    viewer_frame = EnemyViewer(root, dummy_switch_frame, MOCK_ZOMBIE_DATA)
    viewer_frame.pack(fill="both", expand=True)

    root.mainloop()
