# game_data.py

# This file holds mock data and can be expanded for other game data.

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
