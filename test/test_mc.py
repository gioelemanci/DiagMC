import numpy as np
import matplotlib.pyplot as plt

def estimate_pi(n_points):
    # Generate random x and y coordinates between -1 and 1
    x = np.random.uniform(-1, 1, n_points)
    y = np.random.uniform(-1, 1, n_points)
    
    # Squared distance from the center
    squared_distance = x**2 + y**2
    
    # How many points are inside the circle of radius 1?
    inside_circle = squared_distance <= 1
    
    estimated_pi = 4 * np.sum(inside_circle) / n_points
    
    # Plot the first 5000 points for visual verification
    plt.figure(figsize=(6,6))
    plt.scatter(x[inside_circle][:5000], y[inside_circle][:5000], color='blue', s=2, label='Inside')
    plt.scatter(x[~inside_circle][:5000], y[~inside_circle][:5000], color='red', s=2, label='Outside')
    plt.title(f"Estimation of pi: {estimated_pi:.5f}")
    plt.legend()
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    print("Starting Monte Carlo simulation...")
    estimate_pi(1000000)
    print("Simulation finished!")
