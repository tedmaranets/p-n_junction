import tkinter
from tkinter import ttk

root = tkinter.Tk()
root.title("test-gui")

mainframe = tkinter.Frame(root, height=200, width = 200)
mainframe.grid(column=0, row=0)
button = ttk.Button(root, text="test", command=lambda: print("test")).place(x=100,y=100)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
root.mainloop()