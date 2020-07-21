import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.special as sps
import random
from regionize_data import regionize 

if __name__ == "__main__":
    S, I, R = regionize()
    S, I, R = S[I != 0], I[I != 0], R[I != 0]
    S, I, R = S[S != 0], I[S != 0], R[S != 0]
    N = S[0] + I[0] + R[0]
    n = len(S)

    beta = np.array([(S[i - 1] - S[i]) * N / (I[i - 1] * S[i - 1]) for i in range(1, n)])
    time = [i for i in range(1, n)]
    #plt.figure(1)
    #plt.plot(time, beta, 'r-o', label = "beta")
    #plt.show()

    m = int(np.amax(beta) * 10) + 2
    beta_value = [0.1 * x for x in range(m)]
    beta_freq = [0 for i in range(m)]
    for i in beta:
        #print(i, end = " ")
        tmp = int(i * 10)
        beta_freq[tmp] += 1
    #plt.figure(2)
    #plt.plot(beta_value, beta_freq, 'r-o', label = "frequency")
    #plt.show()
    
    gamma = np.array([(R[i] - R[i - 1]) / I[i] for i in range(1, n)])
    m = int(np.amax(gamma) / 0.05)
    gamma_value = np.array([i / 20 for i in range(m + 2)])
    gamma_freq = np.array([0 for i in range(m + 2)])
    for i in gamma:
        tmp = int(i * 20)
        gamma_freq[tmp] += 1
    #plt.figure(3)
    #plt.plot(gamma_value, gamma_freq, "r-o", label = "frequency")
    #plt.show()

    beta_prime = np.array([(I[i] - I[i - 1] + gamma[i - 1] * I[i - 1]) * N \
                 / (I[i - 1] * S[i - 1]) for i in range(1, n)])
    beta_error = beta_prime - beta 
    #print(beta_error)
    gamma_prime = np.array([(1 + beta[i - 1] * S[i - 1] / N - I[i] / I[i - 1]) for i in range(1, n)])
    gamma_error = gamma_prime - gamma 
    #print(gamma_error)

    s = random.choices(list(beta), k = 1000000)
    #print(s)
    tmp1 = np.mean(s)
    tmp2 = np.var(s)
    scale = tmp2 / tmp1 
    shape = tmp1 / scale
    print(shape, 1 / scale)
    
    s = random.choices(list(gamma), k = 1000000)
    #print(s)
    tmp1 = np.mean(s)
    tmp2 = np.var(s)
    scale = tmp2 / tmp1 
    shape = tmp1 / scale
    print(shape, 1 / scale)
    # count, bins, ignored = plt.hist(s, 50, density=True)
    # print(bins)
    #lny = (shape - 1) * np.log(bins) - bins / scale - np.log(sps.gamma(shape)*scale**shape)
    #y = np.exp(lny)
    # y = bins**(shape - 1)*(np.exp(-bins/scale) / (sps.gamma(shape)*scale**shape))
    # plt.plot(bins, y, linewidth=2, color='r')
    # plt.show()
    
    '''
    s = random.choices(list(gamma), k = 10000)
    #print(s)
    lambd = 1 / np.mean(s)
    count, bins, ignored = plt.hist(s, 50, density=True)
    #lny = (shape - 1) * np.log(bins) - bins / scale - np.log(sps.gamma(shape)*scale**shape)
    #y = np.exp(lny)
    y = lambd * np.exp(-lambd * bins)
    plt.plot(bins, y, linewidth=2, color='r')
    plt.show()
    '''

    '''
    s = random.choices(list(gamma), k = 10000)
    #s = s[s != 0]
    #print(s)
    alpha = (1 - np.mean(s)) / np.var(s) - 1 / np.mean(s)
    alpha *= np.mean(s) ** 2
    beta = alpha * (1 - np.mean(s)) / np.mean(s)
    count, bins, ignored = plt.hist(s, 100, density=True)
    #lny = (shape - 1) * np.log(bins) - bins / scale - np.log(sps.gamma(shape)*scale**shape)
    #y = np.exp(lny)
    y = sps.gamma(alpha + beta) / sps.gamma(alpha) / sps.gamma(beta) * np.power(bins, alpha - 1) \
        * np.power((1 - bins), beta - 1)
    plt.plot(bins, y, linewidth=2, color='r')
    plt.show()
    '''