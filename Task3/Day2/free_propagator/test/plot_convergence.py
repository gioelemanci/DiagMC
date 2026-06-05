import numpy as np
import matplotlib
matplotlib.rcParams["font.size"] = 14
import matplotlib.pyplot as plt
import json


def exact_solution(x, eps, mu):
    return np.exp(-(eps - mu) * x)


if __name__ == "__main__":
    file_name = "greens_function.dat"
    input_name = "input.json"

    # read input file
    with open(input_name) as f:
        input = json.load(f)
    epsilon = float(input["Configuration"]["epsilon"])
    mu = float(input["Configuration"]["mu"])
    max_tau = float(input["Configuration"]["max_tau"])

    # generate analytic result
    x = np.linspace(0, max_tau, 200)
    res = exact_solution(x, epsilon, mu)

    tau, gf = np.loadtxt(file_name, usecols=(0, 1), unpack=True)
    with open(input_name) as f:
        input = json.load(f)
    #steps = int(input["Simulation"]["max_steps"])
    steps = int(input["Simulation"]["cycles_per_check"])

    # plot convergence
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    fig, ax = plt.subplots()
    ax.plot(x, np.log(res), color="black", label="Analytic")
    ax.plot(tau, np.log(gf), color=colors[0], label="N = " + str(steps))

    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel(r"$log[G(\tau)]$")
    ax.set_xlim((-0.2, 10.2))
    ax.set_ylim(((-4.5, 0.5)))
    ax.legend()
    plt.tight_layout()
    plt.savefig("fp_convergence_" + str(steps) + ".pdf")
