import numpy as np


def dSIR(s, i, r, beta, gamma, dt):
    """Define dS(t), dI(t) and dR(t)."""
    return np.array([-beta / (s + i + r) * i * s,
                     beta / (s + i + r)  * i * s - gamma * i,
                     gamma * i]) * dt


def euler_step(s0, i0, r0, beta, gamma, dt):
    """Approximate S(t), I(t), R(t) by Euler method."""
    return np.array([s0, i0, r0]) + dSIR(s0, i0, r0, beta, gamma, dt)


def euler_method(s0, i0, r0, beta, gamma, t):
    """
    Approximate S, I, R in time range t.
    
    Parameters
    ----------
    s0:      float
        Initial number of susceptible individuals, S(0)
    i0:      float
        Initial number of infectious individuals, I(0)
    r0:      float
        Initial number of recovered individuals, R(0)
    beta:    float
        Average number of contacts per person per time
    gamma:   float
        Probability of an infectious individual recovering
    t:       array of float with size n
        Concerned points in time

    Returns
    ------
    s:       ndarray with size n
        Estimated S values at all concerned points in time
    i:       ndarray with size n
        Estimated S values at all concerned points in time
    r:       ndarray with size n
        Estimated S values at all concerned points in time
    """
    
    s = [s0]
    i = [i0]
    r = [r0]
    for idx in range(1, len(t)):
        s0, i0, r0 = euler_step(s0, i0, r0, beta, gamma, t[idx] - t[idx - 1])
        s.append(s0)
        i.append(i0)
        r.append(r0)

    return np.array(s), np.array(i), np.array(r)


def improved_euler_step(s0, i0, r0, beta, gamma, dt):
    """approx i(t), r(t) by improved euler method"""
    s1, i1, r1 = euler_step(s0, i0, r0, beta, gamma, dt)
    return np.array([s0, i0, r0]) \
    + (dSIR(s0, i0, r0, beta, gamma, dt) + dSIR(s1, i1, r1, beta, gamma, dt)) / 2


def improved_euler_method(s0, i0, r0, beta, gamma, t):
    s = [s0]
    i = [i0]
    r = [r0]
    for idx in range(1, len(t)):
        s0, i0, r0 = improved_euler_step(s0, i0, r0, beta, gamma, t[idx] - t[idx - 1])
        s.append(s0)
        i.append(i0)
        r.append(r0)

    return np.array(s), np.array(i), np.array(r)