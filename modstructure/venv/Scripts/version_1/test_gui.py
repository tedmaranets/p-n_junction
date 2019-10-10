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
    #master.columnconfigure(0, weight=1)  # these two lines just resize the frame if the main window is resized
    #master.rowconfigure(0, weight=1)

    leftframe = tkinter.Frame(master)
    leftframe.grid(row=0, column=0)

    list_label = tkinter.Label(leftframe, text="Junction Material")
    list_label.grid(row=0, column=0, padx=10, pady=5)
    listbox = tkinter.Listbox(leftframe)
    listbox.grid(row=1, column=0, padx=10, pady=5)
    listbox.config(height=0, relief=tkinter.RIDGE, selectmode=tkinter.BROWSE)  # adjusts listbox height according to how many items are in the list

    mat_choices = mod_materials.get_choices()
    for item in mat_choices:
        listbox.insert(tkinter.END, item)


    tab_parent = ttk.Notebook(master, width=500, height=500)
    tab_parent.grid(row=0, column=1, rowspan=500, columnspan=500, padx=5, pady=10)
    # developing the animation tab
    animation_tab = ttk.Frame(tab_parent)
    tab_parent.add(animation_tab, text='Animation')
    os.environ['SDL_WINDOWID'] = str(animation_tab.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    screen = pygame.display.set_mode((500, 500))
    # create the graph tab
    graph_tab = ttk.Frame(tab_parent)
    tab_parent.add(graph_tab, text='Graph')


    def get_list(event):
        index = listbox.curselection()[0]
        seltext = listbox.get(index)
        #print(seltext)
        master.title(seltext + " Depletion region demo")
        [revbias, dep_widths] = mod_funcs.run_main(seltext)

        def all_children(window):
            _list = window.winfo_children()

            for itm in _list:
                if itm.winfo_children():
                    _list.extend(itm.winfo_children())

            return _list

        graph_con = all_children(graph_tab)
        for obj in graph_con:
            obj.pack_forget() # removes previous graph/stuff in the graph tab for a new graph
                            # doing this because ax.clf() or ax.cla() wasn't working - TM 10/8/2019

        fig = Figure(figsize=(5, 4), dpi=100)
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

    while True:
        pygame.display.flip()
        master.mainloop()


create_window()