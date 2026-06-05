import numpy as np
import matplotlib.pyplot as plt
import argparse

plt.rcParams["font.size"] = 14


# ---- vectorized functions
def mc_integration(rng, N):
    x = rng.random(N)
    return np.mean(np.sqrt(1 - x**2))


def area_method(rng, N):
    points = rng.random((N, 2))
    inside = (points[:, 0] ** 2 + points[:, 1] ** 2) < 1
    return np.mean(inside)


# --- generate histogram of M measurements with N samples
def generate_histograms(N, M):
    mc_vals = np.array([mc_integration(np.random.default_rng(), N) for _ in range(M)])
    area_vals = np.array([area_method(np.random.default_rng(), N) for _ in range(M)])

    np.savetxt("histo_mc_data.txt", mc_vals)
    np.savetxt("histo_area_data.txt", area_vals)


# ---- plot histograms
def plot_histogram(filename, label, outfile):
    data = np.loadtxt(filename)

    print(f"{label}")
    print(f"Mean = {np.mean(data)}")
    print(f"Variance = {np.var(data)}\n")

    plt.figure()
    plt.hist(data, bins=10, edgecolor="black")
    plt.title(label)
    plt.xlabel("Estimate")
    plt.ylabel("Counts")
    #plt.tight_layout()

    plt.savefig(outfile)

    #plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Area method and mc estimator histograms for (N,M) measurements"
    )

    parser.add_argument("--N", type=int, default=10000, help="Number of samples")
    parser.add_argument("--M", type=int, default=1000, help="Number of experiments")

    args = parser.parse_args()

    print("\nExact value (pi/4) =", np.pi / 4, "\n")

    generate_histograms(args.N, args.M)

    plot_histogram("histo_mc_data.txt", "MC histogram", "histo_mc.pdf")
    plot_histogram("histo_area_data.txt", "Area histogram", "histo_area.pdf")
