import numpy as np
import time
import argparse


# --- f(x): mc_function
def mc_function(x):
    return np.sqrt(1 - x**2)


# --- <f(x)/p(x)> : 1/N sum_{i=0}^{N} f(x)/p(x) where p(x) = 1 (see lecture notes I)
# def mc_integration(rng, N):
#    sum = 0.0
#    for i in range(N):
#        sum += mc_function(rng.random())
#    return sum / N


# --- <f(x)/p(x)>  vectorized
def mc_integration(rng, N):
    x = rng.random(N)
    return np.mean(mc_function(x))


def run_mc_integration(func, rng, N, outfile="mc_data.txt"):
    start = time.perf_counter()
    res = func(rng, N)
    elapsed = time.perf_counter() - start

    print("Monte Carlo integration")
    print(f"N = {N:<10} estimate = {res}")
    print(f"Elapsed time = {elapsed:.6f} s\n")

    # ---- append results to file mc_data.txt
    with open(outfile, "a") as f:
        f.write(f"{N} {res}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo estimator for pi/4")
    parser.add_argument("--N", type=int, default=10000)
    args = parser.parse_args()

    rng = np.random.default_rng(seed=42)

    print("Exact value (pi/4):", np.pi / 4, "\n")

    # --- run mc estimator and check elapsed time ----
    run_mc_integration(mc_integration, rng, args.N)
