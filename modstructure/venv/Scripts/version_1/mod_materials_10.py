import numpy

class Material(object):

    def __init__(self, name, Na, Nd, Ni, er, stop, design):
        self.name = name
        self.Na = Na
        self.Nd = Nd
        self.Ni = Ni
        self.er = er
        self.stop = stop
        self.design = design

# data list array
materials = [["AlGaAs (30%Al 70%Ga)",5 * 10 ** 16, 1 * 10 ** 17, 2100, 12.048, 38.5, "D19.1 Wafer"]
             ]

def make_pnd(name): # creates an object with necessary properties for calculations
    for i in range(len(materials)):
        if name == materials[i][0]:
            pnd = Material(name, materials[i][1], materials[i][2], materials[i][3], materials[i][4], materials[i][5],materials[i][6])

    return pnd

def get_choices():
    names = []
    designs = []
    for i in range(len(materials)):
        names.append(materials[i][0])
        designs.append(materials[i][6])
    info_arrs = numpy.stack((names,designs),axis=0)

    return info_arrs
