import numpy as np
import matplotlib.pyplot as plt

# Name of the file containing the data
data_file = "graph-data.txt"

try:
    # Load data ignoring the first row
    alpha, E = np.loadtxt(data_file, skiprows=1, unpack=True)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the original Monte Carlo data as scatter points
    ax.plot(alpha, E, marker='o', linestyle='', color='darkblue', 
            markersize=8, zorder=3, label='Monte Carlo Data')

    # ==========================================
    # THEORETICAL LIMIT 1: Weak Coupling
    # Formula: E = -alpha
    # ==========================================
    # Generate points for the weak coupling line (e.g., from alpha=0 to alpha=4)
    alpha_weak = np.linspace(0, 4, 50)
    
    # You can change the theoretical slope here if needed (-1.0 is the standard)
    weak_slope = -1.0 
    E_weak_theory = weak_slope * alpha_weak
    
    # Plot the theoretical line
    ax.plot(alpha_weak, E_weak_theory, linestyle='--', color='darkorange', 
            linewidth=2.5, label=f'Weak Coupling')

    # ==========================================
    # THEORETICAL LIMIT 2: Strong Coupling (Pekar Limit)
    # Formula: E = -0.108513 * alpha^2 - 2.836
    # ==========================================
    # Generate points for the strong coupling parabola (e.g., from alpha=3 to max alpha)
    # Starting a bit earlier than 4 makes the plot look more continuous
    alpha_strong = np.linspace(2, max(alpha) + 1, 50)
    
    # Standard theoretical coefficients for 3D Froehlich Polaron
    strong_coeff_a = -0.108513
    strong_coeff_c = -2.836
    E_strong_theory = (strong_coeff_a * alpha_strong**2) + strong_coeff_c
    
    # Plot the theoretical parabola
    ax.plot(alpha_strong, E_strong_theory, linestyle='--', color='crimson', 
            linewidth=2.5, label='Strong Coupling')

    # ==========================================
    # Customize the appearance of the plot
    # ==========================================
    ax.set_title("Ground State Energy vs Coupling", fontsize=14, pad=15)
    ax.set_xlabel(r"Coupling Constant $\alpha$", fontsize=12)
    ax.set_ylabel(r"Energy $E_{GS}$", fontsize=12)
    
    # Set axis limits to make it look clean (optional, adjusts automatically otherwise)
    ax.set_xlim(left=0)
    
    # Add a grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=11)

    # Show the plot
    plt.tight_layout()

    plt.savefig("energy_vs_alpha.png", dpi=300)  # Save the figure as a PNG file

    plt.show()

except FileNotFoundError:
    print(f"Error: The file '{data_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
