class Material(object):

    def __init__(self, name, Na, Nd, Ni, er, stop):
        self.name = name
        self.Na = Na
        self.Nd = Nd
        self.Ni = Ni
        self.er = er
        self.stop = stop

# data list array
materials = [["AlGaAs (30%Al 70%Ga)",1 * 10 ** 16, 1 * 10 ** 17, 2100, 12.048, 38.5]
             ]

def make_pnd(name): # creates an object with necessary properties for calculations
    for i in range(len(materials)):
        if name == materials[i][0]:
            pnd = Material(name, materials[i][1], materials[i][2], materials[i][3], materials[i][4], materials[i][5])

    return pnd

def get_choices():
    arr = []
    for i in range(len(materials)):
        arr.append(materials[i][0])
    return arr
