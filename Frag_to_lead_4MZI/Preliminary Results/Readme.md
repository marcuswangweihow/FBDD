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
