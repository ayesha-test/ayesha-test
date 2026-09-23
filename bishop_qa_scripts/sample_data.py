"""
Mock annotation data shaped like an Encord export.
Mix of correct segments and deliberately broken ones, so run_qa.py
proves each check actually catches its error.
"""

SEGMENTS = [
    {"start": 0.0, "end": 1.2, "label": "", "caption": "Picks up the mug with the right hand"},   # ok
    {"start": 1.2, "end": 1.35, "label": "", "caption": "Places the mug on the counter"},           # S3: too short (0.15s)
    {"start": 1.5, "end": 2.0, "label": "", "caption": "opens the fridge with the left hand"},      # S2: gap before (1.35 -> 1.5), C1: lowercase start
    {"start": 2.0, "end": 3.8, "label": "IDLE", "caption": ""},                                     # S4: IDLE but only 1.8s, actually fine (>=1.0)
    {"start": 3.8, "end": 4.1, "label": "idle", "caption": ""},                                     # C2: wrong case
    {"start": 4.1, "end": 4.4, "label": "IDLE", "caption": ""},                                     # S4: IDLE but 0.3s, below threshold
    {"start": 4.4, "end": 5.0, "label": "", "caption": "Wipes the counter with a cloth"},            # C10: banned word
    {"start": 5.0, "end": 5.6, "label": "", "caption": "Picks up the item from the shelf"},          # C12: vague noun
    {"start": 5.6, "end": 6.1, "label": "", "caption": "Places the bowl on the table."},             # C1: trailing period
]
