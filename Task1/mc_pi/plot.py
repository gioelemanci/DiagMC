import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse

matplotlib.rcParams["font.size"] = 14


def load_data(filename):
    data = np.loadtxt(filename)
    data = np.atleast_2d(data)
    return data[:, 0], data[:, 1]


def plot_file(filename, label):
    N, est = load_data(filename)
    plt.plot(N, est, "o-", label=label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mc", "area", "both"], default="both")
    args = parser.parse_args()

    plt.figure()

    if args.mode in ["mc", "both"]:
        plot_file("mc_data.txt", "Monte Carlo")

    if args.mode in ["area", "both"]:
        plot_file("area_data.txt", "Area method")

    plt.axhline(np.pi / 4, color="black", linestyle="--", label="pi/4 exact")

    plt.xscale("log")
    plt.xlabel("N")
    plt.ylabel("Estimate")
    plt.legend()
    #plt.tight_layout()
    plt.savefig("convergence_area_mc.png", dpi=600)
