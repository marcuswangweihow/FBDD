import os
import subprocess

#==================================================================
# Setup folders and paths
#==================================================================

PATH = r"C:\Users\Admin\Documents\Documents\Misc\FBDD project\4MZI - Crystal structure of a human mutant p53"
vina_executable = r"C:\Program Files\AutoDockVina\vina.exe"
ligand_dir = os.path.join(PATH, "Ligands","ligands_pdbqt")
out_dir = os.path.join(PATH, "vina_out")
log_file_path = os.path.join(out_dir, "docking_log.txt")

# Config file specifying all required parameters for docking
# Ensure all parameters are correct before running this script
config_file = os.path.join(PATH, "config.txt")

# Create output folder if it doesn't exist
os.makedirs(out_dir, exist_ok=True)

#==================================================================
# Get list of ligands to dock
#==================================================================

ligand_files = [f for f in os.listdir(ligand_dir) if f.endswith(".pdbqt")]
ligand_file_count = len(ligand_files)

print(f"Found {ligand_file_count} ligands to dock.\n")

#==================================================================
# Start docking ligands
#==================================================================

with open(log_file_path, "w") as log_file:
    for idx, ligand_file in enumerate(ligand_files, start=1):
        ligand_path = os.path.join(ligand_dir, ligand_file)
        out_path = os.path.join(out_dir, f"docked_{ligand_file}")
        
        # Build command as a list for subprocess
        # Note subprocess is used because it’s more robust for long docking runs and won’t fail because of spaces in paths 
        # unlike using os.system(cmd)
        cmd = [
            vina_executable,
            "--config", config_file,
            "--ligand", ligand_path,
            "--out", out_path
        ]
    
        # Print progress 
        if idx % 200 == 0 or idx == 1 or idx == ligand_file_count:
            message = f"[{idx}/{ligand_file_count}] Running Vina for {ligand_file} ..."
            print(message)
            log_file.write(message + "\n")
    
        # Running AutoDock Vina
        try:
            subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT, check=True)
            
        except subprocess.CalledProcessError as e:
            error_message = f"Error docking ligand {ligand_file}: {e}"
            print(error_message)
            log_file.write(error_message + "\n")


    log_file.write("All ligands docked!" + "\n")
    
print("All ligands docked!")

