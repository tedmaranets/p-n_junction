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
    def __init__(self, prov):
        self.pnd = prov

    def calc_dep_widths(pnd):
        # initialize input
        revbias = list(numpy.arange(0, pnd.stop, 0.5))
        er = pnd.er
        ep = er * (8.854 * 10 ** (-14))  # permittivity (relative * permittivity of vacuum)
        q = 1.6029 * 10 ** (-19)  # electron charge in C

        # determine initial layers
        layer_array = mod_materials_12.make_layer_array(pnd)
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
        p_layer_per = []; p_layer_con = []; p_layer_depths = []; p_layer_transper = []; p_layer_transcon = []; p_layer_ni = []
        n_layer_per = []; n_layer_con = []; n_layer_depths = []; n_layer_transper = []; n_layer_transcon = []; n_layer_ni = []
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
        pthick = ast.literal_eval(p_layer_depths[kp]) * 1000 # convert to nm
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

        return revbias, layer_array, widths, first_n_index, first_p_index, n_indexes, p_indexes, nside, pside

    def skt_all(pnd, choice, value, start_val):
        # get calcs
        [revbias, layer_array, widths, first_n_index, first_p_index, n_indexes, p_indexes, nside, pside] = Functions.calc_dep_widths(pnd)
        # initialize
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        font = pygame.font.SysFont('arialms', 12)
        done = False
        clock = pygame.time.Clock()
        init_val = int(start_val)
        xn_start = 50
        yn_start = 150
        xn = 0
        xp = 0
        cxpos = xp
        junc_width = 400
        junc_height = 200
        numlayers = len(layer_array[1:, 0])
        actlayersum = 0
        i = 1
        while i != numlayers + 1:
            actlayersum += ast.literal_eval(layer_array[i, 4])  # in um
            i += 1
        i = 1
        props = []
        while i != numlayers + 1:
            props.append(ast.literal_eval(layer_array[i, 4]) / actlayersum)
            i += 1
        pix_deps = []
        for i in range(len(props)):
            pix_deps.append(props[i] * junc_width)

        pix_to_nm = (junc_width / actlayersum) / 1000  # 1 px for "pix_to_nm" nanometers

        n_high_color = (46, 151, 237)  # blue proportional to dopant concentration
        p_high_color = (21, 227, 150)  # green proportional to dopant concentration
        i = first_n_index
        maxconn = ast.literal_eval(layer_array[i, 3])
        i += 1
        while i != first_n_index - len(n_indexes):
            newcon = ast.literal_eval(layer_array[i, 3])
            if newcon > maxconn:
                maxconn = newcon
            i -= 1
        i = first_p_index
        maxconp = ast.literal_eval(layer_array[i, 3])
        while i != first_p_index + len(p_indexes):
            newcon = ast.literal_eval(layer_array[i, 3])
            if newcon > maxconp:
                maxconp = newcon
            i += 1
        j = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quitting the program
                    done = True

            ######## draw base rectangles to show all layers ########
            def draw_base_regions():
                # k = first_n_index
                k = 1
                i = 0
                xn = xn_start
                nplus = font.render("n+", True, (255, 255, 255))
                nminus = font.render("n-", True, (255, 255, 255))
                while k != first_n_index + 1:
                    currcon = ast.literal_eval(layer_array[k, 3])
                    n_color = n_high_color
                    if currcon != maxconn:
                        n_color = (46, 151, 237 - (1 / 200) * (maxconn / currcon))
                        screen.blit(nminus, (xn + pix_deps[i] / 2 - 5, yn_start - 20))
                    else:
                        screen.blit(nplus, (xn + pix_deps[i] / 2 - 5, yn_start - 20))
                    pygame.draw.rect(screen, n_color, pygame.Rect(xn, yn_start, pix_deps[i], junc_height))
                    xn += pix_deps[i] - 1
                    pygame.draw.line(screen, (255, 255, 255), (xn - 1, yn_start), (xn - 1, yn_start + junc_height - 1))
                    i += 1
                    k += 1
                mid = xn
                xp = xn
                pplus = font.render("p+", True, (255, 255, 255))
                pminus = font.render("p-", True, (255, 255, 255))
                while k != first_p_index + len(p_indexes):
                    currcon = ast.literal_eval(layer_array[k, 3])
                    p_color = p_high_color
                    if currcon != maxconp:
                        p_color = (21, 227 - (1 / 200) * (maxconn / currcon), 150)
                        screen.blit(pminus, (xp + pix_deps[i] / 2 - 5, yn_start - 20))
                    else:
                        screen.blit(pplus, (xp + pix_deps[i] / 2 - 5, yn_start - 20))
                    pygame.draw.rect(screen, p_color, pygame.Rect(xp + 1, yn_start, pix_deps[i], junc_height))
                    xp += pix_deps[i] - 1
                    if i != len(pix_deps) - 1:
                        pygame.draw.line(screen, (255, 255, 255), (xp, yn_start), (xp, yn_start + junc_height - 1))
                    i += 1
                    k += 1

                return mid

            if choice == "sweep":
                full_dep = widths[0:,2]
                if j != len(full_dep):
                    screen.fill((0, 0, 0))
                    nw_color = (237, 90, 69)
                    pw_color = (231, 149, 75)

                    info = "Full width: " + str(round(full_dep[j] / 1000, 2)) + " um | Reverse Bias -" + str(
                                                                                                revbias[j]) + " V"
                    info_text = font.render(info, True, (255, 255, 255))
                    screen.blit(info_text, (xp + 70, yn_start + junc_height + 20))
                    legend_red = font.render("red", True, nw_color)
                    legend_plus = font.render("=  +", True, (255, 255, 255))
                    screen.blit(legend_red, (xn + junc_width / 2 + 120, yn_start + junc_height + 20))
                    screen.blit(legend_plus, (xn + junc_width / 2 + 140, yn_start + junc_height + 20))
                    legend_blue = font.render("orange", True, pw_color)
                    legend_minus = font.render("=  -", True, (255, 255, 255))
                    screen.blit(legend_blue, (xn + junc_width / 2 + 120, yn_start + junc_height + 45))
                    screen.blit(legend_minus, (xn + junc_width / 2 + 160, yn_start + junc_height + 45))

                    mid = draw_base_regions()
                    nw_xpos = mid + (pix_to_nm) * nside[j]
                    pw_xpos = mid + (pix_to_nm) * pside[j]
                    pygame.draw.rect(screen, nw_color, pygame.Rect(nw_xpos, yn_start, mid - nw_xpos, junc_height))
                    pygame.draw.rect(screen, pw_color, pygame.Rect(mid, yn_start, pw_xpos - mid, junc_height))#

                    j += 1
                else:

                    done = True

            elif choice == "adjust":
                full_dep = widths[0:, 2]
                newbias = int(value)
                if newbias != init_val:
                    j = newbias
                    print(j)
                    print(full_dep[j])
                    init_val = newbias
                    test_gui_funcs.GUIFunctions.make_left_panel().adjust_bias(value, init_val)
            else:
                done = True

            pygame.display.flip()  # update
            clock.tick(60)  # refresh every 1/60 sec

        return 1











def run_main(name, choice, value, start_val):
    # start
    pnd = mod_materials_12.make_pnd(name)
    [rev_bias, layer_array, widths, first_n_index, first_p_index, n_indexes, p_indexes, nside, pside] = Functions.calc_dep_widths(pnd)
    Functions.skt_all(pnd, choice, value, start_val)

    return rev_bias, widths[0:,2]

