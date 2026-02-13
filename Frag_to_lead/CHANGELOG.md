# Changelog

All notable changes to this project are documented in this file. Versions prior to 0.3 are not tracked. Date is in format YYYY-MM-DD.

**Note:** Versions prior to 0.3 (working and reproducible workflow for small proteins with single metals - currently only 4MZI tested) have been backed up to a private GitHub repository

## [v0.3.9] - 2026-2-13
### Added
 - Automated generation of production and checkpoint-resume execution scripts, reducing manual script preparation for HPC runs
 - Standardized run directory structure to encapsulate simulation inputs, execution scripts, configuration, and logs for reproducible execution across systems
 - Introduced configuration-driven execution via config.json, allowing run parameters (e.g., checkpoint intervals, paths, run identifiers) to be managed without modifying scripts
 - Added scheduler submission templates to simplify adaptation across different HPC environments while retaining flexibility in job resource configuration
 - Streamlined execution workflow so prepared runs can be transferred and submitted with minimal reconfiguration

## [v0.3.8] - 2026-2-6
### Added
 - Added RNA handling and preprocessing for system creation and solvation, including correct termini treatment for reliable simulation setup
 - Automatic detection and handling of DNA, RNA, and metals based on input PDB content
 - Automatic generation of Tleap configuration lines according to detected system components, removing manual setup adjustments

## [v0.3.7] - 2026-1-30
### Added
 - Added probe aggregation diagnostics for production runs
 - Added functionality to generate probe occupancy per cavity and combined cavity occupancy fraction with top-K visualization for single-run analyses, enabling clear interpretation of probe–cavity interactions
 - Added automated binding event detection and snapshot extraction, including per-cavity top-K ranking, supporting visualization and analysis of probe–cavity interactions over time
 - Added functionality to generate per-probe occupancy fractions across cavities with top-K visualization for multi-run analyses, enabling clear comparison of probe behavior across ensembles

### Changed
 - Shifted individual torsion bias plots to production run diagnostics for per-run clarity. Maintained generation of smoothed torsion angle vs time plots in step 13e with plots saved to torsion_plots folder.

## [v0.3.6] - 2026-1-23
### Added
- Extended cavity occupancy analysis to multiple simulation runs, enabling ensemble-level interpretation of probe–cavity interactions
- Implemented per-probe occupancy tracking in MDpocket cavities, including time spent in each cavity and fraction of simulation occupancy
- Added plotting to visualize per-cavity probe occupancy (fraction of probes in each cavity) across time, highlighting frequently visited vs unexplored cavities
- Output saved in structured JSONs, supporting reproducible analysis and easy aggregation across runs
- Multi-run support: aggregates per-run probe COMs and occupancy into ensemble cavity analyses, allowing ranking and comparison across simulations
- Uploaded probe analysis outputs to GitHub

### Changed
- Removed the previous setup with raw COM plots and binding event detection from DBSCAN clusters

## [v0.3.5] - 2026-1-16
### Added
- Selected medoid representative snapshots from protein PDBs for MDpocket, ensuring consistent cavity analysis
- Extraction of geometric cavities from freq.dx grids, computed per-cavity metrics, and assigned geometry-informed scores for initial ranking of cavities
- Mapped KDE peaks from probe sampling onto cavities to quantify which pockets are actively explored
- Added occupancy-informed ranking to prioritize druggable sites
- Distinguished KDE-supported vs exploratory cavities, providing a clearer picture of pocket druggability
- Uploaded MDpocket analysis outputs (cavity JSONs, visualization) to GitHub

### Changed
- Updated the pipeline to match incoming JSON from single- or multi-run representative snapshots, allowing seamless integration between snapshot selection and cavity detection


## [v0.3.4] - 2026-1-9
### Added
- Uploaded representative snapshots for the 1ns production run of 9N39 to GitHub
- Implemented RMSD, KDE, and DBSCAN selection strategies for multi-run representative snapshot selection.
- Added deduplication and failsafe logic to enforce max_total_frames across RMSD, KDE, and DBSCAN selections.
- For downstream docking, grid creation can now be automatically read from KDE peak coordinates, already sorted by occupancy.
- Implemented global vs probe-specific snapshot selection for both single-run and multi-run systems.
- Merged JSON summary and merged PDB folder now available for multi-run analysis.

### Changed
- Adjusted selection logic for more robust handling of single-run snapshots.
- Refined DBSCAN selection: now focuses on minor clusters and considers RMSD to the mean structure to capture rare probe arrangements.
- Updated the JSON summary structure for single runs to simplify multi-run handling.

## [v0.3.3] - 2026-1-5
### Added
- Uploaded C-alpha radius of gyration (Rg) plots for the 1ns production run of 9N39 to GitHub
- Uploaded most KDE occupancy map images to GitHub. Only combined_full still in progress of generating from PyMOL.
- Extended C-alpha Rg analysis to support both single-trajectory inspection and ensemble-level interpretation across multiple runs
- Added multi-run handling for KDE-based probe occupancy map generation
- Optimized KDE occupancy map code for improved efficiency and scalability

### Changed
- 9N39 folder on GitHub updated for upcoming post-processing results

## [v0.3.2] - 2025-12-29
### Added
- 1ns production run completion and energy/temperature/bias vs time plots for 9N39 uploaded to GitHub

### Changed
- Documentation updated to reflect input flexibility and pipeline workflow
- Installation requirements updated in Frag_to_lead Readme.md
- Multiple other parts of Frag_to_lead Readme.md updated to match the updated workflow

## [v0.3.1] - 2025-12-22
### Changed
- Pre-minimization outputs and diagnostics updated
- Improvements to generating positional restraints and pull restraints. Now supports multiple metals and automatic metal recognition

### Fixed
- Probe placement logic is now functional

## [v0.3.0] - 2025-12-21
### Added
- DNA/protein support for aLMMD probe placement
- Included metal during solvation with tleap parameterisation
- Separate handling for each component in the PDB eg. protein/DNA/metals
- tleap merge and solvation for system
- Probes now parameterized with antechamber before probe placement

### Changed
- Input PDB handling clarified (PDB/mmCIF → PyMOL → pipeline). Input pdb can come from the downloaded .cif or .pdb from the Protein Data Bank
- Substantial pipeline refactor pre-minimization to handle a larger more complex system/target as well as code and workflow optimization
- Probe placement logic has changed and is still being worked on
    
