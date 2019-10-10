import pandas
import numpy
import mod_materials_11

pnd = mod_materials_11.make_pnd("AlGaAs (30%Al 70%Ga)")
layerdata = pandas.read_csv(pnd.data_path, header=None, sep=',')
layer_array = numpy.array(layerdata)
print(layer_array)

def calc_dep_widths(rev_bias, pnd):
    # Ni = intrinsic carrier concentration, er = relative permittivity
    Ni = pnd.Ni
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
    p_indexes = []
    n_indexes = []
    p_layer_depths = []
    n_layer_depths = []
    # i think this following part is a bit hard coded - Teddy 10/10/19
    # maybe doesn't matter if future material data is formatted the same
    i = first_n_index
    while layer_array[i,2] != 'U': # up the column
        n_indexes.append(i)
        n_layer_depths.append(layer_array[i,4])
        i -= 1
    i = first_p_index
    while i != len(layer_array[0:,2]): # down the column
        p_indexes.append(i)
        p_layer_depths.append(layer_array[i,4])
        i += 1

    p_depths_array = numpy.column_stack((p_indexes, p_layer_depths))
    n_depths_array = numpy.column_stack((n_indexes, n_layer_depths))
    print(p_depths_array)
    print(n_depths_array)

    return 1

revbias = list(numpy.arange(0, pnd.stop, 0.5))
calc_dep_widths(revbias,pnd)