from neuron import h
from neuron.units import ms, mV
import numpy as np
import functions
from multiprocessing import Pool
from datetime import datetime
import os
import sys


def initialize(filename):
    """
    initialize NEURON simulation environment and Hallermann et al. 2012 model

    :param filename: name of .hoc file for the simulation
    """
    h.load_file("stdgui.hoc")
    h.load_file('stdrun.hoc')
    h.load_file('morphology.hoc')
    h.load_file(filename)
    print(filename)

    h.parameters()
    h.geom_nseg()
    h.init_channels()


def cc_simulation(currentinjection):
    """
    Runs CC simulation of Hallermann et al. 2012 model and returns a list of simulation results
    :param currentinjection: amplitude (nA) of current injection to run simulation with
    :return: list of results (clamp.amp, spikes_soma, threshold_soma, ap_amp_soma, ap_delay, 
     spikes_ais, threshold_ais, ap_amp_ais, peak_na, peak_ais_na).
     "soma_voltage" and "axon_voltage" are raw voltage traces from NEURON. "ina", "ina_ais" 
     are raw Na-current traces from NEURON (total Na current and AIS Na current).
    """

    # general NEURON settings
    recordTime = 650.0 * ms
    h.celsius = 33
    v_init = -85 * mV

    # clamp definition
    clamp = h.IClamp(h.soma(0.5))
    clamp.delay = 500 * ms
    clamp.dur = 100 * ms
    clamp.amp = currentinjection

    # record data
    t_vec = h.Vector().record(h._ref_t)
    v_soma = h.Vector().record(h.soma(0.5)._ref_v)
    v_axon = h.Vector().record(h.axon[0](1)._ref_v)
    ina = h.Vector().record(h.soma(0.5)._ref_ina)
    ina_ais = h.Vector().record(h.axon[0](0.2)._ref_ina)

    # run simulation with current injection
    h.finitialize(v_init)
    h.fcurrent()
    h.continuerun(recordTime)

    # convert NEURON vector to python
    soma_voltage = v_soma.to_python()
    axon_voltage = v_axon.to_python()
    na_current = ina.to_python()
    ais_na_current = ina_ais.to_python()

    # compute spike delay, number, threshold and amplitude for soma
    start = int(clamp.delay / h.dt)
    end = int((clamp.delay + clamp.dur) / h.dt)
    st = []
    for j in range(start, end):
        if v_soma[j] <= -20 * mV and v_soma[j + 1] > -20 * mV:
            st.append(t_vec[j])
    ap_delay = (st[0] - clamp.delay) if len(st) else float('NaN')
    spikes_soma, threshold_soma, ap_amp_soma = functions.get_spikes(soma_voltage[start:end], h.dt)
    # compute spike number, threshold and amplitude for ais
    spikes_ais, threshold_ais, ap_amp_ais = functions.get_spikes(axon_voltage[start:end], h.dt)
    # get peak Na current
    peak_na = functions.get_na_peak(na_current[start:end])
    peak_ais_na = functions.get_na_peak(ais_na_current[start:end])

    print('%.2f nA \t %2d \t\t %.1f mV \t %.1f ms \t %.1f mV \t %.1f nA' % (clamp.amp, spikes_soma, threshold_soma, ap_delay, ap_amp_soma, peak_na))
    result = [clamp.amp, spikes_soma, threshold_soma, ap_amp_soma, ap_delay, spikes_ais, threshold_ais, ap_amp_ais, peak_na, peak_ais_na]

    return result, soma_voltage, ina, ina_ais


def save_results(results, path):
    """
    saves data to textfiles

    :param results: results list returned from the cc_simulation function
    :param path: path to save results to
    :return: no return value
    """

    results.sort()
    spiking, somatraces, totalna, ais_na = zip(*results)
    t = np.linspace(0, (len(somatraces[0]) - 1) * h.dt, len(somatraces[0]))

    # save the results to file
    np.savetxt(path+'/spiking_results.txt', spiking, fmt=['%.2f', '%2d', '%.3f', '%.3f', '%.3f', '%2d', '%.3f', '%.3f', '%.3f', '%.3f'], delimiter='\t')
    ap_traces = np.transpose(np.vstack((t, somatraces)))
    np.savetxt(path+'/soma_AP_traces.txt', ap_traces, fmt='%.5f', delimiter='\t')
    na_traces = np.transpose(np.vstack((t, totalna)))
    np.savetxt(path+'/soma_Na_current.txt', na_traces, fmt='%.5f', delimiter='\t')
    na_ais_traces = np.transpose(np.vstack((t, ais_na)))
    np.savetxt(path+'/ais_Na_current.txt', na_ais_traces, fmt='%.5f', delimiter='\t')


def ais_diam():
    """
    prints length and diameter of AIS (=axon[0])
    """
    print('Axon length (um): {}'.format(h.axon[0].L))
    print('Axon diameter (um):')
    for i in np.linspace(0, 1, 11):
        print(h.axon[0](i).diam)


def soma_size():
    """
    prints length, diameter and area of soma
    """
    print('Soma length (um): {}'.format(h.soma.L))
    print('Soma diameter (um): {}'.format(h.soma.diam))
    print('Soma area (um^2): {}'.format(h.soma(0.5).area()))
    print('')


if __name__ == '__main__':

    startTime = datetime.now()

    # name_of_sim = os.path.splitext(sys.argv[1])[0]
    name_of_sim = 'youngPN_scn2a_ais_E1803G_het'

    target_path = './Results/' + name_of_sim
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    path_to_hocfile = f'./sim_files/{name_of_sim}.hoc'
    initialize(path_to_hocfile)
    h.dt = 0.02

    # ais_diam()
    # soma_size()

    print('AIS (0.2) gbar\tscn2a: %.2f\tmutated scn2a: %.2f' % (h.axon[0](0.2).nav12.gbar, h.axon[0](0.2).nav12_mut.gbar))
    print('AIS (0.4) gbar\tscn8a: %.2f' % (h.axon[0](0.4).nav18.gbar))

    # current injection protocol
    currentstep = 0.1 # nA
    sweeps = 24
    # start from 1 nA to save computation time
    currents = [1 + x * currentstep for x in range(sweeps)]

    # print results
    print('\ncurrent: \t # spikes: \t AP threshold: \t spike delay: \t spike amplitude: \t peak na current:')

    with Pool() as p:
        results = p.map(cc_simulation, currents)

    save_results(results, target_path)
    print(datetime.now() - startTime)
