import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import mod_materials_12
import calc_dep_widths
import sketch
import mod_gui_class

class GUIFunctions:

    def __init__(self, comp):
        self.comp = comp

    def make_left_panel(self):

        # Left Panel
        list_label = tkinter.Label(self.comp, text="Junction Material")
        list_label.grid(row=0, column=0, padx=10, pady=5)
        list_box = tkinter.Listbox(self.comp)
        list_box.grid(row=1, column=0, padx=10, pady=5)
        list_box.config(width=0, height=0, relief=tkinter.RIDGE, selectmode=tkinter.BROWSE)

        # material names and respective designs
        mat_choices = mod_materials_12.get_choices()
        designs = []
        for item in mat_choices[0]:
            list_box.insert(tkinter.END, item)  # add all available material name data to listbox
        for item in mat_choices[1]:
            designs.append(item)

        source_label = tkinter.Label(self.comp, text="Source")
        source_label.grid(row=2, column=0, padx=10, pady=5)
        source_label_text = tkinter.StringVar()
        source_item_label = tkinter.Label(self.comp, textvariable=source_label_text)
        source_item_label.grid(row=3, column=0, padx=10, pady=2)

        #value = 0
        #adj_before = False
        def make_selection(event):
            index = list_box.curselection()[0]
            selected_text = list_box.get(index)  # get string name of current selected item in listbox
            source_label_text.set(designs[index])
            pnj = mod_materials_12.make_pnd(selected_text)
            # make widgets (sweep button and adjustment scale)
            sweep_button = tkinter.Button(self.comp, text="Sweep")
            sweep_button.grid(row=4, column=0, padx=10, pady=5)
            sweep_button.config(width=10, height=0)
            end = pnj.stop - 0.5
            adjust_bias_scale = tkinter.Scale(self.comp, from_=0, to=end, orient=tkinter.VERTICAL,
                                              tickinterval=2, length=200,
                                             command=adjust_bias)
            adjust_bias_scale.grid(row=5, column=0, padx=7, pady=5)
            # make binds
            sweep_button.bind('<ButtonRelease-1>', sweep_bias)

        def sweep_bias(event):
            index = list_box.curselection()[0]
            selected_text = list_box.get(index)
            pnd = mod_materials_12.make_pnd(selected_text)
            [rev_bias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides] = calc_dep_widths.run(pnd)
            sketch.run(rev_bias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides, False, 0)
            mod_gui_class.graph(selected_text,rev_bias, widths[0:,2])

        def adjust_bias(value):
            index = list_box.curselection()[0]
            selected_text = list_box.get(index)
            pnd = mod_materials_12.make_pnd(selected_text)
            [rev_bias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides] = calc_dep_widths.run(pnd)
            sketch.run(rev_bias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides, True, value)
            mod_gui_class.graph(selected_text, rev_bias, widths[0:, 2])

        list_box.bind('<ButtonRelease-1>', make_selection)


