import numpy as np
from scipy.signal import find_peaks


def set_rates_na8st(seg, rates, vshift_inact=0):
    """
    Sets the rates for the 8-state model in segment seg.
    vshift_inact can be used to locally change the voltage
    dependence of inactivation rates.

    :param seg: the segment to set rates for
    :param rates: numpy array of na8st.mod rates
    :param vshift_inact: the incativation shift parameter
    :return: none
    """
    n_r = 0
    seg.a1_0_na = rates[n_r];    n_r += 1  # 0
    seg.a1_1_na = rates[n_r];    n_r += 1  # 1

    seg.b1_0_na = rates[n_r];    n_r += 1  # 2
    seg.b1_1_na = rates[n_r];    n_r += 1  # 3

    seg.a2_0_na = rates[n_r];    n_r += 1  # 4
    seg.a2_1_na = rates[n_r];    n_r += 1  # 5

    seg.b2_0_na = rates[n_r];    n_r += 1  # 6
    seg.b2_1_na = rates[n_r];    n_r += 1  # 7

    seg.a3_0_na = rates[n_r];    n_r += 1  # 8
    seg.a3_1_na = rates[n_r];    n_r += 1  # 9

    seg.b3_0_na = rates[n_r];    n_r += 1  # 10
    seg.b3_1_na = rates[n_r];    n_r += 1  # 11

    seg.bh_0_na = rates[n_r];    n_r += 1  # 12
    seg.bh_1_na = rates[n_r];    n_r += 1  # 13
    seg.bh_2_na = rates[n_r];    n_r += 1  # 14

    seg.ah_0_na = rates[n_r];    n_r += 1  # 15
    seg.ah_1_na = rates[n_r];    n_r += 1  # 16
    seg.ah_2_na = rates[n_r]               # 17

    seg.vShift_inact_local_na = vshift_inact


def set_rates_scn2a(seg, rates, vshift_inact=0):
    """
    Sets the rates for the 8-state model in segment seg.
    vshift_inact can be used to locally change the voltage
    dependence of inactivation rates.

    :param seg: the segment to set rates for
    :param rates: numpy array of na8st.mod rates
    :param vshift_inact: the incativation shift parameter
    :return: none
    """
    n_r = 0
    seg.a1_0_scn2a = rates[n_r];    n_r += 1  # 0
    seg.a1_1_scn2a = rates[n_r];    n_r += 1  # 1

    seg.b1_0_scn2a = rates[n_r];    n_r += 1  # 2
    seg.b1_1_scn2a = rates[n_r];    n_r += 1  # 3

    seg.a2_0_scn2a = rates[n_r];    n_r += 1  # 4
    seg.a2_1_scn2a = rates[n_r];    n_r += 1  # 5

    seg.b2_0_scn2a = rates[n_r];    n_r += 1  # 6
    seg.b2_1_scn2a = rates[n_r];    n_r += 1  # 7

    seg.a3_0_scn2a = rates[n_r];    n_r += 1  # 8
    seg.a3_1_scn2a = rates[n_r];    n_r += 1  # 9

    seg.b3_0_scn2a = rates[n_r];    n_r += 1  # 10
    seg.b3_1_scn2a = rates[n_r];    n_r += 1  # 11

    seg.bh_0_scn2a = rates[n_r];    n_r += 1  # 12
    seg.bh_1_scn2a = rates[n_r];    n_r += 1  # 13
    seg.bh_2_scn2a = rates[n_r];    n_r += 1  # 14

    seg.ah_0_scn2a = rates[n_r];    n_r += 1  # 15
    seg.ah_1_scn2a = rates[n_r];    n_r += 1  # 16
    seg.ah_2_scn2a = rates[n_r]               # 17

    seg.vShift_inact_local_scn2a = vshift_inact


def get_spikes(data, delta_x, threshold=50, minpeak=-20):
    """
    Calculates first derivative of input data
    and returns spike number according to threshold crossings
    :param data: input data (list or 1d-numpy array)
    :param delta_x: the time step
    :param threshold: spike threshold (derivative crossing; default=50V/s)
    :param minpeak: minimum voltage for AP peak (default=-20mV)
    :return: list with the number of spikes, AP voltage threshold, and AP amplitude
    """
    dVdt = np.gradient(data, delta_x)
    threshold_crossings = np.diff(dVdt > threshold, append=False)
    indices = np.argwhere(threshold_crossings)[::2,0]
    num_spikes = len(indices)

    if num_spikes > 0:
        peaks, _ = find_peaks(data, height=minpeak)
        APthreshold = data[indices[0]]
        APamplitude = data[peaks[0]] - data[indices[0]]
    else:
        APthreshold = float('NaN')
        APamplitude = float('NaN')

    return num_spikes, APthreshold, APamplitude


def get_na_peak(data):
    """
    Calculates and returns minimum of input data
    :param data: input data (list or 1d-numpy array)
    :return: minimum of data
    """
    x = np.abs(np.array(data))
    peaks, properties = find_peaks(x, height=0.05)

    return properties['peak_heights'].max() if len(peaks) else float('NaN')


def get_shape_plot_data(data, delta_x, threshold):
    """
    Calculates first derivative of input data
    and returns voltage and dV/dt for first spike according to threshold crossing

    :param data: input data (list or 1d-numpy array)
    :param delta_x: the time step
    :param threshold: spike threshold (derivative crossing)
    :return: voltage and its time derivative
    """

    dVdt = np.gradient(data, delta_x)
    st = [j for j in range(len(dVdt) - 1)
          if dVdt[j] <= threshold and dVdt[j + 1] > threshold]

    if len(st) > 0:
        start, end = int(st[0] - (2.5 / delta_x)), int(st[0] + (2.2 / delta_x))
        voltage = data[start:end]
        gradient = dVdt[start:end]
    else:
        voltage = data
        gradient = dVdt

    return voltage, gradient
