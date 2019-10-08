import tkinter
from tkinter import ttk
from tkinter import messagebox
import pygame
import os
import sys
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import mod_funcs
import mod_materials

def create_window():
    master = tkinter.Tk()
    master.geometry("680x560")
    master.resizable(False,False)
    master.title("Depletion region demo")

    leftframe = tkinter.Frame(master)
    leftframe.grid(row=0, column=0)

    # developing left panel
    list_label = tkinter.Label(leftframe, text="Junction Material")
    list_label.grid(row=0, column=0, padx=10, pady=5)
    listbox = tkinter.Listbox(leftframe)
    listbox.grid(row=1, column=0, padx=10, pady=5)
    listbox.config(height=0, relief=tkinter.RIDGE, selectmode=tkinter.BROWSE)  # adjusts listbox height according to how many items are in the list

    mat_choices = mod_materials.get_choices()
    for item in mat_choices:
        listbox.insert(tkinter.END, item) # add all available material data to listbox

    # developing right panel
    # the tabs are basically frames located within the right panel (also a frame)
    tab_parent = ttk.Notebook(master, width=500, height=500)
    tab_parent.grid(row=0, column=1, rowspan=500, columnspan=500, padx=5, pady=10)
    # first tab is animation tab
    animation_tab = ttk.Frame(tab_parent)
    tab_parent.add(animation_tab, text='Animation')
    # statements that integrate pygame and tkinter, don't touch
    os.environ['SDL_WINDOWID'] = str(animation_tab.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    screen = pygame.display.set_mode((500, 500))
    # 2nd tab is graph tab
    graph_tab = ttk.Frame(tab_parent)
    tab_parent.add(graph_tab, text='Graph')


    def get_list(event): # triggered if list item is selected
        index = listbox.curselection()[0]
        seltext = listbox.get(index) # get string name of current selected item in listbox
        #print(seltext)
        master.title(seltext + " Depletion region demo") # adjust title
        [revbias, dep_widths] = mod_funcs.run_main(seltext) # run calculations and pygame animation
        # weird bug with the animation clearing after hovering mouse over it

        graphlist = graph_tab.winfo_children()
        for itm in graphlist:
            if itm.winfo_children():
                list.extend(itm.winfo_children())
        for itm in graphlist:
            itm.pack_forget() # removes previous graph/stuff in the graph tab for a new graph
                            # doing this because ax.clf() or ax.cla() wasn't working - Teddy 10/8/2019

        fig = Figure(figsize=(5, 4), dpi=100) # create graph figure to put into graph_tab
        ax = fig.add_subplot(111)
        ax.plot(revbias, dep_widths)

        canvas = FigureCanvasTkAgg(fig, master=graph_tab)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        title = seltext + " Depletion width vs. Reverse bias"
        ax.set_title(title, fontsize=15)
        ax.set_xlabel('Reverse bias (V)',fontsize=15)
        ax.set_ylabel('Depletion width (um)',fontsize=15)

    # bindings and exit protocol
    listbox.bind('<ButtonRelease-1>', get_list)
    listbox.bind('<Return>', get_list)
    def on_closing():
        master.destroy()
        sys.exit()
    master.protocol("WM_DELETE_WINDOW", on_closing)
    # if the window close (X) button is pressed, clear the tkinter GUI and exit the program

    pygame.init()
    pygame.display.flip()

    while True: # program runs till closed
        pygame.display.flip()
        master.mainloop()


create_window()