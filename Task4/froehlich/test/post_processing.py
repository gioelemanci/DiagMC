import numpy as np
import matplotlib
matplotlib.rcParams['font.size'] = 14
import matplotlib.pyplot as plt
import json
from scipy.optimize import curve_fit

def straight_line(x, a, b):
    return a + b * x

if __name__ == '__main__':
    file_name = "greens_function.dat"
    input_name = "input.json"

    # read input file
    with open(input_name) as f:
        input = json.load(f)
    alpha = float(input["Configuration"]["alpha"])
    mu = float(input["Configuration"]["mu"])
    max_tau = float(input["Configuration"]["max_tau"])

    # read data
    tau, gf = np.loadtxt(file_name, unpack=True)
    
    # plot Green's function
    fig, ax = plt.subplots()
    ax.plot(tau, np.log(gf), label="DiagMC")
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$log[G(\tau)]$')
    ax.set_xlim((0.0, max_tau + 0.2))
    ax.legend()
    plt.tight_layout()
    plt.savefig("fpol_gf.pdf")

    # fit to Green's function
    min_tau = 10
    idx = np.argmin(np.abs(tau - min_tau))
    popt, pcov = curve_fit(straight_line, tau[idx:], np.log(gf[idx:]), (1.0, mu))
    fit = straight_line(tau, popt[0], popt[1])

    # print results
    energy = mu - popt[1]
    zf = np.exp(popt[0])
    print()
    print("Extracted energy and quasiparticle weight:")
    print("Energy = {}".format(energy))
    print("Quasiparticle weight = {}".format(zf))
    print()

    # plot Green's function with fit
    fig, ax = plt.subplots()
    ax.plot(tau, np.log(gf), label="DiagMC")
    ax.plot(tau, fit, label='Fit')
    ax.set_xlabel(r'$\tau$')
    ax.set_ylabel(r'$log[G(\tau)]$')
    ax.set_xlim((0.0, max_tau + 0.2))
    ax.legend()
    plt.tight_layout()
    plt.savefig("fpol_gf_fit.pdf")
