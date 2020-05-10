import numpy as np
from tabulate import tabulate
import scipy.stats as stats

if __name__ == '__main__':
    size = 100
    distr = np.random.normal(0, 1, size=size)
    mu = np.mean(distr)
    sigma = np.std(distr)
    print(np.around(mu, decimals=2), ' ', np.around(sigma, decimals=2))

    alpha = 0.05
    k = 6

    limits = np.linspace(-1.01, 1.56, num=k-1)
    quantile = stats.chi2.ppf(1 - alpha, k-1)
    probability = [stats.norm.cdf(limits[0])]
    frequancy = [len(distr[distr <= limits[0]])]

    for i in range(len(limits) - 1):
        probability.append(stats.norm.cdf(limits[i + 1]) - stats.norm.cdf(limits[i]))
        frequancy.append(len(distr[(distr <= limits[i + 1]) & (distr >= limits[i])]))

    probability.append(1 - stats.norm.cdf(limits[-1]))
    frequancy.append(len(distr[distr >= limits[-1]]))

    probability = np.array(probability)
    frequancy = np.array(frequancy)

    result = ((frequancy - size * probability) ** 2) / size / probability

    headers = ["i", "limits", "n_i", "p_i", "np_i", "n_i - np_i", "\\frac{(n_i - np_i)^2}{np_i}"]
    rows = []
    for i in range(len(frequancy)):
        if i == 0:
            boarders = ['-inf', np.around(limits[0], decimals=2)]
        elif i == len(frequancy) - 1:
            boarders = [np.around(limits[-1], decimals=2), 'inf']
        else:
            boarders = [np.around(limits[i - 1], decimals=2), np.around(limits[i], decimals=2)]
        rows.append([i + 1, boarders, frequancy[i], np.around(probability[i], decimals=4), np.around(probability[i] * 100, decimals = 2),
                     np.around(frequancy[i] - size * probability[i], decimals=2), np.around(result[i], decimals=2)])
    rows.append([len(frequancy), "-", np.sum(frequancy), np.around(np.sum(probability), decimals=4),
                 np.around(np.sum(probability * size), decimals=2),
                 -np.around(np.sum(frequancy - size * probability), decimals=2),
                 np.around(np.sum(result), decimals=2)])
    print(tabulate(rows, headers, tablefmt="latex_raw"))

    print(len(frequancy))
    print('\n')
