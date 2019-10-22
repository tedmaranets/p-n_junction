# model_structures

working project to visually model a pn junction under a varying reverse bias. Animations of junction behavior are based on empirical calculations and material data (Not hard-coded).

As of Version 1.2
- `mod_gui_class.py` contains object-oriented code that initializes different parts of the main gui window made in Tkinter.
- `mod_gui_funcs.py` contains the functions that add content/functionality to the left-panel of the gui. Executing this script starts the whole program.
- `mod_materials_12.py` contains the functions related to the material data.
- `calc_dep_widths.py` is a function that calculates depletion region behavior from empirical formulas, using material property data.
- `sktech.py` is a function that animates the calculated depletion region behavior in Pygame.
