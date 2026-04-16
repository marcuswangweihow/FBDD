<!-- REPO_TOC -->
# FBDD Repository Structure
- [FBDD](../../)
  - [Docking](../../Docking/)
  - [Fragment_processing](../../Fragment_processing/)
  - [aLMMD](../)
    - [4MZI](./)
      - [100ps Results](100ps%20Results/)
        - [100ps_pipeline_test](100ps%20Results/100ps_pipeline_test/)
          - [NPT_equil](100ps%20Results/100ps_pipeline_test/NPT_equil/)
          - [NVT_equil](100ps%20Results/100ps_pipeline_test/NVT_equil/)
          - [Production](100ps%20Results/100ps_pipeline_test/Production/)
          - [em](100ps%20Results/100ps_pipeline_test/em/)
        - [binding_event_detection](100ps%20Results/binding_event_detection/)
        - [mdpocket_figures](100ps%20Results/mdpocket_figures/)
        - [plumed_metad_cvs](100ps%20Results/plumed_metad_cvs/)
        - [representative_snapshots](100ps%20Results/representative_snapshots/)
      - [100ps_run_for_checkpoint_testing](100ps_run_for_checkpoint_testing/)
      - [1ns Results](1ns%20Results/)
        - [1ns_pipeline_test](1ns%20Results/1ns_pipeline_test/)
          - [NPT_equil](1ns%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](1ns%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](1ns%20Results/1ns_pipeline_test/Production/)
          - [em](1ns%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](1ns%20Results/binding_event_detection/)
        - [mdpocket_figures](1ns%20Results/mdpocket_figures/)
        - [occupancy_maps](1ns%20Results/occupancy_maps/)
        - [plumed_metad_cvs](1ns%20Results/plumed_metad_cvs/)
        - [representative_snapshots](1ns%20Results/representative_snapshots/)
      - [1ns_withpullres_withcheckpoints Results](1ns_withpullres_withcheckpoints%20Results/)
        - [1ns_pipeline_test](1ns_withpullres_withcheckpoints%20Results/1ns_pipeline_test/)
          - [NPT_equil](1ns_withpullres_withcheckpoints%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](1ns_withpullres_withcheckpoints%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](1ns_withpullres_withcheckpoints%20Results/1ns_pipeline_test/Production/)
          - [em](1ns_withpullres_withcheckpoints%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](1ns_withpullres_withcheckpoints%20Results/binding_event_detection/)
        - [mdpocket_figures](1ns_withpullres_withcheckpoints%20Results/mdpocket_figures/)
        - [occupancy_maps](1ns_withpullres_withcheckpoints%20Results/occupancy_maps/)
        - [plumed_metad_cvs](1ns_withpullres_withcheckpoints%20Results/plumed_metad_cvs/)
        - [representative_snapshots](1ns_withpullres_withcheckpoints%20Results/representative_snapshots/)
    - [9N39](../9N39/)
      - [1ns Results](../9N39/1ns%20Results/)
        - [1ns_test](../9N39/1ns%20Results/1ns_test/)
          - [NPT_equil](../9N39/1ns%20Results/1ns_test/NPT_equil/)
          - [NVT_equil](../9N39/1ns%20Results/1ns_test/NVT_equil/)
          - [Production](../9N39/1ns%20Results/1ns_test/Production/)
          - [em](../9N39/1ns%20Results/1ns_test/em/)
        - [mdpocket_figures](../9N39/1ns%20Results/mdpocket_figures/)
        - [occupancy_maps](../9N39/1ns%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../9N39/1ns%20Results/plumed_metad_cvs/)
        - [probe_behaviour_analysis](../9N39/1ns%20Results/probe_behaviour_analysis/)
        - [representative_snapshots](../9N39/1ns%20Results/representative_snapshots/)
          - [P01A_probespecific_snapshots](../9N39/1ns%20Results/representative_snapshots/P01A_probespecific_snapshots/)
          - [P02A_probespecific_snapshots](../9N39/1ns%20Results/representative_snapshots/P02A_probespecific_snapshots/)
          - [P03A_probespecific_snapshots](../9N39/1ns%20Results/representative_snapshots/P03A_probespecific_snapshots/)
          - [P04A_probespecific_snapshots](../9N39/1ns%20Results/representative_snapshots/P04A_probespecific_snapshots/)
          - [global_snapshots](../9N39/1ns%20Results/representative_snapshots/global_snapshots/)
    - [Final_validation_test_5HO4](../Final_validation_test_5HO4/)
      - [100ps_test](../Final_validation_test_5HO4/100ps_test/)
        - [NPT_equil](../Final_validation_test_5HO4/100ps_test/NPT_equil/)
        - [NVT_equil](../Final_validation_test_5HO4/100ps_test/NVT_equil/)
        - [Production](../Final_validation_test_5HO4/100ps_test/Production/)
        - [em](../Final_validation_test_5HO4/100ps_test/em/)
  - [exploratory_examples](../../exploratory_examples/)
    - [docking_4MZI_roscovitine](../../exploratory_examples/docking_4MZI_roscovitine/)
  - [images](../../images/)
<!-- /REPO_TOC -->






























--------------------------------------------------------
## Readme Table of Contents
- [FBDD Repository Structure](#fbdd-repository-structure)
  - [Readme Table of Contents](#readme-table-of-contents)
- [4MZI](#4mzi)
- [100ps Results](#100ps-results)
- [1ns Results](#1ns-results)
- [1ns\_withpullres\_withcheckpoints Results](#1ns_withpullres_withcheckpoints-results)

--------------------------------------------------------
# 4MZI
[⬆️ Back to top](#readme-table-of-contents)

This folder contains the data and results for a workflow with 4MZI using aLMMD (accelerated Ligand-Mapping Molecular Dynamics).


# 100ps Results
[⬆️ Back to top](#readme-table-of-contents)

This folder contains the representative/test results from the **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** pipeline such as energy, temperature and bias plots, as well as post-processing plots (eg. occupancy maps) for a 100ps production run.

# 1ns Results
[⬆️ Back to top](#readme-table-of-contents)

This folder contains the representative/test results from the **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** pipeline such as energy, temperature and bias plots, as well as post-processing plots (eg. occupancy maps) for a 1ns production run.

# 1ns_withpullres_withcheckpoints Results
[⬆️ Back to top](#readme-table-of-contents)

This folder contains the representative/test results from the **accelerated Ligand-Mapping Molecular Dynamics (aLMMD)** pipeline such as energy, temperature and bias plots, as well as post-processing plots (eg. occupancy maps) for a 1ns production run with pull restraints on the metal as well as multiple restarts from checkpoint/backup files to demonstrate functionality.
