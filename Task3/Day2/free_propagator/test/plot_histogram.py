import numpy as np
import matplotlib
matplotlib.rcParams['font.size'] = 14
import matplotlib.pyplot as plt
import json

def exact_solution(x, eps, mu):
    return np.exp(-(eps - mu) * x)

if __name__ == '__main__':
    file_name = "greens_function.dat"
    input_name = "input.json"

    # read input file
    with open(input_name) as f:
        input = json.load(f)
    epsilon = float(input["Configuration"]["epsilon"])
    mu = float(input["Configuration"]["mu"])
    max_tau = float(input["Configuration"]["max_tau"])

    # read data file
    tau, gf = np.loadtxt(file_name, usecols=(0,1), unpack=True)

    # generate analytic result
    x = np.linspace(0, max_tau, 200)
    res = exact_solution(x, epsilon, mu)

    # plot histogram
    fig, ax = plt.subplots()
    ax.plot(x, res, color='red', label='Analytic')
    ax.bar(tau, gf, tau[2] - tau[1], alpha=0.7, edgecolor='black', label='DiagMC')
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$G(\tau)$')
    ax.legend()
    plt.tight_layout()
    plt.savefig("fp_histogram.pdf")
