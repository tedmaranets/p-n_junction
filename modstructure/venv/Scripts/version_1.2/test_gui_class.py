import tkinter
from tkinter import ttk
from tkinter import messagebox
import pygame
import os
import sys
import mod_materials_12
import test_gui_funcs


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
        test_gui_funcs.GUIFunctions(self).make_left_panel()


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
        # 2nd tab is graph tab
        graph_tab = ttk.Frame(self)
        self.add(graph_tab, text='Graph')


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

def on_closing():
    master.destroy()
    sys.exit()

master.protocol("WM_DELETE_WINDOW", on_closing)
master.mainloop()
################################