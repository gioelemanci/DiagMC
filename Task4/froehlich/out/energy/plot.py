import numpy as np
import matplotlib.pyplot as plt

# Name of the file containing the data
data_file = "graph-data.txt"

try:
    # Load data ignoring the first row (the "alpha E" header)
    # np.loadtxt automatically reads columns separated by spaces or tabs
    alpha, E = np.loadtxt(data_file, skiprows=1, unpack=True)

    # Create the figure and axis for the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the data: 
    # 'o' means markers (scatter)
    # '-' means continuous line connecting the points
    # 'o-' does both simultaneously
    ax.plot(alpha, E, marker='o', linestyle='-', color='darkblue', 
            markersize=8, linewidth=2, label='Monte Carlo Data')

    # Customize the appearance of the plot
    ax.set_title("Ground State Energy vs Coupling", fontsize=14, pad=15)
    ax.set_xlabel(r"Coupling Constant $\alpha$", fontsize=12)
    ax.set_ylabel(r"Energy $E_{GS}$", fontsize=12)
    
    # Add a grid for easier reading
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add the legend
    ax.legend()

    # Show the plot on screen
    plt.tight_layout()
    plt.show()

    # If you want to save the plot automatically, uncomment the line below:
    plt.savefig("energy_vs_alpha.png", dpi=300)

except FileNotFoundError:
    print(f"Error: The file '{data_file}' was not found. Make sure the name and path are correct.")
except Exception as e:
    print(f"An error occurred while reading the data: {e}")
