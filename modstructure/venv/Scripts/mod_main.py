import sys
import tkinter
from tkinter import ttk
import mod_funcs
import mod_materials

# main/starter function of the program
# creates gui and initiates calculations, sketching, and plotting functions from mod_funcs.py

root = tkinter.Tk()
root.title("Depletion region demo")

mainframe = ttk.Frame(root, padding="100 100 100 100")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

name = tkinter.StringVar()
name_entry = ttk.Entry(mainframe, width=7, textvariable=name)
name_entry.grid(column=6, row=6)
button = ttk.Button(mainframe, text="Start", command=lambda: mod_funcs.init_funcs(name.get())).grid(column=6, row=7)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
#root.bind('<Return>', mod_funcs.init_funcs(name.get()))
root.mainloop()

