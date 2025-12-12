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
#=======================================================
# Resume production run from backup
#=======================================================
# Set run_id for backup folder. must match existing backup folder
run_id = "4MZI_1ns_pullres_testing_C"

# Timestamp for for backup folder. must match existing backup folder
timestamp = '20251211'
backup_time = '2026'

# set tolerance to truncate hills last step
tolerance = 1e-6

base_dir = "/mnt/c/Users/Admin/Documents/Documents/Misc/FBDD project"
run_dir = os.path.join(base_dir, f"{run_id}_{timestamp}")
gmx_run_dir = os.path.join(run_dir, "gmx_run")
gmx_temp_dir = os.path.join(run_dir, "gmx_temp")
backup_base = os.path.join(run_dir, "backup")


# Choose backup folder to use
backup_to_use = os.path.join(backup_base, f"{timestamp}_{backup_time}")

# checkpoint interval. this number will be set in min for backup but in ps for the production run
# ie. a "30" interval for both means backups will be saved every 30min and .cpt every 30ps of simulation.
# checkpoint_interval is a string while backup_interval is an integer
checkpoint_interval = "30"
backup_interval = 30

gmx_bin = "/home/marcuswangweihow/miniforge3/envs/almmd/bin.AVX2_256/gmx" # Gromacs 2025.3 with plumed compatibility
os.environ["PLUMED_KERNEL"] = "/home/marcuswangweihow/opt/plumed-2.10/lib/libplumedKernel.so" # currently uses plumed 2.10 from external build as conda forge only has 2.9.2
os.environ["PATH"] = "/home/marcuswangweihow/opt/plumed-2.10/bin:" + os.environ.get("PATH", "")
#=======================================================
# Functions
#=======================================================
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

def get_checkpoint_time(cpt_file, gmx_bin="gmx"):
    """Return last simulation time (ps) from a GROMACS checkpoint (WSL-safe)."""
    proc = subprocess.run([gmx_bin, "check", "-f", cpt_file],
                          capture_output=True, text=True)
    output = proc.stdout + proc.stderr  # capture both stdout and stderr
    # Debug print to see what Python sees
    print("GROMACS check output:\n", output)

    # Match "Last frame   -1 time  864.700" (any number of spaces)
    match = re.search(r"Last frame\s+-?\d+\s+time\s+([\d\.]+)", output)
    print(match)
    if match:
        last_time_ps = float(match.group(1))
        return last_time_ps
    else:
        raise RuntimeError(f"Could not parse time from checkpoint:\n{output}")



def truncate_hills(hills_file, last_time_ps):
    """
    Truncate a HILLS file by scanning from the end backwards,
    keeping all lines up to the last line whose time <= last_time_ps.
    Preserves all comment and malformed lines.
    """
    with open(hills_file, 'r') as f:
        lines = f.readlines()

    # Find index of last valid entry <= last_time_ps
    last_valid_idx = None
    for i in reversed(range(len(lines))):
        stripped = lines[i].strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        try:
            time_ps = float(stripped.split()[0])
            if time_ps <= last_time_ps:
                last_valid_idx = i
                break
        except Exception:
            continue  # malformed line, skip

    if last_valid_idx is None:
        raise RuntimeError(f"No valid HILLS entries <= {last_time_ps} ps found.")

    # Keep all lines up to last valid entry
    truncated_lines = lines[:last_valid_idx+1]

    with open(hills_file, 'w') as f:
        f.writelines(truncated_lines)

    print(f"HILLS truncated at line {last_valid_idx} with time <= {last_time_ps} ps")

