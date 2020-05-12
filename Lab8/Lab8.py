import numpy as np
import scipy.stats as stats
from tabulate import tabulate


def mean_interval(samples, gamma=0.95):
    m = np.mean(samples)
    s = np.std(samples)
    n = len(samples)
    low_b = m - s * stats.t.ppf((1 + gamma) / 2, n - 1) / (n - 1) ** 0.5
    high_b = m + s * stats.t.ppf((1 + gamma) / 2, n - 1) / (n - 1) ** 0.5
    return low_b, high_b


def std_interval(samples, gamma=0.95):
    s = np.std(samples)
    n = len(samples)
    low_b = s * (n / stats.chi2.ppf((1 + gamma) / 2, n - 1)) ** 0.5
    high_b = s * (n / stats.chi2.ppf((1 - gamma) / 2, n - 1)) ** 0.5
    return low_b, high_b


def mean_interval_asimpt(samples, gamma=0.95):
    m = np.mean(samples)
    s = np.std(samples)
    n = len(samples)
    u = stats.norm.ppf((1 + gamma) / 2)
    low_b = m - s * u / (n ** 0.5)
    high_b = m + s * u / (n ** 0.5)
    return low_b, high_b


def std_interval_asimpt(samples, gamma=0.95):
    m = np.mean(samples)
    s = np.std(samples)
    n = len(samples)
    m_4 = stats.moment(samples, 4)
    e = m_4 / s**4 - 3
    u = stats.norm.ppf((1 + gamma) / 2)
    U = u * (((e + 2) / n) ** 0.5)
    low_b = s * (1 + 0.5 * U) ** (-0.5)
    high_b = s * (1 - 0.5 * U) ** (-0.5)
    return low_b, high_b


if __name__ == '__main__':
    sizes = [20, 100]
    rows = []
    for size in sizes:
        samples = np.random.normal(0, 1, size=size)
        
        rows.append(["n = {}".format(size), "m", "$\sigma$"])
        lb_m, hb_m = mean_interval(samples)
        lb_s, hb_s = std_interval(samples)
        rows.append([" ", "{:.2f} < m < {:.2f}".format(lb_m, hb_m),"{:.2f} < $\sigma$ < {:.2f}".format(lb_s, hb_s)])
        rows.append([" ", " ", " "])

    print(tabulate(rows, [], tablefmt="latex_raw"))  

    rows = []
    for size in sizes:
        samples = np.random.normal(0, 1, size=size)
        
        rows.append(["n = {}".format(size), "m", "$\sigma$"])
        lb_m, hb_m = mean_interval_asimpt(samples)
        lb_s, hb_s = std_interval_asimpt(samples)
        rows.append([" ", "{:.2f} < m < {:.2f}".format(lb_m, hb_m),"{:.2f} < $\sigma$ < {:.2f}".format(lb_s, hb_s)])
        rows.append([" ", " ", " "])

    print(tabulate(rows, [], tablefmt="latex_raw")) 