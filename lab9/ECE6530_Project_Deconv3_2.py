import matplotlib.pyplot as plt  ## Libary used for displaying plots and formatting plots
import numpy as np  ## Library used for arrays functions, mathematical functions, etc.

# from matplotlib import cm
# import math
# import cmath
# from scipy.fft import fft,ifft
# import sys
np.set_printoptions(threshold=np.inf)
from scipy.io import wavfile
from scipy.io.wavfile import write
import winsound

# import unicodedata


def zeropad(x, y):
    xpad = np.zeros((len(x) + 2 * len(y) - 2), dtype=np.complex128)
    ylength = len(y) - 1
    for ii in range(0, len(x)):
        xpad[ii + ylength] = x[ii]
    return xpad


def convo(x, b):
    bk = b
    x_n = zeropad(x, bk)
    y_padd = np.zeros(len(x_n), dtype=np.complex128)
    y_n = np.zeros(len(x), dtype=np.complex128)
    b_ind = len(b) - 1
    for n in range(0, len(x_n)):
        for k in range(0, len(bk)):
            y_padd[n] += bk[k] * x_n[n - k]

    for ii in range(0, len(x)):
        y_n[ii] = y_padd[ii + b_ind]
    return y_n


def firconv(p, x_n, bk):
    w_n = convo(x_n, bk)
    n = np.arange(0, 100)
    if p == 0:
        print(x_n)
        print(w_n)
        print("3.1 a) I am unsure of what the effect of these filter coefficients is")
        print(
            "3.1 b) The length of the filtered signal is the length of x_n added to the length of bk minus 1."
        )
        print(
            "The nonzero portion of w_n is one value longer than x_n as well, producing 11 vales rather than 10."
        )
        print("length of x_n is ", len(x_n), "samples")
        print("length of w_n is ", len(w_n), "samples")
        fig, axs = plt.subplots(2, 1, figsize=(12, 12))
        axs[0].stem(n[0:75], x_n[0:75], markerfmt="red")
        axs[0].title.set_text("x(n)")
        axs[0].grid()
        axs[0].set_ylabel("x(n)")
        axs[0].set_xlabel("Samples")
        axs[1].stem(n[0:75], w_n[0:75])
        axs[1].title.set_text("w(n)")
        axs[1].set_ylabel("w(n)")
        axs[1].set_xlabel("samples")
        axs[1].grid()
        plt.show()
    return w_n


def restor(w_n, x_n):
    M = 99
    r = 0.9
    y_n = np.zeros(len(w_n), dtype=np.complex128)

    for n in range(0, len(w_n)):
        for l in range(0, M):
            y_n[n] += (r**l) * w_n[n - l]
    return y_n


def restor_plot(w_n, x_n):
    M = 22
    r = 0.9
    n_val = np.arange(len(w_n))
    y_n = np.zeros(len(w_n), dtype=np.complex128)
    y_err = np.zeros(len(w_n), dtype=np.complex128)

    for n in range(0, len(w_n)):
        for l in range(0, M):
            y_n[n] += (r**l) * w_n[n - l]
    for ii in range(0, len(x_n)):
        y_err[ii] = y_n[ii] - x_n[ii]

    fig, axs = plt.subplots(4, 1, figsize=(12, 12))
    axs[0].stem(n_val, x_n)
    axs[0].grid()
    axs[0].set_ylabel("x(n)")
    axs[0].set_xlabel("Samples")
    axs[1].stem(n_val, w_n)
    axs[1].grid()
    axs[1].set_ylabel("w(n)")
    axs[1].set_xlabel("Samples")
    axs[2].stem(n_val, y_n)
    axs[2].set_ylabel("y(n)")
    axs[2].set_xlabel("samples")
    axs[2].grid()
    axs[3].stem(n_val[0:50], y_err[0:50])
    axs[3].set_ylabel("error y(n) - x(n)")
    axs[3].set_xlabel("samples")
    axs[3].grid()

    plt.show()


