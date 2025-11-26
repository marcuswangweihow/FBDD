plumed_bias_scalar.dat and plumed_com_components.dat contain the raw data for the below plots. These files were generated from a short 100ps production test run. 

**All results shown here are preliminary results and only serve to show workflow/pipeline functionality.**

# From plumed_bias_scalar.dat
## Distance and torsion plots

The distance vs time plots as well as the torsions vs time plots obatined by plotting the data from plumed_bias_scalar.dat are just for sanity checks.

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

Otherwise with just 4 probes and short 100ps runs, mostly a sanity check.

## Per-probe (x,y,z) plots
See if any probe is behaving weirdly.
<table style="border-collapse: collapse; border: none;">
  <tr>
    <td style="border: none; text-align: center;">
      <h3>A</h3>
      <img src="./COM_P01.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>B</h3>
      <img src="./COM_P02.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>C</h3>
      <img src="./COM_P03.png" width="400">
    </td>
    <td style="border: none; text-align: center;">
      <h3>D</h3>
      <img src="./COM_P04.png" width="400">
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
