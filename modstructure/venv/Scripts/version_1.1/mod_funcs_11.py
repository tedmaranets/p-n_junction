import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import sys
import tkinter
from tkinter import ttk
import mod_materials_10

def calc_dep_widths(pnd):

    revbias = list(numpy.arange(0, pnd.stop, 0.5))
    er = pnd.er
    ep = er * (8.854 * 10 ** (-14))  # permittivity (relative * permittivity of vacuum)
    q = 1.6029 * 10 ** (-19)  # electron charge in C

    # determine initial layers
    layer_array = mod_materials_11.make_layer_array(pnd)
    #layers = layer_array[1:,0]
    first_n_index = 0
    first_p_index = 0
    p_after_n = False
    i = 0
    while not p_after_n:
        if layer_array[i,2] == 'N':
            first_n_index = i
        if layer_array[i,2] == 'P':
            first_p_index = i
            p_after_n = True
        i += 1
    # determine subsequent layers
    p_indexes = [] # indexes of the initial layer array
    n_indexes = []
    p_layer_Al = [] ; p_layer_con = [] ; p_layer_depths = [] ; p_layer_transAl = [] ; p_layer_transcon = [] ; p_layer_ni = []
    n_layer_Al = [] ; n_layer_con = [] ; n_layer_depths = [] ; n_layer_transAl = [] ; n_layer_transcon = [] ; n_layer_ni = []
    # i think this following part is a bit hard coded - Teddy 10/10/19
    # maybe doesn't matter if future material data is formatted the same
    i = first_n_index
    k = 1
    while layer_array[i,2] != 'U': # up the column (for n layers)
        n_indexes.append(k)
        n_layer_Al.append(layer_array[i,1])
        n_layer_con.append(layer_array[i,3])
        n_layer_depths.append(layer_array[i,4])
        n_layer_transAl.append(layer_array[i,5])
        n_layer_transcon.append(layer_array[i,6])
        n_layer_ni.append(layer_array[i,7])
        i -= 1
        k += 1
    i = first_p_index
    k = 1
    while i != len(layer_array[0:,2]): # down the column (for p layers)
        p_indexes.append(k)
        p_layer_Al.append(layer_array[i, 1])
        p_layer_con.append(layer_array[i, 3])
        p_layer_depths.append(layer_array[i, 4])
        p_layer_transAl.append(layer_array[i, 5])
        p_layer_transcon.append(layer_array[i, 6])
        p_layer_ni.append(layer_array[i, 7])
        i += 1
        k += 1

    # depletion calcs
    vbarrier = [] ; pside = [] ; nside = [] ; full_dep = []
    kp = 0 ; kn = 0
    pthick = ast.literal_eval(p_layer_depths[kp])*1000
    nthick = ast.literal_eval(n_layer_depths[kn])*1000
    Na = ast.literal_eval(p_layer_con[kp])
    Nd = ast.literal_eval(n_layer_con[kn])
    Ni = ast.literal_eval(p_layer_ni[kp])
    i = 0
    # kp < len(p_indexes)-1 or kn < len(n_indexes)-1
    while i != len(revbias):
        print(revbias[i])
        vbarrier.append(0.026 * numpy.log(Na * Nd / (Ni**2)) + numpy.abs(revbias[i]))
        pside.append(numpy.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) / (10 ** (-7)))  # in nm
        nside.append(-numpy.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) / (10 ** (-7)))
        full_dep.append(pside[i]-nside[i]) # in nm
        if pside[i] > pthick:
            kp += 1
            Na = ast.literal_eval(p_layer_con[kp])
            pthick += ast.literal_eval(p_layer_depths[kp])*1000
            Ni = ast.literal_eval(p_layer_ni[kp])
        if numpy.abs(nside[i]) > nthick:
            kn += 1
            Nd = ast.literal_eval(n_layer_con[kp])
            nthick += ast.literal_eval(p_layer_depths[kp])*1000
        vbarrier[i] = 0.026 * numpy.log(Na * Nd / (Ni**2)) + numpy.abs(revbias[i])
        pside[i] = numpy.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) / (10 ** (-7))
        nside[i] = -numpy.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) / (10 ** (-7))
        full_dep[i] = pside[i]-nside[i]
        i += 1

    #print(nside)
    #print(pside)
    #print(str(kp) + "  " + str(kn))
    #plt.plot(revbias,full_dep)
    #plt.show()
    return revbias, full_dep

