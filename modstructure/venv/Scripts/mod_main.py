import sys
import tkinter
from tkinter import ttk
import mod_funcs
import mod_materials

# main/starter function of the program
# creates gui and initiates calculations, sketching, and plotting functions from mod_funcs.py

root = tkinter.Tk()
root.title("Depletion region demo")
root.geometry("250x200")
root.resizable(0,0)

name = tkinter.StringVar()
name_entry = ttk.Entry(root, width=7, textvariable=name)
name_entry.place(x=60, y=75)
button = ttk.Button(root, text="Start", command=lambda: mod_funcs.init_funcs(name.get())).place(x=60, y=100)
material = ttk.Label(root,text="material").place(x=110,y=75)

name_entry.focus()
root.mainloop()

