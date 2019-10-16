import tkinter
from tkinter import ttk
import pygame
import os
import sys
import mod_gui_funcs
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class GUIMaster(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)

        self.geometry("680x560")
        self.resizable(False, False)
        self.title("Depletion region demo")


class LeftPanel(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        mod_gui_funcs.GUIFunctions(self).make_left_panel()


class RightPanel(ttk.Notebook):

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.config(width=500, height=500)
        self.grid(row=0, column=1, rowspan=500, columnspan=500, padx=5, pady=10)

        # Right Panel
        animation_tab = ttk.Frame(self)
        self.add(animation_tab, text='Animation')
        os.environ['SDL_WINDOWID'] = str(animation_tab.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        screen = pygame.display.set_mode((500, 500))

class GraphTab(ttk.Frame):

    def __init__(self, notebook):
        ttk.Frame.__init__(self, notebook)
        notebook.add(self, text='Graph')

class MainFrame(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent


########## CREATE GUI ##########
master = GUIMaster()
mainframe = MainFrame(master)
mainframe.pack(side="top", fill="both", expand=True)
left_panel = LeftPanel(mainframe)
right_panel = RightPanel(mainframe)
graph_tab = GraphTab(right_panel)

def graph(name, rev_bias, dep_widths):
    graph_list = graph_tab.winfo_children()
    for itm in graph_list:
        if itm.winfo_children():
            list.extend(itm.winfo_children())
    for itm in graph_list:
        itm.pack_forget()  # removes previous graph/stuff in the graph tab for a new graph
        # doing this because ax.clf() or ax.cla() wasn't working - Teddy 10/8/2019

    fig = Figure(figsize=(5, 4), dpi=85)  # create graph figure to put into graph_tab
    ax = fig.add_subplot()
    ax.plot(rev_bias, dep_widths / 1000)

    canvas = FigureCanvasTkAgg(fig, master=graph_tab)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    title = name + "\nDepletion width vs. Reverse bias "
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('bias (V)', fontsize=12)
    ax.set_ylabel('width (um)', fontsize=12)

def on_closing():
    master.destroy()
    sys.exit()

master.protocol("WM_DELETE_WINDOW", on_closing)
master.mainloop()
################################