def open_wav(title):
    fs, data = wavfile.read(title)
    # print(fs)
    # print(data)
    return data, fs


def play_wav(name, fs):
    winsound.PlaySound(name, winsound.SND_FILENAME)


def new_wav(data, rate):
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    write("test.wav", rate, scaled)


def WorstCaseError(w_n, x_n):
    y_n = restor(w_n, x_n)
    n_val = np.arange(len(w_n))
    y_err = np.zeros(len(w_n), dtype=np.complex128)
    for ii in range(0, len(x_n)):
        y_err[ii] = y_n[ii] - x_n[ii]
    max_error = round(max(abs(y_err[0:50])), 4)
    print("The worst case error for y(n) and x(n) is", max_error)
    print(
        "The plot of the error and the worst case error tells me that the restoration of the signal x(n)"
    )
    print(
        "still needs to be improved. This improvement could be done by increasing the 'M' value in the"
    )
    print(
        "restoration filter. This would cause less error. Changing M to nearly 80 causes a difference of around 0.0559."
    )
    print(
        "Changing the value of M to nearly the length of x(n) causes the error to be nearly nonexistent."
    )
    fig, axs = plt.subplots(3, 1, figsize=(12, 12))
    axs[0].stem(n_val, x_n)
    axs[0].grid()
    axs[0].set_ylabel("x(n)")
    axs[0].set_xlabel("Samples")
    axs[1].stem(n_val, y_n)
    axs[1].set_ylabel("y(n)")
    axs[1].set_xlabel("samples")
    axs[1].grid()
    axs[2].stem(n_val[0:50], y_err[0:50])
    axs[2].set_ylabel("error y(n) - x(n)")
    axs[2].set_xlabel("samples")
    axs[2].grid()
    plt.show()


def echoFIR(x_n, td, fs, echo_amp):
    samp_delay = int(fs * td)
    bk = np.zeros(samp_delay, dtype=float)
    bk[0] = 1
    bk[samp_delay - 1] = echo_amp
    # print(samp_delay)
    # print(len(bk))
    echo = np.convolve(x_n, bk)
    return echo


def print_echo(x_n, td, fs, echo_amp):
    samp_delay = int(fs * td)
    bk = np.zeros(samp_delay, dtype=float)
    bk[0] = 1
    bk[samp_delay - 1] = echo_amp
    # print(samp_delay)
    # print(len(bk))
    echo = np.convolve(x_n, bk)
    n_samp = np.arange(len(echo))
    n_val = np.arange(len(x_n))
    fig, axs = plt.subplots(2, 1, figsize=(12, 12))
    axs[0].stem(n_val, x_n)
    axs[0].grid()
    axs[0].set_ylabel("x(n)")
    axs[0].set_xlabel("Samples")
    axs[1].stem(n_samp, echo)
    axs[1].set_ylabel("y(n)")
    axs[1].set_xlabel("samples")
    axs[1].grid()
    plt.show()


def main():
    x_n = 256 * ((np.arange(0, 100, 1) % 50) < 10)
    bk = [1, -0.9]
    # orig_wav = 'pluck_55hz.wav'    ## generated on Audacity
    orig_wav = "boing_x.wav"  ##downloaded free at https://www.wavsource.com/snds_2020-10-01_3728627494378403/sfx/boing_x.wav
    # w_n = firconv(1,x_n,bk)    ##change to 'fircon(0,x_n,bk)' if graphs should be plotted
    # restor_plot(w_n,x_n)
    # WorstCaseError(w_n,x_n)
    fs = 8000
    td = 0.2
    echo_amp = 0.5  ##original specified in lab is 0.9
    # echo = echoFIR(x_n,td,fs)

    data_orig, fs = open_wav(orig_wav)
    # echo_data = print_echo(data_orig,td,fs,echo_amp)
    echo_data = echoFIR(data_orig, td, fs, echo_amp)
    # play_wav(orig_wav,fs)
    new_wav(echo_data, fs)
    play_wav("test.wav", fs)


if __name__ == "__main__":
    main()