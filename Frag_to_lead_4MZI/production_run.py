import os
import subprocess
import shlex
import sys
import shutil
import threading
import time

import random
import math
import copy
import json
import glob
import re
import tempfile

from datetime import datetime

import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import AllChem

from openbabel import pybel

from pdbfixer import PDBFixer

from openmm.app import *
from openmm import *
from openmm.unit import *
from openmm import Vec3
from openmm.app import ForceField as OpenMMForceField

from openmmforcefields.generators import GAFFTemplateGenerator

from openff.toolkit.topology import Molecule as OFFMol
from openff.toolkit.utils import get_data_file_path
from openff.toolkit.typing.engines.smirnoff import ForceField

import parmed as pmd
from parmed import unit as punit

from MDAnalysis import Universe

import mdtraj as md

import matplotlib
import matplotlib.pyplot as plt

from IPython.display import clear_output, display

from pathlib import Path

#======================================================
# USER PARAMETERS
#======================================================
# Add a unique identifier for this simulation run
run_id = "4MZI_5ns_testA"   # <-- you control this manually

# Timestamp for metadata and gromacs runs
timestamp = datetime.now().strftime("%Y%m%d")    # Ensure that the timestamp is correct and matches your run_id folder before running the job for HPC



# For safety, provide a pdb file with waters removed and polar hydrogens added. No need to add Kollman charges.
protein_pdb = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project/4MZI/4MZI.pdb"
protein_pdb_path = Path(protein_pdb)
protein_fixed_pdb = str(protein_pdb_path.with_name(protein_pdb_path.stem + "_fixed" + protein_pdb_path.suffix))

probe_folder = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project/Probes"
probe_names = ["benzene.sdf", "methanol.sdf", "acetonitrile.sdf", "toluene.sdf"]

# sdf paths for load_and_save_off_molecules(sdf_paths) later
sdf_paths = [os.path.join(probe_folder, f"{name}") for name in probe_names]



# Simulation and solvation parameters
temperature = 300 * kelvin
friction = 1.0 / picosecond
pH = 7.0

# Probe placement parameters for Step 4
num_copies_per_probe = 2
max_radius = 10.0 # in nm
min_dist = 0.2  # in nm (~2 Å)
attempts = 5000

# Solvent cutoff for step 5
solvent_cutoff = 0.25  # nm

# number of slowest-moving torsions to select for step 10
num_torsions = 4

# set values for these for plumed.dat generation in step 10
E0_modifier = 0.6
alpha_modifier = 0.3
gamma_torsion_target = 10

# How long to save checkpoint file for production run
checkpoint_interval = "30"    # in mins

# Antechamber path
full_antechamber_path = "/home/marcuswangweihow/miniforge3/envs/almmd/bin/antechamber"

# MDpocket path
mdpocket_path = "/home/marcuswangweihow/miniforge3/envs/almmd/bin/mdpocket"

# Path to forcefields
# Use the cells at the top of the notebook to find the exact path
amber14_all_path = "/home/marcuswangweihow/miniforge3/envs/almmd/lib/python3.11/site-packages/openmm/app/data/amber14-all.xml"
amber14_tip3p_path = "/home/marcuswangweihow/miniforge3/envs/almmd/lib/python3.11/site-packages/openmm/app/data/amber14/tip3p.xml"

# Set up ff_xml_paths
ff_xml_paths = [amber14_all_path, amber14_tip3p_path]


#======================================================
# OUTPUT DIRECTORIES USING RUN ID + TIMESTAMP
#======================================================

base_dir = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project"

# Root folder for this run
run_dir = os.path.join(base_dir, f"{run_id}_{timestamp}")
os.makedirs(run_dir, exist_ok=True)

# Permanent GROMACS output directory
gmx_run_dir = os.path.join(run_dir, "gmx_run")
os.makedirs(gmx_run_dir, exist_ok=True)

