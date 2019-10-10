import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import sys
import tkinter
from tkinter import ttk
import mod_materials_10

def calc_dep_widths(rev_bias, pnd):
    # calculates the depletion region widths for each reverse bias
    # specific to wafer properties: Na = acceptor/hole concentration,
    # Nd = donor/electron concentration, Ni = intrinsic carrier concentration, er = relative permittivity
    vbarrier = []
    pside = []
    nside = []
    dep_width = []
    Na = pnd.Na
    Nd = pnd.Nd
    Ni = pnd.Ni
    er = pnd.er
    ep = er*(8.854*10**(-14)) # permittivity (relative * permittivity of vacuum)
    q = 1.6029*10**(-19) # electron charge in C

    # calculations loop
    for i in range(len(rev_bias)):
        vbarrier.append(0.026 * np.log(Na * Nd / (Ni**2)) + np.abs(rev_bias[i])) # in V
        pside.append(np.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) / (10**(-7))) # in nm
        nside.append(-np.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) / (10**(-7)))
        dep_width.append(pside[i]-nside[i]) # in nm

    widths_arrays = np.stack((pside,nside,dep_width), axis=0)
    return widths_arrays

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
    widths = calc_dep_widths(revbias, pnd)
    #print(widths[0])
    #print(widths[1])
    #print(widths[2])
    skt_2D_dep_widths(revbias, widths)

    return revbias, widths[2]

