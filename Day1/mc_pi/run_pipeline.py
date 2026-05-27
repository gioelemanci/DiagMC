import argparse
import subprocess
import sys

# 1. Setup degli argomenti da terminale
parser = argparse.ArgumentParser(description="Run the Monte Carlo lab pipeline.")
parser.add_argument("--N", type=str, required=True, help="Number of samples")
parser.add_argument("--M", type=str, required=True, help="Number of repeated measurements")
args = parser.parse_args()

# Genero il nome del file dinamicamente in base a N e M
log_filename = f"pipeline-{args.N}-{args.M}.txt"

# Funzione di supporto per stampare a schermo e scrivere nel file contemporaneamente
def log_and_print(text, file_obj):
    print(text, end="")    # Stampa sul terminale
    file_obj.write(text)   # Scrive nel file
    file_obj.flush()       # Forza il salvataggio immediato sul disco

# Apro il file in modalità scrittura ("w" sovrascrive se esiste già)
with open(log_filename, "w") as log_file:
    
    start_msg = f"=== Starting pipeline with N={args.N} and M={args.M} ===\n"
    start_msg += f"=== Output is also being saved to: {log_filename} ===\n\n"
    log_and_print(start_msg, log_file)

    # Lista dei comandi da lanciare in ordine
    commands = [
        ("Running area_method.py", f"python3 area_method.py --N {args.N}"),
        ("Running mc_estimator.py", f"python3 mc_estimator.py --N {args.N}"),
        ("Running plot.py", "python3 plot.py"),
        ("Running histogram.py", f"python3 histogram.py --N {args.N} --M {args.M}")
    ]

    # Eseguo i comandi uno dopo l'altro
    for step_name, cmd in commands:
        log_and_print(f">>> {step_name}\n", log_file)
        
        # Popen permette di catturare l'output (stdout e stderr) mentre il processo è in corso
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        
        # Leggo riga per riga l'output del codice e lo stampo/salvo
        for line in process.stdout:
            log_and_print(line, log_file)
        
        # Aspetto che il comando finisca prima di passare al prossimo
        process.wait()
        log_and_print("\n", log_file)

    log_and_print("=== All tasks completed successfully! ===\n", log_file)
