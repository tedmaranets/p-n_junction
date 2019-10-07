class PNDS(object):

    name = ""
    Na = 0
    Nd = 0
    Ni = 0
    er = 0
    stop = 0

    def __init__(self, name, Na, Nd, Ni, er, stop):
        self.name = name
        self.Na = Na
        self.Nd = Nd
        self.Ni = Ni
        self.er = er
        self.stop = stop

def make_pnd(name): # creates an object with necessary properties for calculations
    if name == "AlGaAs":
        pnd = PNDS(name, 1 * 10 ** 18, 5 * 10 ** 14, 34.43134, 10.628, 38)
    elif name == "4H-SiC":
        pnd = PNDS(name, 2.8 * 10 ** 15 , 3 * 10 ** 19, 5 * 10 ** (-9) , 9.66, 145)
    else:
        pnd = PNDS("null",0,0,0,0,0)
    return pnd

