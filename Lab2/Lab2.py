import scipy.stats as stats
import math

def mean(X):
    sum = 0
    for i in X:
        sum += i
    
    return sum / len(X)

def med(X):
    length = len(X)
    if length % 2:
        return X[int(length / 2)]
    else:
        return (X[int(length / 2 - 1)] + X[int(length / 2)]) / 2

def Z_R(X):
    return (X[0] + X[len(X) - 1]) / 2

def Z_Q(X):
    length = len(X)
    z1 = X[int(length / 4)]
    z2 = X[int(length * 3 / 4)]
    return (z1 + z2) / 2

def Z_tr(X):
    length = len(X)
    r = int(length / 4)
    sum = 0
    for i in range(length - r):
        sum += X[i]

    return sum / (length - 2*r)

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

    return sample

def printLatexTable(distr, n, meanList, medList, Z_RList, Z_QList, Z_trList):
    print("{distr} n = {n} & & & & &  \\\\ \hline \n \
        & $\overline x$& $med x$& $z_R $ & $z_Q $  &  $z_{{tr}}$  \\\\ \hline \n \
        $E(z)$ & {emean:.5f} & {emed:.5f} & {ez_R:.5f} & {ez_Q:.5f} & {ez_tr:.5f} \\\\ \hline \n \
        $D(z)$ & {dmean:.5f} & {dmed:.5f} & {dz_R:.5f} & {dz_Q:.5f} & {dz_tr:.5f} \\\\ \hline \n".format(
            distr=distr, n=n, emean=mean(meanList), emed=mean(medList), ez_R=mean(Z_RList), ez_Q=mean(Z_QList), ez_tr=mean(Z_trList),
            dmean=D(meanList), dmed=D(medList), dz_R=D(Z_RList), dz_Q=D(Z_QList), dz_tr=D(Z_trList)
        ))


def custom_print(value, X):
    print(value)
    print("E:" + str(mean(X)))
    print("D:" + str(D(X)))
    

if __name__ == "__main__":
    sizes = [10, 100, 1000]

    meanList = []
    medList = []
    Z_RList = []
    Z_QList = []
    Z_trList = []

    distr = "Uniform"
    print("Distribution: " + str(distr))
    for n in sizes:
        for i in range(1000):
            sample = generator(distr, n)
            sample.sort()

            meanList.append(mean(sample))
            medList.append(med(sample))
            Z_RList.append(Z_R(sample))
            Z_QList.append(Z_Q(sample))
            Z_trList.append(Z_tr(sample))
        
        
        printLatexTable(distr, n, meanList, medList, Z_RList, Z_QList, Z_trList)

        '''print("n: " + str(n))
        custom_print("Mean", meanList)
        custom_print("Med", medList)
        custom_print("Z_R", Z_RList)
        custom_print("Z_Q", Z_QList)
        custom_print("Z_tr", Z_trList)'''

