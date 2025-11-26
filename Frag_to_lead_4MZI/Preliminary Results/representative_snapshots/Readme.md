The results here are **preliminary** results for a short 100ps production run of the pipeline for worklflow functionality illustration purposes. 

Representative snapshots: Protein-only PDBs selected from a full trajectory (100ps) using RMSD clustering, KDE peaks, and DBSCAN clustering on probe center-of-mass positions.
These snapshots are used as input for downstream docking and MDpocket pocket analysis.

# Representative Snapshot Selection

Full trajectory frames were analyzed to select representative protein conformations.

Selection criteria:

 - RMSD clustering to identify conformational regimes.

 - KDE peak detection on probe positions.

 - DBSCAN clustering to find dense probe-sampling regions.

Selected snapshots are protein-only PDBs, stripped of hydrogens.

# Docking Preparation and Execution

## 1. Inspect the Docking Prep Folder

After running the integrated docking prep script (docking_prep.py), navigate to the docking folder:

C:\Users\Admin\Documents\Documents\Misc\FBDD project\docking_prep

You should see the following files:

- `*_cleaned.pdbqt` → prepared receptor files for each representative snapshot.  
- `*_grid_*.txt` → AutoDock Vina config files (one per KDE peak per snapshot).  
- `run_all_vina.bat` → batch file containing all Vina docking commands.  
- Ligands in `pdbqt_fragment_library` → prepared ligand files (.pdbqt) ready for docking.

---

## 2. Run the Batch Docking

On Windows:

1. Open a **Command Prompt (CMD)** or **PowerShell**.  
2. Navigate to the docking folder:

```cmd
cd "C:\Users\Admin\Documents\Documents\Misc\FBDD project\docking_prep"
```

3. Execute the batch file:
```cmd
run_all_vina.bat
```






