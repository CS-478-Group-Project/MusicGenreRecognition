import numpy as np
from pyAudioAnalysis import audioFeatureExtraction, audioBasicIO
from scipy import signal
from scipy.signal import butter, lfilter
from scipy.signal import freqz
from scipy.fftpack import fft,fftfreq
import librosa


class Gibson:
    def __init__(self):
        return

    def __str__(self):
        return "Zero Crossing Rate, Short Time Energy, Spectral Roll Off, Entropy, Spectral Flux, " \
                "b1, b2, b3, b4, b5, b6, b7"

    def extract(self, section, full_song, sampling_rate):
        self.section = section
        self.full_song = full_song
        self.sampling_rate = sampling_rate

        return [1,2,3]


    def zcr():
        return

    def short_time_energy():
        return

    def spectral_roll_off():
        return

    def entropy():
        return

    def spectral_flux():
        return

    def frequency_bins():
        return
