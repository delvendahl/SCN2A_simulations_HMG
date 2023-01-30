import matplotlib.pyplot as plt
import numpy as np
from neuron import h


def plot(x, y, xlabel, ylabel, title, filename):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


name_of_sim = 'youngPN'
target_path = './Results/' + name_of_sim

soma_AP_traces = np.loadtxt(f'{target_path}/soma_AP_traces.txt', delimiter='\t')
AIS_Na_current = np.loadtxt(f'{target_path}/ais_Na_current.txt', delimiter='\t')
results = np.loadtxt(f'{target_path}/spiking_results.txt', delimiter='\t')

# plot voltage at some and Na current at AIS:
plot(soma_AP_traces[:, 0], soma_AP_traces[:, 13], 'Time (ms)', 'Voltage (mV)', 'Soma AP Traces', f'{target_path}/soma_AP_traces.png')
plot(AIS_Na_current[:, 0], AIS_Na_current[:, 13], 'Time (ms)', 'Current (nA)', 'AIS Na Current', f'{target_path}/ais_Na_current.png')

# plot spiking results:
plot(results[:, 0], results[:, 1], 'Current (nA)', 'Spike Count', 'Spiking Results', f'{target_path}/spiking_results.png')
plot(results[:, 0], results[:, 2], 'Current (nA)', 'AP voltage threshold (mV)', 'AP Threshold Results', f'{target_path}/threshold.png')
plot(results[:, 0], results[:, 3], 'Current (nA)', 'AP amplitude (mV)', 'AP amplitude Results', f'{target_path}/amplitude.png')
plot(results[:, 0], results[:, 4], 'Current (nA)', 'AP latency (ms)', 'AP latency Results', f'{target_path}/latency.png')

# plot the neuron's morphology
h.load_file('morphology.hoc')
for sec in h.allsec():
    if 'apic' in str(sec):
        sec.v = 0
ps = h.PlotShape(False)
ps.plot(plt)
plt.savefig(f'{target_path}/morphology.png')
plt.show()
