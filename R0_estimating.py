import numpy as np
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt
import math
import pylab
import csv
from sampling import metropolis_hastings
from sampling import circle
from sampling import pgauss
from regionize_data import regionize
from gamma_dist import gamma_dist, f_beta_gamma

# def read_csv(file_name):
#     with open(file_name) as csv_file:
#         l = []
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         for row in csv_reader:
#             if(line_count == 1):
#                 l = list(map(int,row[4:]))
#             elif(line_count >1):
#                 int_row = list(map(int,row[4:]))
#                 for i in range(len(int_row)):
#                     l[i] += int_row[i]
#             line_count +=1
#     return l
# #to test!!
# file_i ='data/time_series_covid19_confirmed_global.csv'
# file_r = 'data/time_series_covid19_deaths_global.csv'


s, i, r = regionize()
x = [i + j for i, j in zip(i, r) if i + j != 0]

samples = metropolis_hastings(f_beta_gamma, 10000)
beta = samples[:, 0]
gamma = samples[:, 1]

print(sum(beta) / len(beta))
print(sum(gamma) / len(gamma))
E_R0 = 0
for b, c in zip(beta, gamma):
    pi = 1.
    for val in x:
        pi *= gamma_dist(val, b, c)
    E_R0 += pi * b / c

print(E_R0)