# Pyramidal neuron model for studying ***SCN2A*** mutations

This repository contains NEURON and Python files to simulate the effect of 
different *SCN2A* mutations in a reconstructed mouse cortical L5 pyramidal neuron. This model was used to study the effect of sodium channel mutations on the firing rate of a pyramidal neuron in the following publication ([Asadollahi et al. 2023](https://doi.org/10.1093/hmg/ddad048)): 

Asadollahi R., Delvendahl I., et al. (2023) Pathogenic *SCN2A* variants cause early-stage dysfunction in patient-derived neurons. Human Molecular Genetics, ddad048 (doi:10.1093/hmg/ddad048)

The model was constructed using the [NEURON](https://neuron.yale.edu/) modeling language and is based on the implementation by 
[Ben-Shalom et al. 2017](http://dx.doi.org/10.1016/j.biopsych.2017.01.009) 
of the model that accompanied the paper "State and
location dependence of action potential metabolic 
cost" ([Hallermann et al. 2012](http://dx.doi.org/10.1038/nn.3132)).
  
Simulations were run with NEURON 8.0 in Python 3.8.12 (NEURON can be installed via `pip install neuron`). Python dependencies: neuron, numpy, scipy (run `pip install -r requirements.txt`)

To run simulations:  
* compile all .mod files (cd to directory and execute `nrnivmodl`)
* in run_simulation.py, select which model to run by setting the name of the .hoc file to be loaded (from "/sim_files/" folder), e.g.:  
  `name_of_sim = 'youngPN'`
* In the paper, the different simulation runs were the following:
  * WT (100% SCN2A): "youngPN"
  * 50% SCN2A: "youngPN_scn2a_ais_50perc"
  * 0% SCN2A: "youngPN_scn2a_ais_0perc"
  * E1803G: "youngPN_scn2a_ais_E1803G_het_2"
* adjust current injection amplitude and number of increasing sweeps, if desired:  
  `currentstep = 0.1`  
  `sweeps = 24`
* run the file run_simulation.py
* the file run_simulation_MP.py can be used for running multiple simulations in parallel using multiprocessing
* the file plot_results.py can be used for plotting the results

The simulation output is saved as .txt files into the folder "Results/". Subfolders are created for each independent condition. Output files are:
* "spiking_results.txt" -> current injection, spike numbers, threshold, amplitude and spike delay, spikes AIS, threshold AIS, amplitude AIS, soma I_Na, AIS_I_Na
* "soma_AP_traces.txt" -> voltage traces of the soma
* "soma_Na_current.txt" -> Na current traces (from soma)
* "ais_Na_current.txt"  -> Na current traces (from AIS)
  
  
---  
Contact:
igor.delvendahl@uzh.ch