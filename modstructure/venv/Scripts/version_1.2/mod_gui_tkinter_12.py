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
import mod_funcs_12
import mod_materials_12

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
    listbox.config(width = 0, height=0, relief=tkinter.RIDGE, selectmode=tkinter.BROWSE)



    mat_choices = mod_materials_12.get_choices()
    designs = []
    for item in mat_choices[0]:
        listbox.insert(tkinter.END, item) # add all available material name data to listbox
    for item in mat_choices[1]:
        designs.append(item)


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
    pygame.display.init()
    screen = pygame.display.set_mode((500, 500))
    # 2nd tab is graph tab
    graph_tab = ttk.Frame(tab_parent)
    tab_parent.add(graph_tab, text='Graph')
    initial_val = 0

    def get_list_sweep(event): # triggered if list item is selected
        index = listbox.curselection()[0]
        seltext = listbox.get(index)
        [revbias, dep_widths, newinit_val] = mod_funcs_12.run_main(seltext, "sweep", 0, 0)
        graph_data(seltext, revbias, dep_widths)


    def bias_change(value, start_val):
        index = listbox.curselection()[0]
        seltext = listbox.get(index)
        #print(value)
        [revbias, dep_widths, newinit_val] = mod_funcs_12.run_main(seltext, "adjust", value, start_val)
        initial_val = newinit_val
        graph_data(seltext, revbias, dep_widths)



    def graph_data(name, revbias, dep_widths):
        graphlist = graph_tab.winfo_children()
        for itm in graphlist:
            if itm.winfo_children():
                list.extend(itm.winfo_children())
        for itm in graphlist:
            itm.pack_forget()  # removes previous graph/stuff in the graph tab for a new graph
            # doing this because ax.clf() or ax.cla() wasn't working - Teddy 10/8/2019

        fig = Figure(figsize=(5, 4), dpi=85)  # create graph figure to put into graph_tab
        ax = fig.add_subplot()
        ax.plot(revbias, dep_widths / 1000)

        canvas = FigureCanvasTkAgg(fig, master=graph_tab)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        title = name + "\nDepletion width vs. Reverse bias "
        ax.set_title(title, fontsize=12)
        ax.set_xlabel('bias (V)', fontsize=12)
        ax.set_ylabel('width (um)', fontsize=12)

    def make_selections(event):
        source_label = tkinter.Label(leftframe, text="Source")
        source_label.grid(row=2, column=0, padx=10, pady=5)
        source_label_text = tkinter.StringVar()
        source_item_label = tkinter.Label(leftframe, textvariable=source_label_text)
        source_item_label.grid(row=3, column=0, padx=10, pady=2)
        # get selection
        index = listbox.curselection()[0]
        seltext = listbox.get(index)  # get string name of current selected item in listbox
        master.title(seltext + " Depletion region demo")  # adjust title
        source_label_text.set(designs[index])
        # make pnd
        pnd = mod_materials_12.make_pnd(seltext)
        # make widgets (sweep button and adjustment scale)
        sweep_button = tkinter.Button(leftframe, text="Sweep")
        sweep_button.grid(row=4, column=0, padx=10, pady=5)
        sweep_button.config(width=10, height=0)
        end = pnd.stop - 0.5
        adjust_bias_scale = tkinter.Scale(leftframe, from_=0, to=end, orient=tkinter.VERTICAL,
                                          tickinterval=2, length = 200,
                                          command=lambda value, start_val : bias_change(value, 0))
        adjust_bias_scale.grid(row=5,column=0,padx=7,pady=5)
        # make binds
        sweep_button.bind('<ButtonRelease-1>', get_list_sweep)


        return 1


    listbox.bind('<ButtonRelease-1>', make_selections)
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