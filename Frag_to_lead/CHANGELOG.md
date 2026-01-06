# Changelog

All notable changes to this project are documented in this file. Versions prior to 0.3 are not tracked. Date is in format YYYY-MM-DD.

**Note:** Versions prior to 0.3 (working and reproducible workflow for small proteins with single metals - currently only 4MZI tested) have been backed up to a private GitHub repository

## [v0.3.3] - 2025-1-5
### Added
- Uploaded C-alpha radius of gyration (Rg) plots for the 1ns production run of 9N39 to GitHub
- Uploaded most KDE occupancy map images to GitHub. Only combined_full still in progress of generating from PyMOL.
- Extended C-alpha Rg analysis to support both single-trajectory inspection and ensemble-level interpretation across multiple runs
- Added multi-run handling for KDE-based probe occupancy map generation
- Optimized KDE occupancy map code for improved efficiency and scalability

### Changed
- 9N39 folder on GitHub updated to for upcoming post-processing results

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
    
