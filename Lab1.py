import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

ROW_COLUMN = 310

#Normal
plt.figure("Normal")
gNumber = 1
for n in [10, 50, 1000]:
    plt.subplot(ROW_COLUMN + gNumber)
    plt.title("n = " + str(n))
    gNumber += 1
    normal_sample = stats.norm.rvs(0, 1, n)
    plt.hist(normal_sample, bins = int(math.log(n,1.2)), density = True)
    x_axis = np.arange(min(normal_sample), max(normal_sample), 0.001)
    plt.plot(x_axis, stats.norm.pdf(x_axis,0, 1))
plt.subplots_adjust(hspace=1)

#Cauchy
plt.figure("Cauchy")
gNumber = 1
for n in [10, 50, 1000]:
    plt.subplot(ROW_COLUMN + gNumber)
    plt.title("n = " + str(n))
    gNumber += 1
    normal_sample = stats.cauchy.rvs(0, 1, n)
    plt.hist(normal_sample, bins = int(math.log(n,1.2)), density = True)
    x_axis = np.arange(min(normal_sample), max(normal_sample), 0.001)
    plt.plot(x_axis, stats.cauchy.pdf(x_axis, 0, 1))
plt.subplots_adjust(hspace=1)

#Laplace
plt.figure("Laplace")
gNumber = 1
for n in [10, 50, 1000]:
    plt.subplot(ROW_COLUMN + gNumber)
    plt.title("n = " + str(n))
    gNumber += 1
    normal_sample = stats.laplace.rvs(0, 1/math.sqrt(2), n)
    plt.hist(normal_sample, bins = int(math.log(n,1.2)), density = True)
    x_axis = np.arange(min(normal_sample), max(normal_sample), 0.001)
    plt.plot(x_axis, stats.laplace.pdf(x_axis, 0, 1/math.sqrt(2)))
plt.subplots_adjust(hspace=1)

def poisson_aprox(k):
    return (10**k)/math.gamma(k + 1)*math.exp(-10)

#Poisson
plt.figure("Poisson")
gNumber = 1
for n in [10, 50, 1000]:
    plt.subplot(ROW_COLUMN + gNumber)
    plt.title("n = " + str(n))
    gNumber += 1
    normal_sample = stats.poisson.rvs(10, size = n)
    plt.hist(normal_sample, bins = int(math.log(n,1.5)), density = True)
    x_axis = np.arange(min(normal_sample), max(normal_sample), 0.001)
    plt.plot(x_axis, [poisson_aprox(i) for i in x_axis])
plt.subplots_adjust(hspace=1)

#Uniform
plt.figure("Uniform")
gNumber = 1
for n in [10, 50, 1000]:
    plt.subplot(ROW_COLUMN + gNumber)
    plt.title("n = " + str(n))
    gNumber += 1
    normal_sample = stats.uniform.rvs(-math.sqrt(3), 2*math.sqrt(3), n)
    plt.hist(normal_sample, bins = int(math.log(n,1.5)), density = True)
    x_axis = np.arange(min(normal_sample), max(normal_sample), 0.001)
    plt.plot(x_axis, stats.uniform.pdf(x_axis, -math.sqrt(3), 2*math.sqrt(3)))
plt.subplots_adjust(hspace=1)

plt.show()
