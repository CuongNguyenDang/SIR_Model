import numpy as np
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt
import math
import pylab
import csv
from sampling import metropolis_hastings
from sampling import pgauss
from regionize_data import regionize
from gamma_dist import gamma_dist, f_beta_gamma


s, i, r = regionize()
x = [i + j for i, j in zip(i, r) if i + j != 0]

samples = metropolis_hastings(f_beta_gamma, 10000, scale = [0.25,0.01])
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