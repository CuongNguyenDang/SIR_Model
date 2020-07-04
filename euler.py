import math
import numpy as np
from matplotlib import pyplot as plt
import pylab

def suspectible(beta,gama,i,s):
    return -beta*i*s

def infectious(beta,gama,i,s):
    return beta*i*s - gama*i

def recovered(beta,gama,i,s):
    return gama*i


def euler(t,beta,gama,s0,i0,r0):
    """approx I(t), R(t) by euler method"""
    t_init = 0
    N = i0 + s0 + r0
    s1,i1 = 0,0
    i_init,s_init = i0,s0

    while t_init < t:
        s1 = s_init + suspectible(beta,gama,i_init,s_init)*delta_t
        i1 = i_init + infectious(beta,gama,i_init,s_init) *delta_t
        # print([s1,i1])
        i_init = i1
        s_init = s1
        t_init += delta_t
    new_i = i1
    new_r = N - s1 - i1
    return (new_i,new_r)


t = np.linspace(0, 8, 9)

beta =  0.002
gama = 0.5
delta_t = 1
i0 = 7
s0 = 800
r0 = 0
lista_outputs = [(i0,r0)]

print("  {:} {: >15} {: >20} ".format('Tuần','Ca nhiễm','Ca hồi phục'))
for i in t[1:]:
    lista_outputs.append(euler(i,beta,gama,s0,i0,r0))

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
