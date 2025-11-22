# Preliminary Results
This folder contains the preliminary/test results from the pipeline such as energy, temperature and bias plots, as well as post-processing plots for a 100ps production run.

---

## energy.png
This plot shows the changes in the (instantaneous and smoothed) potential energy (kJ/mol) of the system as the MD simulation progresses ie. MD step increases. The plot shows that the system is stable ie. no large fluctuations in potential energy.
![Energy vs Steps](energy.png)

## temperature.png
This plot shows the changes in the (instantaneous and smoothed) temperature (K) of the system as the MD simulation progresses ie. MD step increases. The plot shows that the system is stable ie. no large fluctuations in temperature.
![Temparature vs Steps](temperature.png)

## energy_temperature_dual.png
This plot shows both of the changes in the (instantaneous and smoothed) temperature (K) of the system, as well as the changes in the (instantaneous and smoothed) potential energy (kJ/mol) of the system as the MD simulation progresses ie. MD step increases. The plot shows that the system is stable ie. no large fluctuations in temperature or potential energy.
![Energy/Temparature vs Steps](energy_temperature_dual.png)

## plumed_bias.png
This plot shows the changes in the bias (kJ/mol) of the system as the MD simulation progresses ie. MD step increases. The plot shows that most of the relevant collective variable (CV) regions have been visited since the increase in bias is slowing down.
![Bias vs Steps](plumed_bias.png)

## Calpha_Rg.png
This plot shows the changes in C-alpha Rg (nm) of the protein backbone as the MD simulation progresses ie. time increases.
![Calpha_Rg vs Time](Calpha_Rg.png)

## Calpha_Rg_RMSD_combined.png
This plot shows the changes in C-alpha Rg (nm) of the protein backbone as the MD simulation progresses ie. time increases. The plot shows that there is likely a structural change from ca. 0.065ns to ca. 0.095ns as marked by the drop in the radius of gyration together with an increase in RMSD, where RMSD measures deviation from the reference structure (the initial conformation). The fall in the radius of gyration indicates the protein is becoming more compact in that region of the trajectory. The smaller wells with fewer black dots represents shorter-lived or smaller deviations — minor conformational shifts, local motions, or fluctuations.
![Calpha_Rg_RMSD vs Time](Calpha_Rg_RMSD_combined.png)


# Benzene occupancy maps per windows
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./benzene_window1_cluster2.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./benzene_window2_cluster1.png" width="400">
    </td>
  </tr>
</table>

Benzene occupancy maps generated from the (A) Cluster 2 0–20ps and(B) Cluster 1 21–40ps analysis windows of the pipeline MD simulation of 100ps , superimposed on the representative protein structure (PDB structure 4MZI (human mutant p53) per window taken from the snapshot whose probe atoms overlap best with avg_grid peaks. Benzene occupancy maps are shown as black meshes.

The small cluster meshes are because each cluster is based on only a handful of snapshots (5 per window by default) and the short production run time of 100ps.Thus the isomesh polygons are tiny and scattered — the “hotspot” occupancy hasn’t had time to converge. Essentially, each mesh reflects a small number of probe binding events, not a fully sampled occupancy, which should be resolved once longer production runs (ns-scale) and more snapshots per window are done for smoother and more interpretable clusters. 




