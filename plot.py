import matplotlib.pyplot as plt
import numpy as np


def plot(x, y, xlabel, ylabel, title, filename):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


name_of_sim = 'ben_shalom_young'
target_path = './Results/' + name_of_sim

soma_AP_traces = np.loadtxt(f'{target_path}/soma_AP_traces.txt', delimiter='\t')
AIS_Na_current = np.loadtxt(f'{target_path}/ais_Na_current.txt', delimiter='\t')
results = np.loadtxt(f'{target_path}/spiking_results.txt', delimiter='\t')

plot(soma_AP_traces[:, 0], soma_AP_traces[:, 13], 'Time (ms)', 'Voltage (mV)', 'Soma AP Traces', f'{target_path}/soma_AP_traces.png')
plot(AIS_Na_current[:, 0], AIS_Na_current[:, 13], 'Time (ms)', 'Current (nA)', 'AIS Na Current', f'{target_path}/ais_Na_current.png')

plot(results[:, 0], results[:, 1], 'Current (nA)', 'Spike Count', 'Spiking Results', f'{target_path}/spiking_results.png')
plot(results[:, 0], results[:, 2], 'Current (nA)', 'AP voltage threshold (mV)', 'Spiking Results', f'{target_path}/threshold.png')
plot(results[:, 0], results[:, 3], 'Current (nA)', 'AP amplitude (mV)', 'Spiking Results', f'{target_path}/amplitude.png')
plot(results[:, 0], results[:, 4], 'Current (nA)', 'AP latency (ms)', 'Spiking Results', f'{target_path}/latency.png')
