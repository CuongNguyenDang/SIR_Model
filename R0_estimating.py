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
x = [0] + [i + j for i, j in zip(i, r) if i + j != 0]
x = [x[i] - x[i - 1] for i in range(1, len(x)) if x[i] != x[i - 1]]

print(x)

samples = metropolis_hastings(f_beta_gamma, 10000)
beta = samples[:, 0]
gamma = samples[:, 1]

numerator = 0
denominator = 0
for b, c in zip(beta, gamma):
    pi = 1.
    for val in x:
        pi *= gamma_dist(val, b, c)
    print(b/c)
    numerator += pi * b / c
    denominator += pi

E_R0 = numerator / denominator
print(numerator, denominator)