# Temporary working directory for gmx execution
gmx_temp_dir = os.path.join(run_dir, "gmx_temp")
os.makedirs(gmx_temp_dir, exist_ok=True)

backup_base = os.path.join(run_dir, "backup")
os.makedirs(backup_base, exist_ok=True)
backup_log_file = os.path.join(backup_base, "backup_log.txt")

def backup_prod_files():
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M")
    temp_backup_dir = tempfile.mkdtemp(dir=backup_base)  # Temporary folder inside backup_base
    final_backup_dir = os.path.join(backup_base, timestamp_str)

    files_to_backup = [
        "prod.tpr", "prod.trr", "prod.edr", "prod.log", "prod.cpt", 
        "plumed.dat", "plumed_restart.dat",
        "plumed_bias_scalar.dat", "plumed_com_components.dat"
    ]

    with open(backup_log_file, "a") as logf:
        logf.write(f"{datetime.now().isoformat()} - Backup started: {timestamp_str}\n")

    # Copy files to temporary folder first
    for f in files_to_backup:
        src = os.path.join(gmx_temp_dir, f)
        if os.path.exists(src):
            shutil.copy(src, temp_backup_dir)

    # Rename temp folder to final timestamped folder (atomic)
    os.rename(temp_backup_dir, final_backup_dir)

    # Keep only latest 3 backups
    backups = sorted(os.listdir(backup_base))
    backups = [b for b in backups if os.path.isdir(os.path.join(backup_base, b))]
    while len(backups) > 3:
        oldest = backups.pop(0)
        shutil.rmtree(os.path.join(backup_base, oldest))

    with open(backup_log_file, "a") as logf:
        logf.write(f"{datetime.now().isoformat()} - Backup completed: {final_backup_dir}\n")

    print(f"Backup completed: {final_backup_dir}")

# Save OpenFF-generated molecules per run
off_mols_save_dir = os.path.join(run_dir, "off_mols")
os.makedirs(off_mols_save_dir, exist_ok=True)

# Plumed directory (per run)
plumed_dir = os.path.join(run_dir, "plumed")
os.makedirs(plumed_dir, exist_ok=True)

plumed_input_file = os.path.join(plumed_dir, f"plumed.dat")


#======================================================================
# STEP 12: Production run starting
#======================================================================
print("\nSTEP 12: Production run starting...")

# -------------------------
# Helper functions
# -------------------------
def parse_mdp_total_steps(mdp_file):
    nsteps = None
    dt = None
    with open(mdp_file, 'r') as f:
        for line in f:
            line = line.strip()
            # skip comments and empty lines
            if not line or line.startswith(';'):
                continue
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                if key.lower() == 'nsteps':
                    nsteps = int(value)
                elif key.lower() == 'dt':
                    dt = float(value)
    return nsteps, dt

def parse_md_edr(edr_file, gmx_bin="gmx"):
    """
    Extract steps, potential energy, and temperature from a GROMACS .edr file.
    
    Parameters
    ----------
    edr_file : str
        Path to the .edr file (e.g., prod.edr)
    gmx_bin : str
        Path to gmx executable (default assumes gmx is in PATH)
    
    Returns
    -------
    steps : np.ndarray
        MD step numbers
    potential : np.ndarray
        Potential energy (kJ/mol)
    temperature : np.ndarray
        Temperature (K)
    """
    import tempfile
    import os

    # Create a temporary file to store gmx energy output
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        energy_xvg = tmp_file.name

    # Use gmx energy non-interactively: select Potential and Temperature
    # Option 10 = Potential, 11 = Temperature in 2025.3, adjust if needed
    # We'll do this via input redirection
    input_str = "10\n11\n"  # 10 = Potential, 11 = Temperature, then Enter to finish

    cmd = [gmx_bin, "energy", "-f", edr_file, "-o", energy_xvg, "-xvg", "none"]
    
    # Run gmx energy with redirected input
    subprocess.run(cmd, input=input_str.encode(), check=True)

    # Read the .xvg-style output
    data = np.loadtxt(energy_xvg)
    os.remove(energy_xvg)

    steps = data[:, 0].astype(int)
    potential = data[:, 1]
    temperature = data[:, 2]

    return steps, potential, temperature

