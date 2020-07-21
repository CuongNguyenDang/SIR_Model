import numpy as np
from pandas import date_range
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, drange 
from pylab import legend
from datetime import datetime, timedelta
import sys

from euler import euler_method, improved_euler_method

def plot_data(s, i, r, t=None, t0=datetime(2020, 1, 22), dt=timedelta(days=1)):
    if t is None:
        t = drange(t0, t0 + s.shape[0] * dt, dt)
    
    fig, ax = plt.subplots() 
    ax.plot_date(t, i, 'r-o', label="Nhiễm bệnh") 
    ax.plot_date(t, r, 'b-x', label="Hồi phục")
    
    fig.autofmt_xdate()
    
    ax.set_title("Giá trị I, R thực")
    legend(loc='upper left')
    
    plt.show()


def plot_method(s0=796702206,
                i0=2,
                r0=0,
                beta=0.1126,
                gamma=0.0252,
                t0=datetime(2020, 1, 22),
                dt=timedelta(days=1),
                nStep=100,
                t=None,
                method="EulerMethod"):
    if method == "ImprovedEulerMethod":
        method = improved_euler_method
        methodName = "Euler mở rộng"
    else:
        method = euler_method
        methodName = "Euler"
        
    if t is None:
        t = drange(t0, t0 + (nStep + 1) * dt, dt)
    
    s, i, r = np.rint(method(s0, i0, r0, beta, gamma, t)).astype(int)
    
    print("  {:} {: >15} {: >20} ".format("Ngày","Ca nhiễm","Ca hồi phục"))
    dates = date_range(t0, t0 + nStep * dt, nStep + 1)
    for date, i_t, r_t in zip(dates, i, r):
        print("{:>5} {: >20} {: >20} ".format(date.strftime("%d/%m"), i_t, r_t))
    
    fig, ax = plt.subplots() 
    ax.plot_date(t, i, 'r-o', label="Nhiễm bệnh")
    ax.plot_date(t, r, 'b-x', label="Hồi phục")
    
    fig.autofmt_xdate()
    
    ax.set_title("Sử dụng giải thuật " + methodName + " để xấp xỉ các đại lượng I, R")
    legend(loc='upper left')
    
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