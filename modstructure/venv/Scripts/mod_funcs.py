import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import sys
import tkinter
from tkinter import ttk
import mod_materials

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
        vbarrier.append(0.26 * np.log(Na * Nd / (Ni**2)) + np.abs(rev_bias[i])) # in V
        pside.append(np.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) * 10 ** 4) # in um
        nside.append(-np.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) * 10 ** 4)
        dep_width.append(pside[i]-nside[i]) # in um

    widths_arrays = np.stack((pside,nside,dep_width), axis=0)
    return widths_arrays

def skt_2D_dep_widths(revbias, widths):

    # draws and animates depletion region as reverse bias increases
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('depletion region visual')
    done = False
    clock = pygame.time.Clock()
    x = 100
    y = 200
    pside = widths[0] * 10 ; nside = widths[1] * 10 ; dep_width = widths[2] * 10;
    i = 0
    pygame.draw.rect(screen, (255, 125, 45), pygame.Rect(x, y, dep_width[i], 100))
    cxpos = x + dep_width[i] + 10*nside[i] # delineates p-doped and n-doped regions (p on left, n on right)
    pygame.draw.line(screen, (255,0,0), (cxpos, 200), (cxpos, 300), 2) # 2 px thick line through middle of depletion region

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(round(dep_width[i] / 10, 4)) + " um - " + str(revbias[i]) + " V", True, (255, 255, 255), (0, 0, 0)) # white text on black background

    i = 1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quitting the program
                done = True
        if i != len(dep_width):
            #sub = dep_width[i]/2
            #x = 200 - sub
            #add = (dep_width[i]-dep_width[i-1])/2
            screen.fill((0,0,0)) # refill screen to black
            pygame.draw.rect(screen, (255,125,45), pygame.Rect(x,y, dep_width[i], 100))

            #cxpos = x + 10*pside[i]

            #print(str(cxpos) + "   " + str(x + dep_width[i]) + "\n")
            cxpos = x + dep_width[i] + 10 * nside[i]
            pygame.draw.line(screen, (255,0,0), (cxpos, 200), (cxpos, 300), 2)
            text = font.render(str(round(dep_width[i] / 10, 4)) + " um - " + str(revbias[i]) + " V", True, (255, 255, 255), (0, 0, 0))
            textRect = text.get_rect()
            screen.blit(text, textRect)
            i += 1
        else:
            done = True # quit

        pygame.display.flip() # update
        clock.tick(60) # refresh every 1/60 sec

def run_main(name):
    # start
    pnd = mod_materials.make_pnd(name)
    revbias = list(np.arange(0, pnd.stop, 0.5))
    widths = calc_dep_widths(revbias, pnd)
    skt_2D_dep_widths(revbias, widths)

    return revbias, widths[2]

