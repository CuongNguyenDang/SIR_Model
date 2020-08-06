import numpy as np
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt
import math
import pylab
from sampling import metropolis_hastings
from regionize_data import regionize
from gamma_dist import gamma_dist_exp, f_beta_gamma


s, i, r = regionize()
x = np.array([x + y for x, y in zip(i, r) if x + y != 0])

for _ in range(20):
    samples = metropolis_hastings(np.array([.1, .025]),
                                lambda x: f_beta_gamma(x[0], x[1]),
                                10000)

    beta = np.array(samples[:, 0])
    gamma = np.array(samples[:, 1])

    denom = np.array([sum([gamma_dist_exp(val, b, c) for val in x]) for b, c in zip(beta, gamma)])
    numer = denom + np.array([math.log(b / c) for b, c in zip(beta, gamma)])

    max_numer = np.amax(numer)
    max_denom = np.amax(denom)

    numer = numer[numer > max_numer - 20]
    denom = denom[denom > max_denom - 20]

    numer -= np.array([max_numer - 10] * numer.shape[0])
    denom -= np.array([max_denom - 10] * denom.shape[0])

    numer = sum([math.exp(x) for x in numer])
    denom = sum([math.exp(x) for x in denom])

    R0 = numer / denom * math.exp(max_numer - max_denom)
    print("R0 =", R0)