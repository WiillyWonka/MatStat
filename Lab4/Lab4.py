import scipy.stats as stats
import math
import numpy as np
import matplotlib.pyplot as plt

def poisson_aprox(k):
    return (10**k)/math.gamma(k + 1)*math.exp(-10)

def generatorDensity(distr, x):
    if (distr == "Normal"):
        return stats.norm.pdf(x, 0, 1)
    if (distr == "Cauchy"):
        return stats.cauchy.pdf(x, 0, 1)
    if (distr == "Laplace"):
        return stats.laplace.pdf(x, 0, 1/math.sqrt(2))
    if (distr == "Poisson"):
        return [poisson_aprox(i) for i in x]
    if (distr == "Uniform"):
        return stats.uniform.pdf(x, -math.sqrt(3), 2*math.sqrt(3))

def generatorDistrFunc(distr, x):
    if (distr == "Normal"):
        return stats.norm.cdf(x, 0, 1)
    if (distr == "Cauchy"):
        return stats.cauchy.cdf(x, 0, 1)
    if (distr == "Laplace"):
        return stats.laplace.cdf(x, 0, 1/math.sqrt(2))
    if (distr == "Poisson"):
        return stats.poisson.cdf(x, 10)
    if (distr == "Uniform"):
        return stats.uniform.cdf(x, -math.sqrt(3), 2*math.sqrt(3))


def generatorRandomArray(distr, n):
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

def clump(x, left_bound, right_bound):
    i_left = 0
    i_right = len(x) - 1
    for i in range(len(x)):
        if x[i] < left_bound:
            i_left = i + 1
        if x[i] < right_bound:
            i_right = i

    return x[i_left:i_right]


if __name__ == '__main__':
    distributions = ['Normal', 'Cauchy', 'Laplace', 'Poisson', 'Uniform']
    sizes = [20, 60, 100]
    n = 1000


    for distr in distributions:
        
        plt.figure(figsize=(10, 4))
        plt.subplots_adjust(wspace=0.5)
        j = 1
        for size in sizes:
            plt.subplot(1, 3, j)
            plt.title('n = ' + str(size))
            if distr == 'Poisson':
                left_bound = 6
                right_bound = 14
            else:
                left_bound = -4
                right_bound = 4
            
            x = clump(generatorRandomArray(distr, size), left_bound, right_bound)
            x_true = np.linspace(left_bound, right_bound, 1000)
            plt.plot(x_true, generatorDistrFunc(distr, x_true))
            plt.hist(x, len(x), density=True, histtype='step',
                           cumulative=True, label='Empirical', range=(left_bound, right_bound))
            plt.xlabel('x')
            plt.ylabel('F(x)')
            j += 1
        
        #plt.show()
        plt.savefig(distr + '.png', format='png')

        
        for size in sizes:
            plt.figure(figsize=(10, 4))
            plt.subplots_adjust(wspace=0.5)
            if distr == 'Poisson':
                left_bound = 6
                right_bound = 14
            else:
                left_bound = -4
                right_bound = 4
            
            x = clump(generatorRandomArray(distr, size), left_bound, right_bound)

            kde = stats.gaussian_kde(x, bw_method='silverman')

            xs = np.linspace(left_bound, right_bound, num=1000)
            y1 = kde(xs)
            kde.set_bandwidth(bw_method=kde.factor / 2.)
            y2 = kde(xs)
            kde.set_bandwidth(bw_method=kde.factor * 4.)
            y3 = kde(xs)

            x_true = np.linspace(left_bound, right_bound, 1000)

            plt.subplot(1, 3, 1)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.plot(xs, y2, label='0.5')
            plt.plot(x_true, generatorDensity(distr, x_true))
            plt.subplot(1, 3, 2)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.plot(xs, y1, label='1')
            plt.plot(x_true, generatorDensity(distr, x_true))
            plt.subplot(1, 3, 3)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.plot(xs, y3, label='2')
            plt.plot(x_true, generatorDensity(distr, x_true))

            


            plt.savefig(distr + 'kernel' + str(size) + '.png', format='png')



            

