import scipy.stats as stats
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def quadrant(X, Y):
    x_mean = np.mean(X)
    y_mean = np.mean(Y)
    n1 = ((X - x_mean > 0) * (Y - y_mean > 0)).sum()
    n2 = ((X - x_mean < 0) * (Y - y_mean > 0)).sum()
    n3 = ((X - x_mean < 0) * (Y - y_mean < 0)).sum()
    n4 = ((X - x_mean > 0) * (Y - y_mean < 0)).sum()

    return ((n1 + n3) - (n2 + n4)) / len(X)

def create_table(pearson_array, spearman_array, quadrant_array, mode, mode_array):
    rows = []
    headers = []

    pearson_mean = np.mean(pearson_array, axis=1)
    spearman_mean = np.mean(spearman_array, axis=1)
    quadrant_mean = np.mean(quadrant_array, axis=1)

    pearson_mean_sq = np.mean(pearson_array ** 2, axis=1)
    spearman_mean_sq = np.mean(spearman_array ** 2, axis=1)
    quadrant_mean_sq = np.mean(quadrant_array ** 2, axis=1)

    pearson_variance = pearson_mean_sq - pearson_mean ** 2
    spearman_variance = spearman_mean_sq - spearman_mean ** 2
    quadrant_variance = quadrant_mean_sq - quadrant_mean ** 2

    for i in range(len(pearson_array)):
        rows.append([mode + "= " + str(mode_array[i]), 'r', '$r_S$', '$r_Q$'])

        rows.append(['$E(z)$', np.around(pearson_mean[i], decimals=5), np.around(spearman_mean[i], decimals=5), np.around(quadrant_mean[i], decimals=5)])

        rows.append(['$E(z^2)$', np.around(pearson_mean_sq[i], decimals=5), np.around(spearman_mean_sq[i], decimals=5), np.around(quadrant_mean_sq[i], decimals=5)])

        rows.append(['$D(z)$', np.around(pearson_variance[i], decimals=5), np.around(spearman_variance[i], decimals=5), np.around(quadrant_variance[i], decimals=5)])

    print(tabulate(rows, headers, tablefmt="latex_raw"))

def draw_confidence_ellipse(x, y, ax, n_std=3.0):
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, facecolor='none', edgecolor='navy')
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)

    ax.scatter(x, y, s=3)


if __name__ == "__main__":
    sizes = [20, 60, 100]
    r = [0.1, 0.5, 0.9]

    mean = [0.0, 0.0]

    for size in sizes:
        fig, ax = plt.subplots(1, 3, figsize=(10, 4))
        fig.subplots_adjust(wspace=0.5)

        pearson_array = np.zeros((3, 1000))
        spearman_array = np.zeros((3, 1000))
        quadrant_array = np.zeros((3, 1000))

        for i in range(3):
            ax[i].set_title(r'$ \rho = $' + str(r[i]))
            cov = [[1, r[i]], [r[i], 1]]
            for j in range(1000):
                buf = stats.multivariate_normal.rvs(mean, cov, size)
                x = buf[:,0]
                y = buf[:,1]
                pearson_array[i, j], _ = stats.pearsonr(x, y)
                spearman_array[i, j], _ = stats.spearmanr(x, y)
                quadrant_array[i, j] = quadrant(x, y)

            draw_confidence_ellipse(x, y, ax[i])

        fig.savefig('n=' + str(size))
        
        print('n = ' + str(size))
        create_table(pearson_array, spearman_array, quadrant_array, '$\\rho$', r)


    pearson_array = np.zeros((3, 1000))
    spearman_array = np.zeros((3, 1000))
    qadnrant_array = np.zeros((3, 1000))

    cov1 = [[1, 0.9], [0.9, 1]]
    cov2 = [[10, -0.9], [-0.9, 10]]

    for i in range(len(sizes)):
        for j in range(1000):
            buf = 0.9 * stats.multivariate_normal.rvs(mean, cov1, sizes[i]) + 0.1 * stats.multivariate_normal.rvs(mean, cov2, sizes[i])
            x = buf[:,0]
            y = buf[:,1]
            pearson_array[i, j], _ = stats.pearsonr(x, y)
            spearman_array[i, j], _ = stats.spearmanr(x, y)
            quadrant_array[i, j] = quadrant(x, y)

    create_table(pearson_array, spearman_array, quadrant_array, 'n', sizes)

    #plt.show()
