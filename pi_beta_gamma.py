import numpy as np
from scipy import stats, special
import math


def approx_alpha_beta(x, n_bucket):
    min_x = np.amin(x)
    bucket = (np.amax(x) - min_x) / n_bucket
    map2bucket = np.array([x_i - min_x for x_i in x]) / bucket
    
    mean = np.sum(x) / (x.shape[0])
    mode = (stats.mode(map2bucket.astype(int))[0] + 0.5) * bucket
    
    print((mean, mode))
    
    alpha = 1 / (mean / mode - 1) + 1
    beta = alpha / mean
    
    return alpha, beta


def approx_lambda_v(s, i, r, n_bucket=5000):
    s, i, r = s[i != 0], i [i != 0], r[i != 0]
    s, i, r = s[s != 0], i [s != 0], r[s != 0]
    
    # beta samples
    beta = []
    for idx in range(s.shape[0] - 1):
        beta.append((s[idx] - s[idx + 1]) / i[idx] / s[idx])
    beta = np.array(beta) * (s[0] + i[0] + r[0])
    
    for idx in range(1, beta.shape[0] - 1):
        if beta[idx] == 0:
            for jdx in range(idx + 1, beta.shape[0] - 1):
                if beta[jdx] != 0:
                    break
            
            step = (beta[jdx] - beta[idx - 1]) / (jdx - idx + 1)
            
            for kdx in range(idx, jdx):
                beta[kdx] = beta[kdx - 1] + step
    
    # gamma samples
    gamma = []
    for idx in range(s.shape[0] - 1):
        gamma.append((r[idx + 1] - r[idx]) / i[idx])
    gamma = np.array(gamma)
    
    for idx in range(1, gamma.shape[0] - 1):
        if gamma[idx] == 0:
            for jdx in range(idx + 1, gamma.shape[0] - 1):
                if gamma[jdx] != 0:
                    break
            
            step = (gamma[jdx] - gamma[idx - 1]) / (jdx - idx + 1)
            
            for kdx in range(idx, jdx):
                gamma[kdx] = gamma[kdx - 1] + step
    
    
    return approx_alpha_beta(beta, n_bucket), approx_alpha_beta(gamma, n_bucket)


def gamma_dist(x, alpha, beta):
    return math.exp(alpha * math.log(beta) - special.loggamma(alpha) \
            + (alpha - 1) * math.log(x) - beta * x)


def pi_beta_gamma(beta,
                  gamma,
                  lambda_beta=1.0672,
                  v_beta=7.9013,
                  lambda_gamma=2.0848,
                  v_gamma=61.4889):
    return gamma_dist(beta, lambda_beta, v_beta) \
        * gamma_dist(gamma, lambda_gamma, v_gamma)
    

if __name__ == "__main__":
    mode_beta = 0.0085
    mode_gamma = 0.0176
    
    mean_beta = 0.1351
    mean_gamma = 0.0339
    
    print(pi_beta_gamma(mode_beta, mode_gamma))
    print(pi_beta_gamma(mean_beta, mean_gamma))