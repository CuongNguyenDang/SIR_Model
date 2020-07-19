import numpy as np
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt


mus = np.array([0, 0])


def circle(x, y):
    return (x-1)**2 + (y-2)**2 - 3**2


def pgauss(x, y):
    # N(0,1)
    return st.multivariate_normal.pdf([x, y], mean=mus)


def metropolis_hastings(p, iter=1000):
    beta, gamma = 0., 0.
    samples = np.zeros((iter, 2))

    for i in range(iter):
        betaStar, gammaStar = np.array([beta, gamma]) + np.random.normal(size=2)
        if np.random.uniform(0.0, 1.0) < p(betaStar, gammaStar) / p(beta, gamma):
            beta, gamma = betaStar, gammaStar
        samples[i] = np.array([beta, gamma])

    return samples


samples = metropolis_hastings(circle, iter=10000)
sns.jointplot(samples[:, 0], samples[:, 1])

samples = metropolis_hastings(pgauss, iter=10000)
sns.jointplot(samples[:, 0], samples[:, 1])

plt.show()