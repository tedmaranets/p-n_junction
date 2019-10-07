import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import sys
import tkinter
from tkinter import ttk
import mod_materials

def calc_dep_widths(revbias, pnd):
    # calculates the depletion region widths for each reverse bias
    # specific to wafer properties: Na = acceptor/hole concentration,
    # Nd = donor/electron concentration, Ni = intrinsic carrier concentration, er = relative permittivity

    vbarrier = []
    pside = []
    nside = []
    depwidth = []
    Na = pnd.Na
    Nd = pnd.Nd
    Ni = pnd.Ni
    er = pnd.er
    ep = er*(8.854*10**(-14)) # permittivity (relative * permittivity of vacuum)
    q = 1.6029*10**(-19) # electron charge in C

    # calculations loop
    for i in range(len(revbias)):
        vbarrier.append(0.26 * np.log(Na * Nd / (Ni**2)) + np.abs(revbias[i])) # in V
        pside.append(np.sqrt(2 * ep / q * Nd / Na * vbarrier[i] / (Na + Nd)) * 10 ** 4) # in um
        nside.append(-np.sqrt(2 * ep / q * Na / Nd * vbarrier[i] / (Na + Nd)) * 10 ** 4)
        depwidth.append(pside[i]-nside[i]) # in um

    outstack = np.stack((pside,nside,depwidth), axis=0)
    return outstack

def skt_2D_dep_widths(revbias, widths):
    # draws and animates depletion region as reverse bias increases
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption('depletion region visual')
    done = False
    clock = pygame.time.Clock()
    x = 300
    y = 200
    dispwidth = []
    pside = widths[0] ; nside = widths[1] ; depwidth = widths[2] ;
    for k in range(len(depwidth)):
        dispwidth.append(depwidth[k] * 10) # arbitrary setting of a proportion of the actual depletion width to pixels

    i = 0
    pygame.draw.rect(screen, (255, 125, 45), pygame.Rect(x, y, dispwidth[i], 100))
    cxpos = x + dispwidth[i]/2 + pside[i]*10 # delineates p-doped and n-doped regions (p on left, n on right)
    pygame.draw.line(screen, (255,0,0), (cxpos, 200), (cxpos, 300), 2) # 2 px thick line through middle of depletion region

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(round(depwidth[i], 4)) + " um - " + str(revbias[i]) + " V", True, (255, 255, 255), (0, 0, 0)) # white text on black background
    textRect = text.get_rect()

    i = 1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quitting the program
                done = True
        if i != len(dispwidth):
            sub = dispwidth[i]/2
            x = 200 - sub
            add = (dispwidth[i]-dispwidth[i-1])/2
            screen.fill((0,0,0)) # refill screen to black
            pygame.draw.rect(screen, (255,125,45), pygame.Rect(x,y, dispwidth[i-1] + add, 100))
            cxpos = x + (dispwidth[i-1] + add)/2 + pside[i]*10
            print(str(cxpos) + "   " + str(x) + "\n")
            pygame.draw.line(screen, (255,0,0), (cxpos, 200), (cxpos, 300), 2)
            text = font.render(str(round(depwidth[i], 4)) + " um - " + str(revbias[i]) + " V", True, (255, 255, 255), (0, 0, 0))
            textRect = text.get_rect()
            screen.blit(text, textRect)
            i += 1
        else:
            done = True # quit

        pygame.display.flip() # update
        clock.tick(60) # refresh every 1/60 sec

def init_funcs(name):
    # start
    pnd = mod_materials.make_pnd(name)
    if pnd.name is "null":
        print("\n invalid pnd name")
        sys.exit()
    else:
        revbias = list(np.arange(0, pnd.stop, 0.5))
        print(revbias)
        widths = calc_dep_widths(revbias, pnd)  # wafer properties of APD
        print(widths[2])

    # drawings and plots
    skt_2D_dep_widths(revbias, widths)

    plt.clf()
    fig = plt.plot(revbias, widths[2])
    title = name + " depletion width vs. reverse bias"
    plt.title(title, fontsize=18)
    plt.xlabel("reverse bias (V)", fontsize=15)
    plt.ylabel("depletion width (um)", fontsize=15)
    plt.show()
