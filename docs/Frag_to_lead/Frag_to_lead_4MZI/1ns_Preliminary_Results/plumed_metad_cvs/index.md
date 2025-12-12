---
title: "plumed_metad_cvs"
nav_order: 1
---

# plumed_metad_cvs

<!-- REPO_TOC -->
# FBDD Repository Structure
- [FBDD](../../../../)
  - [Frag_to_lead](../../../)
    - [Frag_to_lead_4MZI](../../)
      - [100ps_Preliminary Results](../../100ps_Preliminary%20Results/)
        - [100ps_pipeline_test](../../100ps_Preliminary%20Results/100ps_pipeline_test/)
          - [NPT_equil](../../100ps_Preliminary%20Results/100ps_pipeline_test/NPT_equil/)
          - [NVT_equil](../../100ps_Preliminary%20Results/100ps_pipeline_test/NVT_equil/)
          - [Production](../../100ps_Preliminary%20Results/100ps_pipeline_test/Production/)
          - [em](../../100ps_Preliminary%20Results/100ps_pipeline_test/em/)
        - [binding_event_detection](../../100ps_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../100ps_Preliminary%20Results/mdpocket_figures/)
        - [plumed_metad_cvs](../../100ps_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../100ps_Preliminary%20Results/representative_snapshots/)
      - [100ps_run_for_checkpoint_testing](../../100ps_run_for_checkpoint_testing/)
      - [1ns_Preliminary Results](../)
        - [1ns_pipeline_test](../1ns_pipeline_test/)
          - [NPT_equil](../1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../1ns_pipeline_test/NVT_equil/)
          - [Production](../1ns_pipeline_test/Production/)
          - [em](../1ns_pipeline_test/em/)
        - [binding_event_detection](../binding_event_detection/)
        - [mdpocket_figures](../mdpocket_figures/)
        - [occupancy_maps](../occupancy_maps/)
        - [plumed_metad_cvs](./)
        - [representative_snapshots](../representative_snapshots/)
      - [1ns_withpullres_withcheckpoints_Preliminary Results](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/)
        - [1ns_pipeline_test](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/)
          - [NPT_equil](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NPT_equil/)
          - [NVT_equil](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/NVT_equil/)
          - [Production](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/Production/)
          - [em](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/1ns_pipeline_test/em/)
        - [binding_event_detection](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/binding_event_detection/)
        - [mdpocket_figures](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/mdpocket_figures/)
        - [occupancy_maps](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/occupancy_maps/)
        - [plumed_metad_cvs](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/plumed_metad_cvs/)
        - [representative_snapshots](../../1ns_withpullres_withcheckpoints_Preliminary%20Results/representative_snapshots/)
  - [docking_4MZI_roscovitine](../../../../docking_4MZI_roscovitine/)
  - [images](../../../../images/)
<!-- /REPO_TOC -->





---------------------------------------------------------

plumed_bias_scalar.dat and plumed_com_components.dat contain the raw data for the below plots. These files were generated from a 1ns production test run. 

**All results shown here are preliminary results and only serve to show workflow/pipeline functionality.**

# From plumed_bias_scalar.dat
## Distance and torsion plots

The distance vs time plots as well as the torsions vs time plots obtained by plotting the data from plumed_bias_scalar.dat are just for sanity checks.

The plots show that the dihedrals change with time and the probes are moving, which shows the system is working.

## Distance vs time plots
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./Distance_d1.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./Distance_d2.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./Distance_d3.png" width="400">
    </td>
  </tr>
</table>

<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>D</h3>
      <img src="./Distance_d4.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>E</h3>
      <img src="./Distance_d5.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>F</h3>
      <img src="./Distance_d6.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>G</h3>
      <img src="./Distance_d7.png" width="400">
    </td>
  </tr>
</table>



## Torsions vs time plots
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./Torsion_t1.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./Torsion_t2.png" width="400">
    </td>
  </tr>
</table>

<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./Torsion_t3.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>D</h3>
      <img src="./Torsion_t4.png" width="400">
    </td>
  </tr>
</table>

## Combined torsions vs time plot
![Combined torsions vs Time](Torsions_Combined.png)

---
# From plumed_com_components.dat

With more probes and longer simulations, the 2D/3D COM density plots could become informative about preferred probe regions, which might correspond to cryptic or binding sites.

Otherwise with just 8 probes and 1ns runs, mostly a sanity check. Also with 8 probes the combined plots are quite messy.

## Per-probe (x,y,z) plots
See if any probe is behaving weirdly.
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./COM_P01A.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./COM_P02A.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./COM_P03A.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>D</h3>
      <img src="./COM_P04A.png" width="400">
    </td>
  </tr>
</table>

<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./COM_P01B.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./COM_P02B.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./COM_P03B.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>D</h3>
      <img src="./COM_P04B.png" width="400">
    </td>
  </tr>
</table>

## Combined per-axis plots (x-only, y-only, z-only)
Detects if probes drift together or if one is outlier.
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./COM_combined_x.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./COM_combined_y.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./COM_combined_z.png" width="400">
    </td>
  </tr>
</table>

## 2D projections (x-y, x-z, y-z)
See if probes overlap unphysically or leave the expected region.
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./COM_x_vs_y.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./COM_x_vs_z.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./COM_y_vs_z.png" width="400">
    </td>
  </tr>
</table>

## 3D COM scatter
Good for spotting impossible geometries, clustering, or probes stuck together.

For multiple copies or long simulations, dense clusters may indicate potential hotspots or binding regions. 

![3D COM scatter](COM_3D.png)

## Pairwise COM distances
To confirm probes don’t collide or drift apart unexpectedly.
![Pairwise COM distances](COM_pairwise_distances.png)

