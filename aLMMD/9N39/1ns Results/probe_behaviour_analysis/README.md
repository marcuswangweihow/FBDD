<!-- REPO_TOC -->
# FBDD Repository Structure
- [FBDD](../../../../)
  - [Docking](../../../../Docking/)
  - [Fragment_processing](../../../../Fragment_processing/)
  - [aLMMD](../../../)
    - [4MZI](../../../4MZI/)
      - [100ps Results](../../../4MZI/100ps%20Results/)
        - [100ps_pipeline_test](../../../4MZI/100ps%20Results/100ps_pipeline_test/)
          - [NPT_equil](../../../4MZI/100ps%20Results/100ps_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../4MZI/100ps%20Results/100ps_pipeline_test/NVT_equil/)
          - [Production](../../../4MZI/100ps%20Results/100ps_pipeline_test/Production/)
          - [em](../../../4MZI/100ps%20Results/100ps_pipeline_test/em/)
        - [binding_event_detection](../../../4MZI/100ps%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../4MZI/100ps%20Results/mdpocket_figures/)
        - [plumed_metad_cvs](../../../4MZI/100ps%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../4MZI/100ps%20Results/representative_snapshots/)
      - [100ps_run_for_checkpoint_testing](../../../4MZI/100ps_run_for_checkpoint_testing/)
      - [1ns Results](../../../4MZI/1ns%20Results/)
        - [1ns_pipeline_test](../../../4MZI/1ns%20Results/1ns_pipeline_test/)
          - [NPT_equil](../../../4MZI/1ns%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../4MZI/1ns%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](../../../4MZI/1ns%20Results/1ns_pipeline_test/Production/)
          - [em](../../../4MZI/1ns%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](../../../4MZI/1ns%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../4MZI/1ns%20Results/mdpocket_figures/)
        - [occupancy_maps](../../../4MZI/1ns%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../../../4MZI/1ns%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../4MZI/1ns%20Results/representative_snapshots/)
      - [1ns_withpullres_withcheckpoints_Preliminary Results](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/)
        - [1ns_pipeline_test](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/)
          - [NPT_equil](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/Production/)
          - [em](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/mdpocket_figures/)
        - [occupancy_maps](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../../4MZI/1ns_withpullres_withcheckpoints_Preliminary%20Results/representative_snapshots/)
    - [9N39](../../)
      - [1ns Results](../)
        - [1ns_test](../1ns_test/)
          - [NPT_equil](../1ns_test/NPT_equil/)
          - [NVT_equil](../1ns_test/NVT_equil/)
          - [Production](../1ns_test/Production/)
          - [em](../1ns_test/em/)
        - [mdpocket_figures](../mdpocket_figures/)
        - [occupancy_maps](../occupancy_maps/)
        - [plumed_metad_cvs](../plumed_metad_cvs/)
        - [probe_behaviour_analysis](./)
        - [representative_snapshots](../representative_snapshots/)
          - [P01A_probespecific_snapshots](../representative_snapshots/P01A_probespecific_snapshots/)
          - [P02A_probespecific_snapshots](../representative_snapshots/P02A_probespecific_snapshots/)
          - [P03A_probespecific_snapshots](../representative_snapshots/P03A_probespecific_snapshots/)
          - [P04A_probespecific_snapshots](../representative_snapshots/P04A_probespecific_snapshots/)
          - [global_snapshots](../representative_snapshots/global_snapshots/)
    - [Final_validation_test_5HO4](../../../Final_validation_test_5HO4/)
      - [100ps_test](../../../Final_validation_test_5HO4/100ps_test/)
        - [NPT_equil](../../../Final_validation_test_5HO4/100ps_test/NPT_equil/)
        - [NVT_equil](../../../Final_validation_test_5HO4/100ps_test/NVT_equil/)
        - [Production](../../../Final_validation_test_5HO4/100ps_test/Production/)
        - [em](../../../Final_validation_test_5HO4/100ps_test/em/)
  - [exploratory_examples](../../../../exploratory_examples/)
    - [docking_4MZI_roscovitine](../../../../exploratory_examples/docking_4MZI_roscovitine/)
  - [images](../../../../images/)
<!-- /REPO_TOC -->



























-----------------

# Probe behaviour analysis

This module performs probe aggregation diagnostics and probe cavity residency calculations. Binding events are now defined as a time interval where a probe resides within a defined protein cavity, optionally supported by a KDE density maximum.


**All results shown are preliminary and are used to demonstrate pipeline/workflow functionality.**

## Probe aggregation diagnostic

Uses COMs of probes to identify aggregation events with a user-defined `aggregation_distance_threshold` and `aggregation_time_threshold`. Outputs a list of aggregations events in a json. If no aggregation events are recorded, the json will explicitly contain a "no aggregation events" message.

## Probe–cavity residency

Uses COMs of probes and MDpocket cavity centroids to compute the time spent by probes spent inside cavities. This is done per probe and per cavity. Outputs a json containing all calculated data as well as cavity occupancy visualisations.

### Cavity occupancy visualisations
For the 1ns simulation run analyzed here, no probe–cavity residency events were observed within the selected distance threshold. This is expected given the short simulation timescale and the absence of translational or cavity-targeted biasing. Thermal fluctuations lead to local probe motion but are insufficient to drive spontaneous entry into MDpocket-defined cavities within the current simulation time.

 
