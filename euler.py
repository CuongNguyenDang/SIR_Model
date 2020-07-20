import math
import numpy as np
from matplotlib import pyplot as plt
import pylab

def dSIR(s, i, r, beta, gamma, dt):
    return np.array([-beta / (s + i + r) * i * s,
                     beta / (s + i + r)  * i * s - gamma * i,
                     gamma * i]) * dt


def eulerMethod(s0, i0, r0, beta, gamma, dt):
    """approx i(t), r(t) by euler method"""
    return np.array([s0, i0, r0]) + dSIR(s0, i0, r0, beta, gamma, dt)


def improvedEulerMethod(s0, i0, r0, beta, gamma, dt):
    """approx i(t), r(t) by improved euler method"""
    s1, i1, r1 = eulerMethod(s0, i0, r0, beta, gamma, dt)
    return np.array([s0, i0, r0]) \
    + (dSIR(s0, i0, r0, beta, gamma, dt) + dSIR(s1, i1, r1, beta, gamma, dt)) / 2


def plotEuler(s0=793, i0=7, r0=0, beta=1.6, gamma=0.5, dt=1, nStep=8, method="EulerMethod"):
    if method == "ImprovedEulerMethod":
        method = improvedEulerMethod
        methodName = "Euler mở rộng"
    else:
        method = eulerMethod
        methodName = "Euler"
    
    t = np.linspace(dt, dt*nStep, dt*nStep)
    print(type(t))
    sir = []
    for _ in range(nStep):
        s0, i0, r0 = method(s0, i0, r0, beta, gamma, dt)
        sir.append((s0, i0, r0))
    
    print("  {:} {: >15} {: >20} ".format("Tuần","Ca nhiễm","Ca hồi phục"))
    for idx, row in enumerate(sir):
        print("{:>5} {: >20} {: >20} ".format(idx + 1, row[1], row[2]))
    
    plt.plot(t, [x[1] for x in sir], 'r-o', label="Nhiễm bệnh")
    plt.plot(t, [x[2] for x in sir], 'b-x', label="Hồi phục")
    plt.title("Sử dụng giải thuật " + methodName + " để xấp xỉ các đại lượng I, R")
    pylab.legend(loc='upper right')
    
    plt.show()
    

if __name__ == "__main__":
    plotEuler()