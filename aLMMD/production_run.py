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
import MDAnalysis as mda
from MDAnalysis.analysis import dihedrals
from MDAnalysis.coordinates import PDB

import mdtraj as md

import matplotlib
import matplotlib.pyplot as plt

from IPython.display import clear_output, display

from pathlib import Path

#======================================================
# USER PARAMETERS
#======================================================
print('defining user parameters')
# Add a unique identifier for this simulation run
run_id = "4MZI_100ps_checkpoint_testing_A"   # <-- you control this manually

# Timestamp for metadata and gromacs runs
timestamp = datetime.now().strftime("%Y%m%d")



# For safety, provide a pdb file with waters removed and polar hydrogens added. No need to add Kollman charges.
protein_pdb = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project/4MZI/4MZI.pdb"
protein_pdb_path = Path(protein_pdb)
protein_fixed_pdb = str(protein_pdb_path.with_name(protein_pdb_path.stem + "_fixed" + protein_pdb_path.suffix))

probe_folder = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project/Probes"
probe_names = ["benzene.sdf", "methanol.sdf", "acetonitrile.sdf", "toluene.sdf"]

# sdf paths for load_and_save_off_molecules(sdf_paths) later
sdf_paths = [os.path.join(probe_folder, f"{name}") for name in probe_names]

# all standard protein residues
protein_resnames = ("ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY",
                    "HIS","ILE","LEU","LYS","MET","PHE","PRO","SER",
                    "THR","TRP","TYR","VAL")

# Simulation and solvation parameters
temperature = 300 * kelvin
friction = 1.0 / picosecond
pH = 7.0

# metal coordination cut off
coordination_cutoff = 0.25  # 2.5 Å in nm

# set coord residues to metal
coord_residues = ['CYS','HIS','ASP','GLU']

# metal coordination harmonic bond restraint
k_metal = 1000.0  # kJ/mol/nm^2

# Probe placement parameters for Step 4 and automatically set padding for solvation in step 3
num_copies_per_probe = 1
max_radius = 3.0 # in nm - shell thickness
min_dist = 0.3  # in nm (~2 Å)
attempts = 1000
protein_radius_buffer = 0.20     # nm outside protein surface
padding = max_radius + protein_radius_buffer + 1.0

# Solvent cutoff for step 4
probe_solvent_cutoff = 0.25  # nm

# Solvent cutoff for step 5
solvent_cutoff = 0.25  # nm

# number of slowest-moving torsions to select for step 10
num_torsions = 4

# set values for these for plumed.dat generation in step 10
E0_modifier = 0.5
alpha_modifier = 0.2
gamma_torsion_target = 8

# checkpoint interval. this number will be set in min for backup but in ps for the production run
# ie. a "30" interval for both means backups will be saved every 30min and .cpt every 30ps of simulation.
# checkpoint_interval is a string while backup_interval is an integer
checkpoint_interval = "20"
backup_interval = 20

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
        "plumed.dat", "HILLS",
        "plumed_bias_scalar.dat", "plumed_com_components.dat",
        "prod_pullx.xvg", "prod_pullf.xvg" 
    ]

    # Add any HILLS-containing files automatically
    hills_files = glob.glob(os.path.join(gmx_temp_dir, "HILLS*"))
    files_to_backup += [os.path.basename(f) for f in hills_files]
    
    with open(backup_log_file, "a") as logf:
        logf.write(f"{datetime.now().isoformat()} - Backup started: {timestamp_str}\n")

    # Copy files to temporary folder first
    for f in files_to_backup:
        src = os.path.join(gmx_temp_dir, f)
        if os.path.exists(src):
            shutil.copy(src, temp_backup_dir)

    # Rename temp folder to final timestamped folder (atomic)
    os.rename(temp_backup_dir, final_backup_dir)

    # Keep only latest 5 backups
    backups = sorted(os.listdir(backup_base))
    backups = [b for b in backups if os.path.isdir(os.path.join(backup_base, b))]
    while len(backups) > 5:
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
# STEP 12a: Production run starting
#======================================================================
print("\nSTEP 12a: Production run starting...")

# Paths
bias_and_energy_and_temp_plots_dir = os.path.join(gmx_run_dir, "bias_and_energy_and_temp_plots")
os.makedirs(bias_and_energy_and_temp_plots_dir, exist_ok=True)

md_log_file = os.path.join(gmx_temp_dir, f"prod.log")

# -------------------------
# Run production
# -------------------------
stop_backup_flag = False

def periodic_backup(interval_min=int(backup_interval)):
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

# Move outputs for prod once .tpr for production is generated
for ext in [".gro", ".trr", ".edr", ".tpr", ".log",".mdp"]:
    src = os.path.join(gmx_temp_dir, f"prod{ext}")
    dst = os.path.join(gmx_run_dir, f"prod{ext}")
    if os.path.exists(src): shutil.copy(src, dst)

print("\nProduction run complete.")
print("\nSTEP 12a complete.")
