import numpy
import pandas

# data list array
materials = [["AlGaAs (30%Al 70%Ga)", 12.048, 40.5, "D19.1 Wafer", "AlGaAs_D191.csv"],
             ["4H-SiC", 9.7, 144, "High Detection \n Sensitivity of \n Ultraviolet \n 4H-SiC APDs \n- UVA", "4HSiC.csv"]]

class Material(object):

    def __init__(self, name, er, stop, design, data_path):
        self.name = name
        self.er = er
        self.stop = stop
        self.design = design
        self.data_path = data_path # in data folder, as .csv file


def make_pnd(name): # creates an object with necessary properties for calculations
    for i in range(len(materials)):
        if name == materials[i][0]:
            pnd = Material(name, materials[i][1], materials[i][2], materials[i][3], materials[i][4])

    return pnd

def make_layer_array(pnd):
    layer_data = pandas.read_csv(pnd.data_path, header=None, sep=',')
    layer_array = numpy.array(layer_data)
    return layer_array

def get_choices():
    names = []
    designs = []
    for i in range(len(materials)):
        names.append(materials[i][0])
        designs.append(materials[i][3])
    info_arrs = numpy.stack((names,designs),axis=0)

    return info_arrs
