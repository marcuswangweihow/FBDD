<!-- REPO_TOC -->
# FBDD Repository Structure
- [FBDD](../../../../)
  - [Frag_to_lead](../../../)
    - [9N39](../../)
      - [1ns_Preliminary Results](../)
        - [1ns_test](../1ns_test/)
          - [NPT_equil](../1ns_test/NPT_equil/)
          - [NVT_equil](../1ns_test/NVT_equil/)
          - [Production](../1ns_test/Production/)
          - [em](../1ns_test/em/)
        - [mdpocket_figures](../mdpocket_figures/)
        - [occupancy_maps](../occupancy_maps/)
        - [plumed_metad_cvs](../plumed_metad_cvs/)
        - [probe_behaviour_analysis](../probe_behaviour_analysis/)
        - [representative_snapshots](./)
          - [P01A_probespecific_snapshots](P01A_probespecific_snapshots/)
          - [P02A_probespecific_snapshots](P02A_probespecific_snapshots/)
          - [P03A_probespecific_snapshots](P03A_probespecific_snapshots/)
          - [P04A_probespecific_snapshots](P04A_probespecific_snapshots/)
          - [global_snapshots](global_snapshots/)
    - [Frag_to_lead_4MZI](../../../Frag_to_lead_4MZI/)
      - [100ps_Preliminary Results](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/)
        - [100ps_pipeline_test](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/100ps_pipeline_test/)
          - [NPT_equil](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/100ps_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/100ps_pipeline_test/NVT_equil/)
          - [Production](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/100ps_pipeline_test/Production/)
          - [em](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/100ps_pipeline_test/em/)
        - [binding_event_detection](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/mdpocket_figures/)
        - [plumed_metad_cvs](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../Frag_to_lead_4MZI/100ps_Preliminary%20Results/representative_snapshots/)
      - [100ps_run_for_checkpoint_testing](../../../Frag_to_lead_4MZI/100ps_run_for_checkpoint_testing/)
      - [1ns_Preliminary Results](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/)
        - [1ns_pipeline_test](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/1ns_pipeline_test/)
          - [NPT_equil](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/1ns_pipeline_test/Production/)
          - [em](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/mdpocket_figures/)
        - [occupancy_maps](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../Frag_to_lead_4MZI/1ns_Preliminary%20Results/representative_snapshots/)
      - [1ns_withpullres_withcheckpoints_Preliminary Results](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/)
        - [1ns_pipeline_test](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/)
          - [NPT_equil](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/Production/)
          - [em](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/mdpocket_figures/)
        - [occupancy_maps](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../Frag_to_lead_4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/representative_snapshots/)
  - [docking_4MZI_roscovitine](../../../../docking_4MZI_roscovitine/)
  - [images](../../../../images/)
<!-- /REPO_TOC -->













-----------------------------------------------------------

The results here are **preliminary** results for a 1ns production run of the pipeline for workflow functionality illustration purposes. 

Representative snapshots (PDBs) were selected from the full trajectory using:

- RMSD clustering to identify conformational regimes.

- KDE peak mapping and detection on probe positions.

- DBSCAN clustering on probe center-of-mass positions to identify rare probe-sampling regions, followed by RMSD-based prioritization of representative frames.

These snapshots are intended for downstream docking and MDpocket pocket analysis.

- For **overall fragment hotspots**, use snapshots in the **global_snapshots** folder.

- For **probe-specific hotspots**, use snapshots in the respective **probespecific** folders.

All snapshot and peak mapping information is saved in `representative_selection_summary.json`. 

For docking, each grid center coordinate is stored as `"peak"` under the relevant section:
- `global_selection` for global docking.
- Probe-specific sections for probe-specific docking.

# Docking Preparation and Execution

docking_prep.py and prepare_protein_snapshots.py are provided in this folder. 

These scripts are intended to work on Windows.

For Linux and Mac users:
Use `conda install -c conda-forge autodock-vina` and adapt docking_prep.py and prepare_protein_snapshots.py to make them work.

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






