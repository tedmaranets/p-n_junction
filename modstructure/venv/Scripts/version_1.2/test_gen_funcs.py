import numpy
import matplotlib.pyplot as plt
import pygame
import time
import sys
import tkinter
from tkinter import ttk
import mod_materials_12
import test_gui_funcs
import ast

class Functions:

    def __init__(self, pnj):
        self.pnj = pnj

    def calc_dep_widths(self):
        pnj = self.pnj
        # initialize input
        revbias = list(numpy.arange(0, pnj.stop, 0.5))
        er = pnj.er
        ep = er * (8.854 * 10 ** (-14))  # permittivity (relative * permittivity of vacuum)
        q = 1.6029 * 10 ** (-19)  # electron charge in C

        # determine initial layers
        layer_array = mod_materials_12.make_layer_array(pnj)
        # layers = layer_array[1:,0]
        first_n_index = 0
        first_p_index = 0
        p_after_n = False
        i = 1
        while not p_after_n:
            if layer_array[i, 2] == 'N':
                first_n_index = i
            if layer_array[i, 2] == 'P':
                first_p_index = i
                p_after_n = True
            i += 1
        # determine subsequent layers
        p_indexes = []  # indexes of the initial layer array
        n_indexes = []
        p_layer_per = [];
        p_layer_con = [];
        p_layer_depths = [];
        p_layer_transper = [];
        p_layer_transcon = [];
        p_layer_ni = []
        n_layer_per = [];
        n_layer_con = [];
        n_layer_depths = [];
        n_layer_transper = [];
        n_layer_transcon = [];
        n_layer_ni = []
        i = first_n_index
        k = 1
        while i != 0:  # up the column (for n layers)
            n_indexes.append(k)
            n_layer_per.append(layer_array[i, 1])
            n_layer_con.append(layer_array[i, 3])
            n_layer_depths.append(layer_array[i, 4])
            n_layer_transper.append(layer_array[i, 5])
            n_layer_transcon.append(layer_array[i, 6])
            n_layer_ni.append(layer_array[i, 7])
            i -= 1
            k += 1
        i = first_p_index
        k = 1
        while i != len(layer_array[0:, 2]):  # down the column (for p layers)
            p_indexes.append(k)
            p_layer_per.append(layer_array[i, 1])
            p_layer_con.append(layer_array[i, 3])
            p_layer_depths.append(layer_array[i, 4])
            p_layer_transper.append(layer_array[i, 5])
            p_layer_transcon.append(layer_array[i, 6])
            p_layer_ni.append(layer_array[i, 7])
            i += 1
            k += 1

        # depletion calcs
        vbarrier = []
        pside = []
        nside = []
        full_dep = []
        kp = 0
        kn = 0
        pthick = ast.literal_eval(p_layer_depths[kp]) * 1000  # convert to nm
        nthick = ast.literal_eval(n_layer_depths[kn]) * 1000
        Na = ast.literal_eval(p_layer_con[kp])
        Nd = ast.literal_eval(n_layer_con[kn])
        Ni = ast.literal_eval(p_layer_ni[kp])
        i = 0
        # kp < len(p_indexes)-1 or kn < len(n_indexes)-1
        while i != len(revbias):
            # print(revbias[i])
            vbarrier.append(0.026 * numpy.log(Na * Nd / (Ni ** 2)) + numpy.abs(revbias[i]))
            pside.append(numpy.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) / (10 ** (-7)))  # in nm
            nside.append(-numpy.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) / (10 ** (-7)))
            full_dep.append(pside[i] - nside[i])  # in nm
            if pside[i] > pthick:
                kp += 1
                Na = ast.literal_eval(p_layer_con[kp])
                pthick += ast.literal_eval(p_layer_depths[kp]) * 1000
                Ni = ast.literal_eval(p_layer_ni[kp])
            if numpy.abs(nside[i]) > nthick:
                kn += 1
                Nd = ast.literal_eval(n_layer_con[kp])
                nthick += ast.literal_eval(p_layer_depths[kp]) * 1000
            vbarrier[i] = 0.026 * numpy.log(Na * Nd / (Ni ** 2)) + numpy.abs(revbias[i])
            pside[i] = numpy.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) / (10 ** (-7))
            nside[i] = -numpy.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) / (10 ** (-7))
            full_dep[i] = pside[i] - nside[i]
            i += 1

        widths = numpy.column_stack((nside, pside, full_dep))
        first_indexes = numpy.stack((first_n_index,first_p_index))
        sides = numpy.column_stack((nside,pside))

        return revbias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides