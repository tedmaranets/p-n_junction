class Material(object):

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

# data list array
# eventually make this a file (ascii, excel, origin?)
materials = [["AlGaAs",1 * 10 ** 18, 5 * 10 ** 14, 34.43134, 10.628, 38],
             ["4H-SiC",2.8 * 10 ** 15 , 3 * 10 ** 19, 5 * 10 ** (-9) , 9.66, 145]
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
