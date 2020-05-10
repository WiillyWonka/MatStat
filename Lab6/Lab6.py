import numpy as np
import matplotlib.pyplot as plt

def MNK(X, Y):
    b1 = (np.mean(X * Y) - np.mean(X) * np.mean(Y)) / np.var(X)
    b2 = np.mean(Y) - np.mean(X) * b1

    quality = np.sum(np.abs(Y - b2 - b1 * X))

    return b1, b2, quality

def r_Q(X, Y):
    return np.sum((np.sign(X - np.mean(X)) * np.sign(Y - np.mean(Y)))) / len(X)

def q(X):
    temp = np.sort(X)

    return temp[int(len(temp) * 3 / 4)] - temp[int(len(temp) / 4)]

def MAE(X, Y):
    b1 = r_Q(X, Y) * q(Y) / q(X)
    b2 = np.median(Y) - b1 * np.median(X)

    
    quality = np.sum(np.abs(Y - b2 - b1 * X))

    return b1, b2, quality
    

if __name__ == "__main__":
    X = np.arange(-1.8, 2, 0.2)
    e = np.random.normal(0, 1, size=len(X))
    Y = 2 + 2*X + e

    a1, a2, quality1 = MNK(X, Y)

    b1, b2, quality2 = MAE(X, Y)

    print(a1, a2, quality1)
    print(b1, b2, quality2)

    plt.figure()
    plt.scatter(X, Y, label='Выборка', edgecolor='navy')
    plt.plot(X, 2 + 2*X, label='Модель', color='blue')
    plt.plot(X, a2 + a1*X, label='МHK', color='red')
    plt.plot(X, b2 + b1*X, label='МHM', color='green')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim([-2, 2])
    plt.legend()
    plt.savefig('notperturbation_lab6.png', format='png')
    #plt.show()

    Y[0] += 10
    Y[-1] -= 10

    a1, a2, quality1 = MNK(X, Y)

    b1, b2, quality2 = MAE(X, Y)

    print(a1, a2, quality1)
    print(b1, b2, quality2)

    plt.figure()
    plt.scatter(X, Y, label='Выборка', edgecolor='navy')
    plt.plot(X, 2 + 2*X, label='Модель', color='blue')
    plt.plot(X, a2 + a1*X, label='МHK', color='red')
    plt.plot(X, b2 + b1*X, label='МHM', color='green')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim([-2, 2])
    plt.legend()
    plt.savefig('perturbation_lab6.png', format='png')
    #plt.show()

