# Binding Event Detection and Pocket Mapping

This module performs integrated COM clustering of probe fragments along MD trajectories and maps clusters to MDpocket-derived density peaks to identify potential binding pockets and transient binding events.

Cluster → Density Peak mapping: Each cluster centroid is assigned to the nearest MDpocket density peak (DensPeak_X).

If a cluster is farther than a user-defined threshold (e.g., 3 Å) from any density peak, it is labeled Pocket_X.

**All results shown are preliminary and are used to demonstrate pipeline/workflow functionality.**

## Binding event detection: Track consecutive frames where a probe is in a cluster.

Events lasting longer than dbscan_min_samples frames are reported as binding events.

## Interpretation:

DensPeak_X clusters are likely near real pockets detected by MDpocket.

Pocket_X clusters may represent transient, low-occupancy, or previously unidentified pockets.

Binding events summarize when and for how long a probe occupies a particular cluster/pocket. Once clusters are labeled, users can track how long a probe resides in a cluster → gives residence times, which are biologically relevant.

## Outputs:

JSON file: enhanced_clustering_results_TIMESTAMP.json with cluster centroids, names, distances to peaks, and binding events.

3D COM plots: probe trajectories color-coded by cluster labels.

3D COM plots from a short 100ps production test run. The results shown are preliminary and are used to demonstrate pipeline/workflow functionality.



## Usage of JSON file for numerical cluster detection → structural snapshot → physical interpretation:

### Open JSON → see which clusters survived as “binding events”

Compare cluster names to plots to confirm physical location

DensPeak → matches an MDpocket peak

Pocket_X → a cluster far from any peak, might be minor or transient

### Once you identify a cluster / binding event of interest:

Use the rep_frame_pdb listed in the JSON (and saved in the cv_plots_dir) or extract frames manually from the full trajectory

Open in PyMOL/Chimera

Overlay protein + probe COMs to see how the probe binds in that cluster
