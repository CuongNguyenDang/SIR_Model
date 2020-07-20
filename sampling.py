import numpy as np #ver 1.19.0
import scipy.stats as st
import seaborn as sns
from matplotlib import pyplot as plt
mus = np.array([0, 0])


def circle(x, y):
    return (x-1)**2 + (y-2)**2 - 3**2


def pgauss(x, y):
    # N(0,1)
    return st.multivariate_normal.pdf([x, y], mean=mus)


def metropolis_hastings(p, iter):
    beta, gamma = 0.0212, 3.39 #The starting point of our Markov chain is the estimated value of (α, β) from Raggett (1982)?????
    samples = np.zeros((iter, 2))
    count = 0
    while count < iter:
        betaStar, gammaStar = np.array([beta, gamma]) + np.random.normal(size=2)
        if betaStar>0 and gammaStar>0:
            if np.random.uniform(0.0, 1.0) < p(betaStar, gammaStar) / p(beta, gamma):
                beta, gamma = betaStar, gammaStar
                samples[count] = np.array([beta, gamma])
                count +=1
    return samples
if __name__ == "__main__":
    samples = metropolis_hastings(circle,10000)
    sns.jointplot(samples[:, 0], samples[:, 1])
    print(samples)
    plt.show()