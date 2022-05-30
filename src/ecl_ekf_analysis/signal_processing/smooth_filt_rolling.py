# /usr/bin/env python3
"""
This library contains helper functions for smoothing, filtering and applying functions to rolling
windows.

- For applying any function over a rolling window: use apply_rolling_run_1d_boundaries.
- For smoothing use:
    - smooth_1d_boundaries: for a simple fast average smoother
    - scipy.signal.savgol_filter: for a polynomial filter
- For filtering:
    - for low-pass use:
        b, a = scipy.signal.butter(order, fs, btype='low'); fs: sample rate
        signal_low = scipy.signal.filtfilt(b, a, input_signal, padlen=padlen)
    - for high-pass use:
        b, a = scipy.signal.butter(order, fs, btype='high'); fs: sample rate
        signal_high = scipy.signal.filtfilt(b, a, input_signal, padlen=padlen)
    use lfilter instead of filtfilt for realtime streaming processing (filtfilt works for offline
    post-processing without phase-shift)
"""
from typing import Callable

import numpy as np
from scipy.signal import butter, filtfilt


def butter_filter_1d(
        input_signal: np.ndarray,
        cut_off: float,
        sample_rate: float,
        order: int = 5,
        btype: str = 'low') -> np.ndarray:
    """
    simple butterworth filter implementation. This assumes a regularly sampled input signal!
    :param input_signal:
    :param cut_off:
    :param sample_rate:
    :param order:
    :param btype: one of low, high, bandpass, bandstop
    :return:
    """
    nyq_freq = 0.5 * sample_rate
    normalized_cutoff = cut_off / nyq_freq
    b, a = butter(order, normalized_cutoff, btype=btype)
    y = filtfilt(b, a, input_signal)
    return y


def apply_rolling_fun_1d_boundaries(
        input_signal: np.ndarray, fun: Callable, window_len: int = 51,
        mode: str = 'valid') -> np.ndarray:
    """
    apply's a function to a rolling window for 1d signals.
    :param input_signal: the 1d input signal.
    :param fun: the function to apply on the rolling window: needs to return a single floating
        point statistic for the window.
    :param window_len: window length in number of samples.
    :param mode: valid selectors:
        'valid':    no padding is applied, the output signal is starts window_len/2 after the signal
                    start and ends window_len/2 before the signal end
        'same'      the output signal has the same length as the input signal. the input signal is
                    padded with zeros at the start and end to achieve this.
        'mirror':   the output signal has the same length as the input signal. this is achieved by
                    mirroring the input signal at it's begin and end.
    :return: the resulting 1d output signal.
    """
    if mode == 'mirror':
        extended_signal = np.concatenate(
            (input_signal[int(window_len / 2):0:-1], input_signal,
             input_signal[-2:-int(window_len / 2) - 2:-1]))
        filtered_signal = apply_rolling_fun_1d(
            extended_signal, fun, window_len)
    elif mode == 'same':
        extended_signal = np.concatenate(
            (np.zeros(int(window_len / 2)), input_signal, np.zeros(int(window_len / 2))))
        filtered_signal = apply_rolling_fun_1d(
            extended_signal, fun, window_len)
    elif mode == 'valid':
        filtered_signal = apply_rolling_fun_1d(input_signal, fun, window_len)
    else:
        raise NotImplementedError(f'mode {mode:s} not implemented')

    return filtered_signal


def smooth_1d_boundaries(
        input_signal: np.ndarray,
        window_len: int = 51,
        window_type: str = 'flat',
        mode: str = 'mirror',
        mean_for_short_signals: bool = False) -> np.ndarray:
    """
    apply's a smoothing function to a rolling window for 1d signals using convolution. This
    function is generally faster than the apply_rolling_fun_1d_boundaries.
    :param input_signal: the 1d input signal.
    :param window_len: window length in number of samples.
    :param window_type: the window type, valid selectors:
        'flat':     a convolution operator with ones for a standard average smoothing function
        'hanning':  a hanning window operator
        'hamming':  a hamming window operator
        'bartlett'  a bartlett window operator
        'blackman'  a blackman winowd operator
    :param mode: valid selectors:
        'valid':    no padding is applied, the output signal is starts window_len/2 after the signal
                    start and ends window_len/2 before the signal end
        'same'      the output signal has the same length as the input signal. the input signal is
                    padded with zeros at the start and end to achieve this.
        'mirror':   the output signal has the same length as the input signal. this is achieved by
                    mirroring the input signal at it's begin and end.
    :param mean_for_short_signals: return the arithmetic mean if the input signal is shorter than
        the window length.
    :return: the resulting 1d output signal.
    """
    if window_len % 2 == 0:
        raise ValueError("window length needs to be odd")

    if input_signal.shape[0] < window_len:
        if mean_for_short_signals:
            return np.mean(input_signal)
        raise ValueError("the signal needs to be longer than the window")

    # moving average
    if window_type == 'flat':
        c_filter = np.ones(window_len, dtype='float32')
    elif window_type == 'hanning':
        c_filter = np.hanning(window_len)
    elif window_type == 'hamming':
        c_filter = np.hamming(window_len)
    elif window_type == 'bartlett':
        c_filter = np.bartlett(window_len)
    elif window_type == 'blackman':
        c_filter = np.blackman(window_len)
    else:
        raise ValueError("unknown window type")

    c_filter = c_filter / c_filter.sum()

    filtered_signal = convolve_1d_boundaries(input_signal, c_filter, mode=mode)

    return filtered_signal


def convolve_1d_boundaries(
        input_signal: np.ndarray,
        inp_filter: np.ndarray,
        mode: str = 'valid') -> np.ndarray:
    """
    convolve a 1d input signal with a filter with the option to mirror the signal at the boundaries.
    :param input_signal:
    :param filter:
    :param mode:
    :return:
    """
    if mode == 'mirror':
        extended_signal = np.concatenate(
            (input_signal[int(inp_filter.shape[0] / 2):0:-1], input_signal,
             input_signal[-2:-int(inp_filter.shape[0] / 2) - 2:-1]))
        filtered_signal = np.convolve(
            inp_filter, extended_signal, mode='valid')
    else:
        filtered_signal = np.convolve(inp_filter, input_signal, mode=mode)

    return filtered_signal


def rolling_window_1d(a: np.ndarray, window_len: int) -> np.ndarray:
    """
    creates rolling windows for 1d signals in the 2nd dimensions.
    :param a:
    :param window_len:
    :return:
    """
    shape = a.shape[:-1] + (a.shape[-1] - window_len + 1, window_len)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def apply_rolling_fun_1d(
        input_signal: np.ndarray,
        fun: Callable,
        window_len,
        stepsize: int = 1) -> np.ndarray:
    """
    apply's a rolling function to 1d signals.
    :param input_signal:
    :param fun:
    :param window_len:
    :param stepsize:
    :return:
    """
    if window_len % 2 == 0:
        raise ValueError("window length needs to be odd")

    if input_signal.shape[0] < window_len:
        filtered_signal = fun(input_signal)
    else:
        signal_windows = rolling_window_1d(
            input_signal, window_len)[::stepsize, :]
        filtered_signal = np.apply_along_axis(fun, 1, signal_windows)

    return filtered_signal
