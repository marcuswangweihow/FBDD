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
