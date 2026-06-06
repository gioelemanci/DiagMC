import numpy as np
import matplotlib.pyplot as plt

# Name of the file containing the data
data_file = "graph-data.txt"

try:
    # Load data ignoring the first row
    alpha, E = np.loadtxt(data_file, skiprows=1, unpack=True)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the original data just as points ('o') without the connecting line
    ax.plot(alpha, E, marker='o', linestyle='', color='darkblue', 
            markersize=8, label='Monte Carlo Data')

    # ==========================================
    # FIT 1: Linear Fit (up to alpha = 4)
    # ==========================================
    # Create a filter (mask) to grab only the first part of the data
    mask_linear = alpha <= 4
    alpha_lin = alpha[mask_linear]
    E_lin = E[mask_linear]
    
    # Perform the fit: degree 1 means a line (y = mx + c)
    coeffs_lin = np.polyfit(alpha_lin, E_lin, deg=1)
    
    # Generate points for a smooth trendline
    alpha_lin_smooth = np.linspace(min(alpha_lin), max(alpha_lin), 50)
    E_lin_fit = np.polyval(coeffs_lin, alpha_lin_smooth)
    
    # Plot the linear fit
    ax.plot(alpha_lin_smooth, E_lin_fit, linestyle='--', color='darkorange', 
            linewidth=2.5, label='Linear Fit ($\\alpha \leq 4$)')

    # ==========================================
    # FIT 2: Parabolic Fit (from alpha = 4 onwards)
    # ==========================================
    # Create a filter for the second part of the data
    mask_parabola = alpha >= 4
    alpha_par = alpha[mask_parabola]
    E_par = E[mask_parabola]
    
    # Perform the fit: degree 2 means a parabola (y = ax^2 + bx + c)
    coeffs_par = np.polyfit(alpha_par, E_par, deg=2)
    
    # Generate points for a smooth trendline
    alpha_par_smooth = np.linspace(min(alpha_par), max(alpha_par), 50)
    E_par_fit = np.polyval(coeffs_par, alpha_par_smooth)
    
    # Plot the parabolic fit
    ax.plot(alpha_par_smooth, E_par_fit, linestyle='--', color='crimson', 
            linewidth=2.5, label='Parabolic Fit ($\\alpha \geq 4$)')

    # ==========================================
    # Customize the appearance of the plot
    # ==========================================
    ax.set_title("Ground State Energy vs Coupling with Trendlines", fontsize=14, pad=15)
    ax.set_xlabel(r"Coupling Constant $\alpha$", fontsize=12)
    ax.set_ylabel(r"Energy $E_{GS}$", fontsize=12)
    
    # Add a grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=11)

    # Show the plot
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: The file '{data_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
