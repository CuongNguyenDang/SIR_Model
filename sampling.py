import numpy as np  # ver 1.19.0
import scipy.stats as st  # ver 1.5.1
import seaborn as sns  # ver 0.10.1
from matplotlib import pyplot as plt  # ver 3.2.2
from gamma_dist import f_beta_gamma

def pgauss(x, y):
    # N(0,1)
    return st.multivariate_normal.pdf([x, y], mean=np.array([0, 0]))


def metropolis_hastings(p, iter, scale=[1, 1]):
    """
    Use Metropolis-Hastings algorithm to draw samples from probability distribution p

    Parameters
    ----------
    p:     string
        The desired probability distribution (we have 'pgauss' and 'f_beta_gama' distribution).
    iter:  int
        Size of sample set.
    scale: float or array_like of floats
        "width" of the distribution.

    Returns
    ------
    out: ndarray
         Samples stastify p distribution
    """
    # The starting point of our Markov chain is the estimated value of (α, β) from Raggett (1982)?????
    beta, gamma = 0.27 / 2.47, 0.19 / 7.58
    samples = np.zeros((iter, 2))
    count = 0
    while count < iter:
        beta_star, gamma_star = np.random.multivariate_normal(
            mean=[beta, gamma], cov=np.diag(scale))
        r = p(beta_star, gamma_star) * st.multivariate_normal.pdf([beta, gamma], mean=[beta, gamma], cov=np.diag(scale)) / p(
            beta, gamma) / st.multivariate_normal.pdf([beta_star, gamma_star], mean=[beta, gamma], cov=np.diag(scale))
        if np.random.uniform(0.0, 1.0) < r:
            beta, gamma = beta_star, gamma_star        # accept beta_star,gamma_star
        #     # uncomment this (3 lines from here) to plot accepted and injected points
        #     plt.plot(beta_star,gamma_star,'b.')
        # else: plt.plot(beta_star,gamma_star,'r.')

        # inject beta_star,gamma_star
        samples[count] = np.array([beta, gamma])
        count += 1
    print('Accept Rate = {0}%'.format(
        len(np.unique(samples, axis=0))/iter*100))
    # print(np.unique(samples,axis = 0))
    return samples


if __name__ == "__main__":
    samples = metropolis_hastings(f_beta_gamma, 10000, scale=[0.25, 0.01])
    h = sns.jointplot(samples[:, 0], samples[:, 1], kind='reg')  # 'kde')
    h.set_axis_labels(r'$\beta$', r'$\gamma$')
    plt.suptitle('Lấy mẫu bằng Metropolis-Hastings')
    plt.savefig('sampling.png')

    plt.show()
