import numpy as np
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt
import math
import pylab
import csv

def read_csv(file_name):
    with open(file_name) as csv_file:
        l = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if(line_count == 1):
                l = list(map(int,row[4:]))
            elif(line_count >1):
                int_row = list(map(int,row[4:]))
                for i in range(len(int_row)):
                    l[i] += int_row[i]
            line_count +=1
    return l
