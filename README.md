# FBDD Repository Structure

- [FBDD](./)
   - [Frag_to_lead_4MZI](Frag_to_lead_4MZI/)
     - [Preliminary Results](Frag_to_lead_4MZI/Preliminary%20Results/)
       - [binding_event_detection](Frag_to_lead_4MZI/Preliminary%20Results/binding_event_detection/)
       - [mdpocket_figures](Frag_to_lead_4MZI/Preliminary%20Results/mdpocket_figures/)
       - [plumed_metad_cvs](Frag_to_lead_4MZI/Preliminary%20Results/plumed_metad_cvs/)
       - [representative_snapshots](Frag_to_lead_4MZI/Preliminary%20Results/representative_snapshots/)
     - [1ns_Preliminary Results](Frag_to_lead_4MZI/1ns_Preliminary%20Results/)

-------------------------------------------------------------------------------

# Frag_to_lead_4MZI
This folder contains the data and results for a fragment to lead workflow with 4MZI using aLMMD (accelerated Ligand-Mapping Molecular Dynamics).

The entire workflow can be shown as:
## 🧬 Workflow Overview

![Overall workflow FBDD](images/Overall_workflow_FBDD.svg)

This is ongoing work and i am currently working on the aLMMD sampling and analysis.

---

# Preliminary Results ([Preliminary Results](Frag_to_lead_4MZI/Preliminary%20Results/))
This folder contains the preliminary/test results from the **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** pipeline such as energy, temperature and bias plots, as well as post-processing plots (eg. occupancy maps) for a 100ps production run.

# 1ns_Preliminary Results ([1ns_Preliminary Results](Frag_to_lead_4MZI/1ns_Preliminary%20Results/))
This folder contains the preliminary/test results from the **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** pipeline such as energy, temperature and bias plots, as well as post-processing plots (eg. occupancy maps) for a 1ns production run.

# aLMMD Pipeline - aLMMD Sampling / aLMMD Analysis ([Frag_to_lead_4MZI](Frag_to_lead_4MZI/))

This pipeline implements an **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** workflow with automated setup, simulation, and post‑processing.  
It produces **5 (can be set) representative snapshots** for subsequent MDpocket analysis and docking tasks.

The pipeline is inspired by the workflow described in the abstracts and supporting information of **Tan et al.** (2020, 2022).  

References:

