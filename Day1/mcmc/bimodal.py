import numpy as np
import argparse
import matplotlib.pyplot as plt
import sys
import os

os.makedirs("out", exist_ok=True)


# ---- Custom Logger to save terminal output to a file
class OutputLogger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# ---- bimodal gaussian function
def bimodal_gauss_func(x, x0, sigma):
    return (
        1
        / (2 * np.sqrt(2 * np.pi) * sigma)
        * (
            np.exp(-((x + x0) ** 2) / (2 * sigma**2))
            + np.exp(-((x - x0) ** 2) / (2 * sigma**2))
        )
    )

# ---- sampling values from uniform distribution (UPDATED WITH RNG)
def unif(rng, x_min, x_max):
    return rng.uniform(low=x_min, high=x_max)

# ---- plot bimodal gaussian function
def plot_bimodal_gaussian(ax, x0, sigma, x_min, x_max, n_points=1000):
    """
    Plot the analytic bimodal Gaussian PDF and highlight
    the integration region.
    """
    x = np.linspace(x_min, x_max, n_points)
    y = bimodal_gauss_func(x, x0, sigma)
    ax.plot(x, y, color="darkred", linestyle="--", linewidth=2.5, label="Analytic PDF")

    ax.set_xlabel("x")
    ax.set_ylabel("Probability Density")
    return ax

# ---- UPDATED HISTO FUNCTION (Calculates MSE inside)
def plot_bimodal_gaussian_histo(ax, x, xmin, xmax, x0, sigma, n_bins):
    # ---- bin data for histogram and normalize for pdf
    hist, bin_edges = np.histogram(x, n_bins, (xmin, xmax))
    widths = np.diff(bin_edges)
    hist = hist / widths / len(x) # using len(x) instead of n_samples directly for safety
    bins = bin_edges[:-1] + widths * 0.5

    # ---- analytic function computed at bin centers
    pdf = bimodal_gauss_func(bins, x0, sigma)
    
    # ---- get MSE histo and analytic func
    mse = np.mean((hist - pdf) ** 2)

    # ---- bar plot
    ax.bar(bins, hist, widths, color="orange",
           #edgecolor="black", 
           alpha=0.6, label=f"Histo (MSE={mse:.3e})")
    return ax, hist, mse

# ---- perform MCMC sampling (UPDATED WITH RNG)
def mcmc(func, x0, sigma, xmin, xmax, nsam, ntherm, rng):
    print("Starting MCMC...")
    samples = np.zeros(nsam)
    acc = 0
    rej = 0
    curr = unif(rng, xmin, xmax)
    for i in np.arange(ntherm):
        prop = unif(rng, xmin, xmax)
        ratio = func(prop, x0, sigma) / func(curr, x0, sigma)
        if ratio < rng.random():
            rej = rej + 1
        else:
            acc = acc + 1
            curr = prop
    print("After equilibration:")
    print("Accepted = {:.3f}".format(float(acc) / ntherm))
    print("Rejected = {:.3f}".format(float(rej) / ntherm))
    acc = 0
    rej = 0
    for i in np.arange(nsam):
        prop = unif(rng, xmin, xmax)
        ratio = func(prop, x0, sigma) / func(curr, x0, sigma)
        if ratio < rng.random():
            rej = rej + 1
        else:
            acc = acc + 1
            curr = prop
        samples[i] = curr
    print("After sampling:")
    print("Accepted = {:.3f}".format(float(acc) / nsam))
    print("Rejected = {:.3f}".format(float(rej) / nsam))
    return samples, acc, rej

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulation of bimodal gaussian using MCMC."
    )
    parser.add_argument("--x0", type=float, help="Center of gaussian", default=1)
    parser.add_argument("--sigma", type=float, help="Std of gaussian", default=0.25)
    parser.add_argument(
        "--x_max", type=float, help="Maximum x to be sampled", default=2
    )
    parser.add_argument(
        "--x_min", type=float, help="Minimum x to be sampled", default=-2
    )
    parser.add_argument(
        "--N", type=int, help="Number of samples in the simulation", default=1000000
    )
    parser.add_argument(
        "--N_therm",
        type=int,
        help="Number of samples to discard for Markov Chain thermalization",
        default=1000,
    )
    parser.add_argument(
        "--n_bins",
        type=int,
        help="Number of bins for the histogram of the sampled distribution",
        default=100,
    )

    args = parser.parse_args()

    # ---- variable renaming
    x0 = args.x0
    sigma = args.sigma
    xmin = args.x_min
    xmax = args.x_max
    n_samples = args.N
    n_therm = args.N_therm
    n_bins = args.n_bins

    # Generate a descriptive filename for the text output including all input values
    log_filename = f"out/mcmc_log_N{n_samples}_Ntherm{n_therm}_x0{x0}_sig{sigma}_xmin{xmin}_xmax{xmax}_bins{n_bins}.txt"
    sys.stdout = OutputLogger(log_filename)

    # ---- Output of simulation parameters (x0, sigma...)
    print()
    print("MCMC: f(x) = 1/2 N(x0, sigma) + 1/2 N(-x0, sigma)")
    print("x0= {:.1f}".format(x0))
    print("sigma= {:.1f}".format(sigma))
    print("domain [{:.1f},{:.1f}]".format(xmin, xmax))
    print("Number of bins = {}".format(n_bins))
    print("Number of MC samples = {}".format(n_samples))
    print("Number of thermalization samples = {}".format(n_therm))
    print()

    # ---- Seeded rng for reproducibility
    rng = np.random.default_rng(seed=42)

    # ---- Markov Chain Monte Carlo (Now passes rng)
    x, acc, rej = mcmc(bimodal_gauss_func, x0, sigma, xmin, xmax, n_samples, n_therm, rng)

    # ---- plot histogram and analytic bimodal gaussian
    fig, ax = plt.subplots()
    ax, hist, mse = plot_bimodal_gaussian_histo(ax, x, xmin, xmax, x0, sigma, n_bins)
    ax = plot_bimodal_gaussian(ax, x0, sigma, xmin, xmax)

    print(f"MSE: {mse:.6e}")

    plt.title(f"Histogram and Bimodal Gaussian (N={n_samples})")
    ax.grid(True)
    ax.legend()

    # --- SAVE PLOT AUTOMATICALLY ---
    plot_filename = f"out/mcmc_plot_N{n_samples}_Ntherm{n_therm}_x0{x0}_sig{sigma}_xmin{xmin}_xmax{xmax}_bins{n_bins}.png"
    plt.savefig(plot_filename, dpi=500, bbox_inches='tight')
    print(f"Plot saved successfully as '{plot_filename}'")
    plt.close(fig)