def moving_average(x, w=5):
    """Simple moving average with window w."""
    if len(x) < w:
        return x
    return np.convolve(x, np.ones(w)/w, mode='valid')


def plot_energy(steps, energy, output_dir, total_steps, smooth_window=5):
    energy_smooth = moving_average(energy, smooth_window)
    steps_smooth = steps[(smooth_window-1)//2 : -(smooth_window//2)] if len(steps) >= smooth_window else steps

    # Save data
    np.savez(os.path.join(output_dir, "energy_data.npz"),
             steps=steps, energy=energy,
             steps_smooth=steps_smooth, energy_smooth=energy_smooth)

    plt.figure(figsize=(7,4))
    plt.plot(steps, energy, color='lightblue', lw=0.8, label='Potential Energy (instantaneous)')
    plt.plot(steps_smooth, energy_smooth, color='blue', lw=1.5, label='Potential Energy (smoothed)')
    plt.xlabel("MD step")
    plt.ylabel("Potential Energy (kJ/mol)")
    xticks = np.linspace(0, total_steps, 11, dtype=int)
    plt.xticks(xticks)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "energy.png"), dpi=300)
    plt.close()


def plot_temperature(steps, temp, output_dir, total_steps, smooth_window=5):
    temp_smooth = moving_average(temp, smooth_window)
    steps_smooth = steps[(smooth_window-1)//2 : -(smooth_window//2)] if len(steps) >= smooth_window else steps

    # Save data
    np.savez(os.path.join(output_dir, "temperature_data.npz"),
             steps=steps, temp=temp,
             steps_smooth=steps_smooth, temp_smooth=temp_smooth)

    plt.figure(figsize=(7,4))
    plt.plot(steps, temp, color='lightcoral', lw=0.8, label='Temperature (instantaneous)')
    plt.plot(steps_smooth, temp_smooth, color='red', lw=1.5, label='Temperature (smoothed)')
    plt.xlabel("MD step")
    plt.ylabel("Temperature (K)")
    xticks = np.linspace(0, total_steps, 11, dtype=int)
    plt.xticks(xticks)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "temperature.png"), dpi=300)
    plt.close()


def plot_bias(plumed_bias_file, output_dir, total_steps):
    steps_raw, bias = [], []
    with open(plumed_bias_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#!") or not line:
                continue
            parts = line.split()
            try:
                steps_raw.append(float(parts[0]))
                bias.append(float(parts[2]))  # boost_pot.bias
            except (ValueError, IndexError):
                continue

    steps_raw = np.array(steps_raw)
    bias = np.array(bias)
    if len(steps_raw) == 0:
        print(f"Warning: no bias data found in {plumed_bias_file}")
        return steps_raw, bias

    # Rescale x-axis to total MD steps
    steps = steps_raw / steps_raw[-1] * total_steps

    # Save data
    np.savez(os.path.join(output_dir, "bias_data.npz"),
             steps_raw=steps_raw, bias=bias, steps=steps)

    plt.figure(figsize=(7,4))
    plt.plot(steps, bias, color='green', lw=1.5)
    plt.xlabel("MD step")
    plt.ylabel("Bias (kJ/mol)")
    xticks = np.linspace(0, total_steps, 11, dtype=int)
    plt.xticks(xticks)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plumed_bias.png"), dpi=300)
    plt.close()

    return steps, bias


def plot_energy_temperature_dual(steps, energy, temp, output_dir, total_steps, smooth_window=5):
    energy_smooth = moving_average(energy, smooth_window)
    temp_smooth = moving_average(temp, smooth_window)
    steps_smooth = steps[(smooth_window-1)//2 : -(smooth_window//2)] if len(steps) >= smooth_window else steps

    # Save data
    np.savez(os.path.join(output_dir, "energy_temperature_dual_data.npz"),
             steps=steps, energy=energy, temp=temp,
             steps_smooth=steps_smooth, energy_smooth=energy_smooth, temp_smooth=temp_smooth)

    fig, ax1 = plt.subplots(figsize=(7,4))

    # Left y-axis: Potential energy
    ax1.set_xlabel("MD step")
    ax1.set_ylabel("Potential Energy (kJ/mol)", color='tab:blue')
    ax1.plot(steps, energy, color='lightblue', lw=0.8, label='Energy (inst.)')
    ax1.plot(steps_smooth, energy_smooth, color='blue', lw=1.5, label='Energy (smoothed)')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Right y-axis: Temperature
    ax2 = ax1.twinx()
    ax2.set_ylabel("Temperature (K)", color='tab:red')
    ax2.plot(steps, temp, color='lightcoral', lw=0.8, label='Temp (inst.)')
    ax2.plot(steps_smooth, temp_smooth, color='red', lw=1.5, label='Temp (smoothed)')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # X-axis ticks
    xticks = np.linspace(0, total_steps, 11, dtype=int)
    ax1.set_xticks(xticks)

    # Legends outside top
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "energy_temperature_dual.png"), dpi=300)
    plt.close()