- Tze-Yang Ng, J. and Tan, Y.S., 2022. Accelerated ligand-mapping molecular dynamics simulations for the detection of recalcitrant cryptic pockets and occluded binding sites. Journal of Chemical Theory and Computation, 18(3), pp.1969-1981. [Abstract & SI only — full text/code not accessed](https://pubs.acs.org/doi/10.1021/acs.jctc.1c01177) — referenced for dihedral boost, aMD, and general workflow concepts.
- Tan, Y.S. and Verma, C.S., 2020. Straightforward incorporation of multiple ligand types into molecular dynamics simulations for efficient binding site detection and characterization. Journal of Chemical Theory and Computation, 16(10), pp.6633-6644. [Abstract & SI only — full text/code not accessed](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.0c00405) — referenced for general workflow concepts.

## Pipeline Overview

1. **Fragment/Probe Preparation**  
    - Automatic SDF → MOL2 conversion with 3D coordinates.
    - AM1‑BCC charge assignment via Antechamber (AmberTools, WSL2).
    - Conversion of probes into OpenMM residues (full residues, explicit bonds).
    - Supports multiple probes (P01, P02, …) with per-probe residue templates. 

2. **Probe Placement**  
    - N copies of each probe placed around the protein centroid while avoiding collisions 

3. **System Solvation & Neutralization**  
   - TIP3P water model.  
   - Ionic strength / counterion neutralization as needed.

4. **Energy Minimization & Equilibration**  
   - Energy minimization → NVT → NPT equilibration.  
   - Automatic estimation of aMD boost parameters from equilibration (E₀, α).

5. **Multi‑Dihedral + Total‑Potential aMD with METAD CVs (Distances + COMs)**  
   - Automatic selection of torsions (protein backbone) for multi-dihedral boost.  
   - Total potential boost applied to system.  
   - PLUMED METAD CVs: distances and center-of-mass (COM) coordinates of probes are automatically monitored during production.  
   - `plumed.dat` is auto-generated for U‑boost style aMD integration.

6. **GPU Acceleration**  
   - Detects GPU (CUDA/OpenCL) automatically and uses it when available.  
   - CPU fallback is supported with minor adaptations.

7. **Production Run**  
   - Full accelerated MD simulation using PLUMED.  
   - Plotting of PLUMED bias, total energy, and temperature after run.

8. **Post‑processing**  
   - **Protein analysis**: C‑alpha radius of gyration (Rg) across trajectory.  
   - **Probe occupancy mapping**: Per-probe and combined density (voxel) maps.  
   - **Representative snapshot selection**: RMSD clustering, KDE peak mapping, and DBSCAN probe clustering to select representative snapshots.
   - **PLUMED METAD CVs**: Probe distances and torsions are extracted, smoothed, saved as CSV, and plotted for analysis.
       - **COM Analysis**: Generate single COM overview plot for all probes.
       - Additional visualizations:
         - Per-probe x/y/z COM plots.
         - Combined per-axis plots (x-only, y-only, z-only).
         - 2D projections (x-y, x-z, y-z) for probe COMs.
         - 3D scatter plot of COMs.
         - Pairwise COM distance time series.
         - 3D scatter plots of probe COM clusters.
             - Clusters colored based on assignment (e.g., density peak vs pocket).
             - Noise points plotted in grey.
             - Legend placed outside axes for clarity.
          - **Enhanced JSON**: JSON summary of clusters and top MDpocket peaks. Includes cluster info, binding events, top MDpocket peaks per cluster.
          - **Binding events CSV/JSON**: flattened per-probe events for inspection. Includes representative frame PDBs.
   - **MDpocket analysis** is run on representative snapshots.

9. **Output Organization**  
   - Simulation outputs (`.gro`, `.trr`, `.edr`, `.tpr`, `.log`) are stored in `gmx_run_dir`.  
   - Subdirectories in gmx_run_dir/ for:  
     - `bias_and_energy_and_temp_plots/` → energy, temperature, bias plots
   - Subdirectories in gmx_run_dir/post_processing/ for:  
     - `rg/` → plots of C‑alpha radius of gyration (Rg) across trajectory 
     - `windows/` → .dx and .pdb files per window
     - `full_trajectory/` → .dx and .pdb files for the full trajectory
     - `full_trajectory/representative_snapshots` → .pdb files for the representative snapshots
     - `full_trajectory/representative_snapshots/cleaned_protein_pdbs` →  cleaned protein only .pdb files for the representative snapshots for downstream MDpocket analysis and docking tasks
     - `mdpocket_analysis` → to store the MDpocket analysis results from the manual run of mdpocket outside the notebook
     - `cv_plots/` → plots for PLUMED METAD CVs and COM Analysis, and binding events CSV/JSON  

 ## Force Fields

    - **Protein**: AMBER ff14SB, via `amber14-all.xml` (includes ff14SB).  
    - **Water**: TIP3P, standard model from Amber `amber14` force field.  
    - **Small molecules / Probes (GAFF)**:  
      - GAFF version 2.11, via `GAFFTemplateGenerator` (OpenMM-compatible).    

---

> **Note:** This pipeline has potential for publication similar to the 2020 and 2022 papers by Tan et al.  
> The full code is **not publicly released on GitHub**, but is **available upon request** to technical interviewers or collaborators for evaluation purposes.
> If you require access, please contact me via the email provided in my application/CV.
> More details on the pipeline can be found in the Frag_to_lead_4MZI folder's README.

# prepare_ligands.ipynb
This notebook contains a script to prepare ligands automatically for docking in AutoDock Vina.

Main software and dependencies used:
- Windows 11
- MGLTools-1.5.7 (AutoDock Tools)
- Autodock Vina v1.2.7 (from https://github.com/ccsb-scripps/AutoDock-Vina/releases)
- OpenBabel 3.1.1

The script requires a folder containing all ligand files in .sdf format and outputs all ligands in .pdbqt format in a separate folder with numbering.

During the ligand preparation, the following operations are performed.
 - Add all hydrogens
 - Assign Gasteiger charges
 - non-polar hydrogens are merged
 - Count rotatable bonds

Note that for receptors, an automated script is not provided because of the need to assign Kollman charges.

During receptor preparation, the following operations are performed within AutoDock Tools before saving the receptor as a .pdbqt file.
 - Delete water 
 - Add polar hydrogens
 - Add Kollman charges

# docking.py
By default, the parameters for:
- num_modes = 9
- exhaustiveness = 8
- energy_range = 4

are set in the config.txt file.

The script takes each ligand prepared using prepare_ligands.ipynb and docks it with the specified receptor using AutoDock Vina.

Each docked ligand is saved as a .pdbqt file and the log file for the entire process is saved as docking_log.txt

# FBDD.ipyb
This notebook contains three functions

 - get_descriptors
   
   This function takes a list of molecules as input and calculates the molecular descriptors for each molecule in the list.
   
   The resulting list can be easily saved to a dataframe for input into the model function
   
 - train_fragment_nn_model
   
   This function takes a dataframe and trains it using a neural network model.
   The output is a model and the test data as tensors

 - train_fragment_rf_model
   
   This function takes a dataframe and trains it using a random forest model.
   The output is a model and the test data as tensors
   
 - evaluate_model
   
   This function takes a model and test tensor data as input.
   The output is a dictionary of metrics.


# def mol_to_frags(mol_list)
This function takes in a list of molecules as input and decomposes them into fragments using BRICS.

The resulting list of fragments can be converted into a dataframe and fed into the function for calculating molecular descriptors.

# Docking_4MZI_roscovitine
This folder contains the .pdbqt files for 4MZI - Crystal structure of a human mutant p53 and Roscovitine as the ligand.

The .pdbqt file containing the 9 poses of the docked ligand is also included. 

The log.txt file and the config.txt file for this docking project is included in this folder.