def clean_hills_fields(hills_file):
    """
    Scan a HILLS file and remove numeric prefixes before `#! FIELDS` lines.
    
    Examples of transformation:
        '      7.000000332482159                      0 #! FIELDS time t1 sigma_t1 height biasf'
        -> '#! FIELDS time t1 sigma_t1 height biasf'
    """
    with open(hills_file, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if '#! FIELDS' in stripped:
            # Find index of '#! FIELDS' in line
            idx = line.find('#! FIELDS')
            # Keep only from '#! FIELDS' onwards
            cleaned_lines.append(line[idx:].rstrip() + '\n')
        else:
            # Leave other lines unchanged
            cleaned_lines.append(line)
    
    # Overwrite the original file
    with open(hills_file, 'w') as f:
        f.writelines(cleaned_lines)
    
    print(f"HILLS file cleaned: numeric prefixes before '#! FIELDS' removed.")

def get_last_step_from_log(log_file):
    last_step = None
    last_time = None
    with open(log_file) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "Step" in line and "Time" in line:
            # Next non-empty line should contain step and time
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                parts = lines[j].split()
                try:
                    last_step = int(parts[0])
                    last_time = float(parts[1])
                except (ValueError, IndexError):
                    continue
    if last_step is None:
        raise RuntimeError("No valid step found in log file")
    return last_step, last_time

def truncate_log(log_file, last_time_ps):
    print(f'\nTruncating log...')
    truncated = []
    lines = open(log_file, 'r').readlines()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        truncated.append(line)

        # detect beginning of a step block:
        if "Step" in line and "Time" in line:
            if i+1 < n:
                # next line should contain step and time
                parts = lines[i+1].split()
                try:
                    step_time = float(parts[1])
                except:
                    i += 1
                    continue

                if step_time > last_time_ps:
                    # remove this header because it starts a block we cannot keep
                    truncated.pop()
                    break

        i += 1

    with open(log_file, 'w') as f:
        f.writelines(truncated)

    print("Log truncation OK.")

def truncate_trr(trr_file, tpr_file, last_time_ps, gmx_bin="gmx"):
    """Use gmx trjconv to truncate trajectory up to last_time_ps."""
    print(f'\nTruncating trr...')
    temp_trr = tempfile.NamedTemporaryFile(delete=False, suffix=".trr").name
    cmd = [gmx_bin, "trjconv", "-f", trr_file, "-s", tpr_file, "-o", temp_trr,
           "-b", "0", "-e", str(last_time_ps)]
    proc = subprocess.run(cmd, input=b'System\n', capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"trjconv failed: {proc.stderr.decode()}")
    shutil.move(temp_trr, trr_file)
    print(f"TRR truncated to time <= {last_time_ps} ps")


def truncate_pull(pull_file, last_time_ps):
    """
    Truncate a GROMACS pullx/pullf .xvg file so that only rows with 
    time <= last_time_ps are kept.
    Preserves all header/comment lines beginning with '@' or '#'.
    """
    if not os.path.exists(pull_file):
        print(f"Pull file not found, skipping: {pull_file}")
        return

    with open(pull_file, "r") as f:
        lines = f.readlines()

    # Find last valid data row
    last_valid_idx = None

    for i in reversed(range(len(lines))):
        line = lines[i].strip()

        # Skip headers/comments/blank lines
        if (not line) or line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        try:
            time_ps = float(parts[0])
        except Exception:
            continue  # malformed row

        if time_ps <= last_time_ps + 1e-9:
            last_valid_idx = i
            break

    if last_valid_idx is None:
        raise RuntimeError(
            f"No valid pull entries <= {last_time_ps} ps found in {pull_file}"
        )

    # Keep all headers + data lines up to last_valid_idx
    truncated = lines[: last_valid_idx + 1]

    with open(pull_file, "w") as f:
        f.writelines(truncated)

    print(f"Truncated {os.path.basename(pull_file)} at line {last_valid_idx} (<= {last_time_ps} ps)")

#=======================================================
# Setting up files from backup folder
#=======================================================

# Remove old prod files in gmx_temp_dir
print(f"\nRemoving old files in {gmx_temp_dir}")

files_in_backup = [
    "prod.tpr", "prod.trr", "prod.edr", "prod.log", "prod.cpt", 
    "plumed.dat",
    "plumed_bias_scalar.dat", "plumed_com_components.dat",
    "prod_pullx.xvg", "prod_pullf.xvg" 
]

# Add any HILLS-containing files automatically
hills_files = glob.glob(os.path.join(backup_to_use, "HILLS*"))
files_in_backup += [os.path.basename(f) for f in hills_files]

for f in files_in_backup:
    path = os.path.join(gmx_temp_dir, f)
    if os.path.exists(path):
        print(f"Removing old file {path}")
        os.remove(path)

# Copy backup files
print(f"\nCopying files from {backup_to_use} to {gmx_temp_dir}")
for f in os.listdir(backup_to_use):
    shutil.copy(os.path.join(backup_to_use, f), gmx_temp_dir)
    print(f"Copied file {f}")

print('\nAll backup files copied to gmx_temp')    
#=======================================================
# Setting up checkpoint
#=======================================================
print(f"\nSetting up last_step and last_time_ps...")

plumed_file = os.path.join(gmx_temp_dir, "plumed.dat")

checkpoint_file = os.path.join(gmx_temp_dir, "prod.cpt")
if os.path.exists(checkpoint_file):
    cpi_arg = ["-cpi", "prod.cpt"] 
else:
    sys.exit()
    
last_time_ps = get_checkpoint_time(checkpoint_file, gmx_bin=gmx_bin)

# just check if one of the pull files exists then enable pull args
pull_file = os.path.join(gmx_temp_dir, "prod_pullx.xvg")
if os.path.exists(pull_file):
    pull_arg = ["-px", "prod_pullx.xvg", "-pf", "prod_pullf.xvg"]
                
                
#=======================================================
# Truncating files
#=======================================================
print(f"\nTruncating necessary files...")

# need to get last step from log since cpt file only contains time
truncate_log(os.path.join(gmx_temp_dir, "prod.log"), last_time_ps)
last_recorded_step, last_recorded_time = get_last_step_from_log(os.path.join(gmx_temp_dir, "prod.log"))

# note that last time might not match the time for last step due to step intervals
# but gromacs will still write with the original interval.
# eg. cpt file last time is 864.700ps. log file records 864.400,864.600,864.800.
# here this will truncate to 864.600 and the simulation will continue writing from 864.800 onwards
# the truncated part does not break continuity
print(f"\nlast recorded step in files: {last_recorded_step}, last recorded time in files: {last_recorded_time} ps")
print(f"\nSimluation will continue from last saved state at: {last_time_ps} ps")

# Truncate necessary files
print(f'\nTruncating HILLS files...')
hills_files = glob.glob(os.path.join(backup_to_use, "HILLS*"))
for f in hills_files:
    path = os.path.join(gmx_temp_dir, f)
    if os.path.exists(path):
        print(f"\nTruncating HILLS file {path}")
        truncate_hills(path, last_time_ps)

truncate_trr(os.path.join(gmx_temp_dir, "prod.trr"),
             os.path.join(gmx_temp_dir, "prod.tpr"),
             last_time_ps, gmx_bin=gmx_bin)


truncate_pull(os.path.join(gmx_temp_dir, "prod_pullx.xvg"), last_time_ps)
truncate_pull(os.path.join(gmx_temp_dir, "prod_pullf.xvg"), last_time_ps)

print(f"\nAll backup files prepared for production")

#=======================================================
# Restarting prod run from checkpoint + files in backup folder
#=======================================================
print(f"\nStarting production run from backup files...")

stop_backup_flag = False

def periodic_backup(interval_min=int(backup_interval)):
    """Run periodic backups in a separate thread."""
    while not stop_backup_flag:
        backup_prod_files()
        time.sleep(interval_min*60)

# Start periodic backup thread
backup_thread = threading.Thread(target=periodic_backup, daemon=True)
backup_thread.start()

# Continue production
print(f"Continuing production run...")

subprocess.run([gmx_bin, "mdrun", "-deffnm", "prod", "-v", "-plumed", plumed_file, "-cpt", checkpoint_interval, "-append"] + pull_arg + cpi_arg,
               cwd=gmx_temp_dir, check=True)

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


print(f"\nProduction run completed")