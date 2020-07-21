import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, drange 
import pylab
from datetime import datetime, timedelta
import sys

import euler

def plot_data(s, i, r, t=None, t0=datetime(2020, 1, 22), dt=timedelta(days=1)):
    if t is None:
        t = drange(t0, t0 + s.shape[0] * dt, dt)
    
    fig, ax = plt.subplots() 
    ax.plot_date(t, i, 'r-o', label="Nhiễm bệnh") 
    ax.plot_date(t, r, 'b-x', label="Hồi phục")
    
    fig.autofmt_xdate() 
    ax.xaxis.set_major_formatter(DateFormatter('%m/%y'))
    ax.xaxis.set_minor_formatter(DateFormatter('%d')) 
    ax.fmt_xdata = DateFormatter('%S:%M:%H %d/%m/%y')
    
    ax.set_title("Giá trị I, R thực")
    pylab.legend(loc='upper left')
    
    plt.show()


def plot_method(s0=796702206,
                i0=2,
                r0=0,
                beta=0.1126,
                gamma=0.0252,
                dt=timedelta(days=1),
                nStep=None,
                t=None,
                method="EulerMethod"):
    if method == "ImprovedEulerMethod":
        method = euler.improved_euler_method
        methodName = "Euler mở rộng"
    else:
        method = euler.euler_method
        methodName = "Euler"
    
    s, i, r = method(s0, i0, r0, beta, gamma, dt, nStep)
    
    print("  {:} {: >15} {: >20} ".format("Ngày","Ca nhiễm","Ca hồi phục"))
    for t, (i_t, r_t) in enumerate(zip(i, r)):
        print("{:>5} {: >20} {: >20} ".format(t, i_t, r_t))
    
    
    t = np.linspace(0, dt*nStep, dt*nStep + 1)
    plt.plot(t, i, 'r-o', label="Nhiễm bệnh")
    plt.plot(t, r, 'b-x', label="Hồi phục")
    
    plt.title("Sử dụng giải thuật " + methodName + " để xấp xỉ các đại lượng I, R")
    pylab.legend(loc='upper right')
    
    plt.show()
    

if __name__ == "__main__":
    if len(sys.argv) < 7:
        plot_method()
    elif len(sys.argv) == 7:
        plot_method(s0=sys.argv[1], i0=sys.argv[2], r0=sys.argv[3], \
                    beta=sys.argv[4], gamma=sys.argv[5], nStep=sys.argv[6])
    else:
        plot_method(s0=sys.argv[1], i0=sys.argv[2], r0=sys.argv[3], \
            beta=sys.argv[4], gamma=sys.argv[5], nStep=sys.argv[6], method=sys.argv[7])