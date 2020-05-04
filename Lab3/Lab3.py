import scipy.stats as stats
import math
import matplotlib.pyplot as plt
from tabulate import tabulate


def mean(X):
    return sum(X) / len(X)

def D(X):
    sqrX = [i**2 for i in X]
    return mean(sqrX) - mean(X)**2

def generator(distr, n):
    if (distr == "Normal"):
        sample = stats.norm.rvs(0, 1, n)
    if (distr == "Cauchy"):
        sample = stats.cauchy.rvs(0, 1, n)
    if (distr == "Laplace"):
        sample = stats.laplace.rvs(0, 1/math.sqrt(2), n)
    if (distr == "Poisson"):
        sample = stats.poisson.rvs(10, size = n)
    if (distr == "Uniform"):
        sample = stats.uniform.rvs(-math.sqrt(3), 2*math.sqrt(3), n)

    sample.sort()
    return sample


def quantile(array, p):
    return array[int(len(array)*p) if p != 1 else len(array) - 1]


repeat = 1000

if __name__ == '__main__':
    distributions = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']
    sizes = [20, 100]
    n = 1000


    for distr in distributions:
        line_props = dict(color="black", alpha=0.3, linestyle="dashdot")
        bbox_props = dict(color="b", alpha=0.9)
        flier_props = dict(marker="o", markersize=4)
        plt.figure()
        plt.boxplot((generator(distr, sizes[0]), generator(distr, sizes[1])), whiskerprops=line_props, boxprops=bbox_props, flierprops=flier_props, labels=["n = 20", "n = 100"])
        plt.ylabel("X")
        plt.title(distr)
        #plt.savefig(distr + '.png', format='png')
        #plt.show()

        headers = ["distribution name", "proportion of ejections", "D"]
        for size in sizes:
            rows = list()
            emissions_list = list()
            for i in range(1000):
                count = 0
                sample = generator(distr, size)

                down_bound = quantile(sample, 0.25) - 1.5 * (quantile(sample, 0.75) - quantile(sample, 0.25))
                up_bound = quantile(sample, 0.75) + 1.5 * (quantile(sample, 0.75) - quantile(sample, 0.25))

                for i in sample:
                    if i > up_bound or i < down_bound: count += 1

                emissions_list.append(count / size)
            
            rows.append([str(distr) + ", n = " + str(size),  mean(emissions_list), D(emissions_list)])
            print(tabulate(rows, headers, tablefmt="latex"))

