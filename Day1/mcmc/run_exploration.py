import subprocess
import re
import os

os.makedirs("out", exist_ok=True)

# =========================================================================
# CONFIGURATION BLOCK
# Uncomment the lists you want to vary. 
# WARNING: All uncommented lists MUST have the exact same length!
# =========================================================================

#n_values      = [500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000, 10000000]
#n_therm_values = [5, 10, 50, 100, 500, 1000, 5000]
#x0_values     = [1.0, 2.0, 3.0]
#sigma_values  = [1.0, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01]
#xmin_values   = [-0.5, -1, -1.5, -10.0, 0.5]
#xmax_values   = [0.5, 1, 1.5, 10.0, 1.5]
bins_values   = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000]

# =========================================================================

# 1. Collect all active (uncommented) parameters into a dictionary
active_params = {}

if 'n_values' in locals(): active_params['--N'] = n_values
if 'n_therm_values' in locals(): active_params['--N_therm'] = n_therm_values
if 'x0_values' in locals(): active_params['--x0'] = x0_values
if 'sigma_values' in locals(): active_params['--sigma'] = sigma_values
if 'xmin_values' in locals(): active_params['--x_min'] = xmin_values
if 'xmax_values' in locals(): active_params['--x_max'] = xmax_values
if 'bins_values' in locals(): active_params['--n_bins'] = bins_values

# Safety check: ensure we have at least one list and they are all the same length
if not active_params:
    print("Error: You must uncomment at least one list of parameters to test.")
    exit(1)

lengths = [len(lst) for lst in active_params.values()]
if len(set(lengths)) > 1:
    print("Error: All active (uncommented) lists must have the exact same number of elements.")
    print(f"Current lengths: {lengths}")
    exit(1)

num_iterations = lengths[0]
output_filename = "out/parameter_exploration_data.txt"

print(f"Starting parameter exploration ({num_iterations} runs). Please wait...\n")

with open(output_filename, "w") as txt_file:
    
    # 2. Build the dynamic header for the text file
    header_elements = [key.replace('--', '') for key in active_params.keys()]
    header_elements += ["Ratio_Accepted", "MSE"]
    txt_file.write("\t".join(header_elements) + "\n")
    
    # 3. Loop through the values
    for i in range(num_iterations):
        cmd_args = []
        row_output_values = []
        
        # Build the command arguments and the row string simultaneously
        for param_flag, param_list in active_params.items():
            val = param_list[i]
            cmd_args.append(f"{param_flag} {val}")
            row_output_values.append(str(val))
            
        # Join the arguments to the base command
        command = f"python3 bimodal.py " + " ".join(cmd_args)
        
        print(f"Run {i+1}/{num_iterations} -> Executing: {command}")
        
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text = result.stdout
        
        # Extract the metrics
        match_ratio = re.search(r"After sampling:\nAccepted = ([0-9.]+)", output_text)
        match_mse = re.search(r"MSE:\s*([0-9.eE+-]+)", output_text)
        
        ratio = match_ratio.group(1) if match_ratio else "Error"
        mse = match_mse.group(1) if match_mse else "Error"
        
        # Append the metrics to the row and write to file
        row_output_values += [ratio, mse]
        txt_file.write("\t".join(row_output_values) + "\n")

print(f"\nFinished! Exploration data saved in '{output_filename}'.")
