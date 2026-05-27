import numpy as np
import time
import argparse


# ---- Nc/N point ratio inside quarter circle -> norm(x,y) < 1
def area_method(rng, N):
    count = 0
    for i in range(N):
        if np.linalg.norm(rng.random(2)) < 1:
            count += 1
    return count / float(N)


# ----Nc/N vectorized for repeated histogram sampling
# def area_method(rng, N):
#    points = rng.random((N, 2))
#    inside = np.linalg.norm(points, axis=1) < 1
#    return np.mean(inside)


def run_area_method(func, rng, N, outfile="area_data.txt"):
    start = time.perf_counter()
    res = func(rng, N)
    elapsed = time.perf_counter() - start

    print("Area method")
    print(f"N = {N:<10} estimate = {res}")
    print(f"Elapsed time = {elapsed:.6f} s\n")

    # ---- append data to file area_data.txt
    with open(outfile, "a") as f:
        f.write(f"{N} {res}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Area method for pi/4")
    parser.add_argument("--N", type=int, default=10000, help="number of samples")
    args = parser.parse_args()

    rng = np.random.default_rng(seed=42)
    print("Exact value (pi/4):", np.pi / 4, "\n")

    # --- run area_method and check elapsed time ----
    run_area_method(area_method, rng, args.N)
