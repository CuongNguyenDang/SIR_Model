import numpy as np
from scipy import stats, special
import math


def approximate_lambda_v(s, i, r, n_bucket=5000):
    # approx for beta
    beta = []
    for idx in range(s.shape[0] - 1):
        beta.append((s[idx] - s[idx + 1]) / i[idx] / s[idx])
    beta = np.array(beta) * (s[0] + i[0] + r[0])
    
    min_beta = np.amin(beta)
    bucket_beta = (np.amax(beta) - min_beta) / n_bucket
    map2bucket_beta = np.array([b - min_beta for b in beta]) / bucket_beta
    
    mean_beta = np.sum(beta) / (beta.shape[0])
    mode_beta = (stats.mode(map2bucket_beta.astype(int)) + 0.5) * bucket_beta
    
    lambda_beta = 1 / (mean_beta / mode_beta - 1) + 1
    v_beta = lambda_beta / mean_beta
    
    
    # approx for gamma
    gamma = []
    for idx in range(beta.shape[0]):
        gamma.append((r[idx + 1] - r[idx]) / i[idx])
    gamma = np.array(gamma)
    
    min_gamma = np.amin(gamma)
    bucket_gamma = (np.amax(gamma) - min_gamma) / n_bucket
    map2bucket_gamma = np.array([b - min_gamma for b in gamma]) / bucket_gamma
    
    mean_gamma = np.sum(gamma) / (gamma.shape[0])
    mode_gamma = (stats.mode(map2bucket_gamma.astype(int)) + 0.5) * bucket_gamma
    
    lambda_gamma = 1 / (mean_gamma / mode_gamma - 1) + 1
    v_gamma = lambda_gamma / mean_gamma
    
    
    return (lambda_beta, v_beta), (lambda_gamma, v_gamma)


def pi_beta_gamma(beta,
                  gamma,
                  lambda_beta=1.1631,
                  v_beta=10.3343,
                  lambda_gamma=3.3453,
                  v_gamma=132.9341):
    return math.exp(lambda_beta * math.log(v_beta) - special.loggamma(lambda_beta) \
            + (lambda_beta - 1) * math.log(beta) - v_beta * beta \
            + lambda_gamma * math.log(v_gamma) - special.loggamma(lambda_gamma) \
            + (lambda_gamma - 1) * math.log(gamma) - v_gamma * gamma)
    

if __name__ == "__main__":
    mode_beta = 0.0158
    mode_gamma = 0.0176
    mean_gamma = 0.0252
    mean_beta = 0.1126
    
    print(pi_beta_gamma(mode_beta, mode_gamma))
    print(pi_beta_gamma(mean_beta, mean_gamma))