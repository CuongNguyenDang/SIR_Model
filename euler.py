import math
import numpy as np
from matplotlib import pyplot as plt
import pylab

def suspectible(beta,gamma,i,s):
    return -beta*i*s

def infectious(beta,gamma,i,s):
    return beta*i*s - gamma*i

def recovered(beta,gamma,i,s):
    return gamma*i


def EulerMethod(t, beta, gamma, S0, I0, R0):
    """approx I(t), R(t) by euler method"""
    currentTime = 0
    N = I0 + S0 + R0
    Si, Ii = 0,0
    I, S = I0, S0

    while currentTime < t:
        Si = S + suspectible(beta, gamma, I, S) * delta_t
        Ii = I + infectious(beta, gamma, I, S) * delta_t
        # print([s1,i1])
        I = Ii
        S = Si
        currentTime += delta_t
    newI = Ii
    newR = N - Si - Ii
    return (newI, newR)

def improvedEulerMethod(t, beta, gamma, S0, I0, R0):
    currentTime = 0
    N = I0 + S0 + R0
    Si, Ii = 0,0
    I, S = I0, S0

    while currentTime < t:
        tmpS = S + suspectible(beta, gamma, I, S)
        tmpI = I + infectious(beta, gamma, I, S)
        # print([s1,i1])
        Si = S + delta_t * (suspectible(beta, gamma, I, S) + suspectible(beta, gamma, tmpI, tmpS)) / 2
        Ii = I + delta_t * (infectious(beta, gamma, I, S) + infectious(beta, gamma, tmpI, tmpS)) / 2
        I = Ii
        S = Si
        currentTime += delta_t
    newI = Ii
    newR = N - Si - Ii
    return (newI, newR)


t = np.linspace(0, 8, 9)

beta =  0.002
gamma = 0.5
delta_t = 1
i0 = 7
s0 = 800
r0 = 0
lista_outputs = [(i0,r0)]
listb_outputs = [(i0,r0)]

print("  {:} {: >15} {: >20} ".format('Tuần','Ca nhiễm','Ca hồi phục'))
for i in t[1:]:
    lista_outputs.append(EulerMethod(i, beta, gamma, s0, i0, r0))
    listb_outputs.append(improvedEulerMethod(i, beta, gamma, s0, i0, r0))

i_table = [item[0] for item in lista_outputs]
r_table = [item[1] for item in lista_outputs]

idx = 0
for row in lista_outputs:
    print("{:>5} {: >20} {: >20} ".format(idx, *row))
    idx += 1

plt.plot(t, i_table, 'r-o', label="Nhiễm bệnh")
plt.plot(t, r_table, 'b-x', label="Hồi phục")
plt.title('Sử dụng giải thuật Euler để xấp xỉ các đại lượng I,R')
pylab.legend(loc='upper right')

plt.show()