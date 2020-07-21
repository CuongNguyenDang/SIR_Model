import numpy as np #ver 1.19.0
import scipy.stats as st #ver 1.5.1
import seaborn as sns #ver 0.10.1
from matplotlib import pyplot as plt #ver 3.2.2
from pi_beta_gamma import f_beta_gamma
mus = np.array([0, 0])


def circle(x, y):
    return (x-1)**2 + (y-2)**2 - 3**2


def pgauss(x, y):
    # N(0,1)
    return st.multivariate_normal.pdf([x, y], mean=mus)


def metropolis_hastings(p, iter):
    beta, gamma = 0.27 / 2.47, 0.19 / 7.58 #The starting point of our Markov chain is the estimated value of (α, β) from Raggett (1982)?????
    samples = np.zeros((iter, 2))
    count = 0
    while count < iter:
        beta_i, gamma_i = np.array([beta, gamma]) + np.random.normal(size=2)
        if beta_i > 0 and gamma_i > 0:
            if np.random.uniform(0.0, 1.0) < p(beta_i, gamma_i) / p(beta, gamma):
                beta, gamma = beta_i, gamma_i
                samples[count] = np.array([beta, gamma])
                count +=1
    return samples


if __name__ == "__main__":
    samples = metropolis_hastings(f_beta_gamma,10000)
    sns.jointplot(samples[:, 0], samples[:, 1])
    print(samples)
    plt.show()