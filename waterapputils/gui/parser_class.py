import numpy as np

class Parser(object):
    """ provides functionality to parse a text file to extract letter frequencies """
    def __init__(self):
        pass
        
    def parse(self, filename):
        """ method that parses a 2 columns tab delimited text file and returns the x and y values """
        
        x = []
        y = []
        with open(filename) as f:
            for line in f:
                x_value = float(line.split('\t')[0].strip())
                y_value = float(line.split('\t')[1].strip())
                x.append(x_value)
                y.append(y_value)
        
        # convert x and y to numpy arrays
        x = np.array(x)
        y = np.array(y)
        
        return x, y