import numpy as np #ver 1.19.0
import scipy.stats as st #ver 1.5.1
import seaborn as sns #ver 0.10.1
from matplotlib import pyplot as plt #ver 3.2.2
from gamma_dist import f_beta_gamma
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
        #beta_i, gamma_i = np.array([beta, gamma]) + np.random.normal(size=2)
        #beta_i, gamma_i = np.array([np.random.normal(loc=beta), np.random.normal(loc=gamma)])
        beta_i, gamma_i = np.random.multivariate_normal(mean=[beta, gamma], cov=[[1,0],[0,1]])
        if beta_i > 0 and gamma_i > 0:
            #tmp1 = st.multivariate_normal.pdf([beta_i, gamma_i], [beta, gamma], [[1,0],[0,1]])
            #tmp2 = st.multivariate_normal.pdf([beta, gamma], [beta_i, gamma_i], [[1,0],[0,1]])
            #if (tmp1 - tmp2) ** 2 > 1e-6:
            #    print(tmp1, tmp2)
            if np.random.uniform(0.0, 1.0) < p(beta_i, gamma_i) / p(beta, gamma):
                beta, gamma = beta_i, gamma_i
            samples[count] = np.array([beta, gamma])
            count +=1
    return samples


if __name__ == "__main__":
    samples = metropolis_hastings(f_beta_gamma, 10000)
    h = sns.jointplot(samples[:, 0], samples[:, 1])
    h.set_axis_labels(r'$\beta$',r'$\gamma$')
    plt.suptitle('Lấy mẫu bằng Metropolis-Hastings')
    plt.savefig('sampling.png')
    #print(samples)
    #print(np.mean(samples[:,0]) ** 2 / np.var(samples[:,0]))
    #print(np.mean(samples[:,0]) / np.var(samples[:,0]))
    plt.show()