def skt_2D_dep_widths(revbias, widths):
    # initialize
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    font = pygame.font.SysFont('arialms', 18)
    #print(pygame.font.get_fonts())
    done = False
    clock = pygame.time.Clock()
    # draw junction
    xp = 100
    yp = 150
    junc_width = 300
    junc_height = 200
    xn = xp + junc_width/2 - 1
    yn = yp
    p_color = (21, 227, 150) ; n_color = (46, 151, 237)
    pygame.draw.rect(screen, p_color, pygame.Rect(xp, yp, junc_width/2, junc_height)) # p-type region
    pygame.draw.rect(screen, n_color, pygame.Rect(xn, yn, junc_width/2, junc_height)) # n-type region
    ptext = font.render("p-type",True, (0,0,0))
    ntext = font.render("n-type", True, (0,0,0))
    screen.blit(ptext, (xp+20,yp))
    screen.blit(ntext, (xn+20,yn))
    # draw depletion region
    p_width = widths[0] ; n_width = widths[1] ; dep_width = widths[2]
    pw_color = (0,0,255) ; nw_color = (255,0,0)
    cxpos = xp + junc_width/2
    nm_topix_prop = 0.02
    pw_xpos = cxpos - nm_topix_prop * p_width[0]
    nw_xpos = cxpos - nm_topix_prop * n_width[0]
    #print(str(nm_topix_prop * p_width[0]))
    #print(str(pw_xpos))
    pygame.draw.rect(screen, pw_color, pygame.Rect(pw_xpos, yp, nm_topix_prop * p_width[0], junc_height))
    pygame.draw.rect(screen, nw_color, pygame.Rect(cxpos-1, yp, - nm_topix_prop * n_width[0], junc_height))

    info = str(round(dep_width[0]/1000,2)) + " um - " + str(revbias[0]) + " V"
    print(info + " p dep = " + str(round(p_width[0] / 1000, 2)) + " n dep = " + str(round(n_width[0] / 1000, 2)))
    info_text = font.render(info, True, (255,255,255))
    screen.blit(info_text, (xp + 70, yp + junc_height + 20))
    legend_red = font.render("red",True,(255,0,0))
    legend_plus = font.render("= +",True,(255,255,255))
    screen.blit(legend_red,(xn+junc_width/2-50,yn + junc_height + 20))
    screen.blit(legend_plus, (xn+junc_width/2- 20,yn + junc_height + 20))
    legend_blue = font.render("blue", True,(0, 0, 255))
    legend_minus = font.render("= -", True, (255, 255, 255))
    screen.blit(legend_blue, (xn + junc_width / 2 - 50, yn + junc_height + 45))
    screen.blit(legend_minus, (xn + junc_width / 2 - 10, yn + junc_height + 45))

    i = 1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quitting the program
                done = True

        if i != len(widths[2]):
            pw_xpos = cxpos - nm_topix_prop * p_width[i]
            nw_xpos = cxpos - nm_topix_prop * n_width[i]

            screen.fill((0,0,0))
            pygame.draw.rect(screen, p_color, pygame.Rect(xp, yp, junc_width / 2, junc_height))  # p-type region
            pygame.draw.rect(screen, n_color, pygame.Rect(xn, yn, junc_width / 2, junc_height))  # n-type region
            pygame.draw.rect(screen, pw_color, pygame.Rect(pw_xpos,yp, nm_topix_prop * p_width[i], junc_height))
            pygame.draw.rect(screen, nw_color, pygame.Rect(cxpos-1, yn, - nm_topix_prop * n_width[i], junc_height))
            ptext = font.render("p-type", True, (255, 255, 255))
            ntext = font.render("n-type", True, (255, 255, 255))
            screen.blit(ptext, (xp + 20, yp-30))
            screen.blit(ntext, (xn + 20, yn-30))

            info = str(round(dep_width[i]/1000,2)) + " um - " + str(revbias[i]) + " V"
            print(info + " p dep = " + str(round(p_width[i]/1000,2)) + " n dep = " + str(round(n_width[i]/1000,2)))
            info_text = font.render(info, True, (255, 255, 255))
            screen.blit(info_text, (xp + 70, yp + junc_height + 20))
            legend_red = font.render("red", True,(255, 0, 0))
            legend_plus = font.render("= +",True, (255, 255, 255))
            screen.blit(legend_red, (xn + junc_width / 2 - 50, yn + junc_height + 20))
            screen.blit(legend_plus, (xn + junc_width / 2 - 20, yn + junc_height + 20))
            legend_blue = font.render("blue",True, (0, 0, 255))
            legend_minus = font.render("= -", True, (255, 255, 255))
            screen.blit(legend_blue, (xn + junc_width / 2 - 50, yn + junc_height + 45))
            screen.blit(legend_minus, (xn + junc_width / 2 - 10, yn + junc_height + 45))

            i += 1
        else:
            done = True

        pygame.display.update() # update
        clock.tick(60) # refresh every 1/60 sec

def run_main(name):
    # start
    pnd = mod_materials_10.make_pnd(name)
    revbias = list(np.arange(0, pnd.stop, 0.5))
    [revbias, widths] = calc_dep_widths(pnd)

    #print(widths[0])
    #print(widths[1])
    #print(widths[2])
    skt_2D_dep_widths(revbias, widths)

    return revbias, widths[2]

