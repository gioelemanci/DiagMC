import numpy as np
import matplotlib
matplotlib.rcParams['font.size'] = 14
import matplotlib.pyplot as plt
import json

def exact_solution(x, eps, delta, mu):
    return np.exp(-(eps - mu + delta) * x)

if __name__ == '__main__':
    file_name = "greens_function.dat"
    input_name = "input.json"

    # read input file
    with open(input_name) as f:
        input = json.load(f)
    epsilon = float(input["Configuration"]["epsilon"])
    delta = float(input["Configuration"]["delta"])
    mu = float(input["Configuration"]["mu"])
    max_tau = float(input["Configuration"]["max_tau"])

    # generate analytic result
    x = np.linspace(0, max_tau, 200)
    res = exact_solution(x, epsilon, delta, mu)

    # read data
    tau = np.loadtxt(file_name, usecols=(0), unpack=True)
    steps = []
    
    # plot single gf
    gf = np.loadtxt(file_name, usecols=(1), unpack=True)
    with open(input_name) as f:
        input = json.load(f)
    #steps.append(input["Simulation"]["max_steps"])

    # positive for log (just for visualization for out of convergence samples)
    gf = np.absolute(gf)
    # plot single gf
    fig, ax = plt.subplots()
    ax.plot(x, np.log(res), color='black', label='Analytic')
    ax.plot(tau, np.log(gf), color='tab:red', label="positive")
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$log[G(\tau)]$')
    ax.set_xlim((-0.2, 10.2))
    ax.set_ylim((-10.0, 0.2))
    ax.legend(loc='upper right')
    #ax.set_title('N = ' + str(steps[:]))
    plt.tight_layout()
    plt.savefig("ap_test.pdf")
