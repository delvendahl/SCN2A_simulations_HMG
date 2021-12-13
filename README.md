## SCN2A_simulation

## NEURON model of SCN2A mutations


# Pyramidal neuron model for studying ***SCN2A*** mutations

This directory contains NEURON and Python files to simulate the effect of 
different *SCN2A* mutations in a reconstructed pyramidal neuron. 
The model is based on the implementation by 
[Ben-Shalom et al. 2017](http://dx.doi.org/10.1016/j.biopsych.2017.01.009) 
of the model that accompanied the paper "State and
location dependence of action potential metabolic 
cost" ([Hallermann et al. 2012](http://dx.doi.org/10.1038/nn.3132)).
  
Simulations were run with NEURON 8.0 in Python 3.8.12 (NEURON can be install via `pip install neuron`). Python dependencies: neuron, numpy, scipy

To run simulations:  
* compile all .mod files (cd to directory and execute `nrnivmodl`)
* in run_simulation.py, select model to run by setting the name of the .hoc file to be loaded (from "/sim_files" folder):  
e.g.  
  `name_of_sim = 'ben_shalom_young'`
* The different simulation runs were the following:
  * WT (100% SCN2A): "ben_shalom_young"
  * 50% SCN2A: "youngPN_scn2a_ais_50perc"
  * 0% SCN2A: "youngPN_scn2a_ais_0perc"
  * E1803G: "youngPN_scn2a_ais_E1803G_het_2"
* adjust current injection amplitude and number of increasing sweeps, if desired:  
  `currentstep = 0.1`  
  `sweeps = 24`
* run run_simulation.py
* the file run_simulation_MP.py can be used for using multiprocessing

The simulation output is saved as .txt files into the folder "Results/".
  
  
---  
Contact:
igor.delvendahl@uzh.ch