# Paths
bias_and_energy_and_temp_plots_dir = os.path.join(gmx_run_dir, "bias_and_energy_and_temp_plots")
os.makedirs(bias_and_energy_and_temp_plots_dir, exist_ok=True)

md_log_file = os.path.join(gmx_temp_dir, f"prod.log")

# -------------------------
# Run production
# -------------------------
stop_backup_flag = False

def periodic_backup(interval_min=30):
    """Run periodic backups in a separate thread."""
    while not stop_backup_flag:
        backup_prod_files()
        time.sleep(interval_min*60)

# Start periodic backup thread
backup_thread = threading.Thread(target=periodic_backup, daemon=True)
backup_thread.start()

# Run GROMACS production
subprocess.run(
    [gmx_bin, "mdrun", "-deffnm", "prod", "-v", "-plumed", plumed_input_temp, "-cpt", checkpoint_interval],
    cwd=gmx_temp_dir, check=True
)

# Stop backup thread after production completes
stop_backup_flag = True
backup_thread.join()

plumed_bias_file = os.path.join(gmx_temp_dir, "plumed_bias_scalar.dat")
shutil.copy(plumed_bias_file, plumed_dir)

plumed_com_file = os.path.join(gmx_temp_dir, "plumed_com_components.dat")
shutil.copy(plumed_com_file, plumed_dir)

edr_file = os.path.join(gmx_temp_dir, f"prod.edr")
steps, energy, temp = parse_md_edr(edr_file, gmx_bin=gmx_bin)

total_steps, timestep_ps = parse_mdp_total_steps(prod_mdp_file)
print("Total steps:", total_steps)
print("Time step (ps):", timestep_ps)

plot_energy(steps, energy, bias_and_energy_and_temp_plots_dir, total_steps, smooth_window=5)
plot_temperature(steps, temp, bias_and_energy_and_temp_plots_dir, total_steps, smooth_window=5)
plot_energy_temperature_dual(steps, energy, temp, bias_and_energy_and_temp_plots_dir, total_steps, smooth_window=5)
steps_b, bias = plot_bias(plumed_bias_file, bias_and_energy_and_temp_plots_dir, total_steps)

# Move outputs for NPT equilbration once .tpr for production is generated
for ext in [".gro", ".trr", ".edr", ".tpr", ".log"]:
    src = os.path.join(gmx_temp_dir, f"prod{ext}")
    dst = os.path.join(gmx_run_dir, f"prod{ext}")
    if os.path.exists(src): shutil.copy(src, dst)

print("\nProduction run complete.")
print(f"Final plots saved in: {bias_and_energy_and_temp_plots_dir}")
print("\nSTEP 12 complete.")
