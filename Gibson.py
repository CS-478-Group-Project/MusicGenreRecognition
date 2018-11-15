import numpy as np
from pyAudioAnalysis import audioFeatureExtraction, audioBasicIO
from scipy import signal
from scipy.signal import butter, lfilter
from scipy.signal import freqz
from scipy.fftpack import fft,fftfreq
import librosa

from windowing import overlapped_window
from statistics import mean, stdev


class Gibson:
    window_size = 8192 # Around about 0.2s window size
    overlaps_per_window = 4 # 0.05s overlap



    def __init__(self):
        return

    # We may not be doing short time energy anymore...
    def __str__(self):
        return "Zero Crossing Rate, Short Time Energy, Spectral Roll Off, Entropy, Spectral Flux, " \
                "b1, b2, b3, b4, b5, b6, b7"

    def extract(self, section, full_song, sampling_rate):
        self.section = section
        self.full_song = full_song
        self.sampling_rate = sampling_rate

        # Convert sample to frequency domain for cool stuff :)
        self.section_fft = abs(fft(section))

        # hasattr(x, '__iter__') might be useful

        features = []

        features.append(self.zcr())


        assert (len(str(self).split(',')) == len(features)) # Enforce feature length correctly

        return features


    def zcr(self):
        # Compute the zero crossing rate for each window
        zcr_values = [audioFeatureExtraction.stZCR(np.array(window)) for window in overlapped_window(self.section, self.window_size, self.overlaps_per_window)]
        # Return the mean and standard deviation for our measured zcr values
        return mean(zcr_values), stdev(zcr_values)

    def short_time_energy(self):
        return

    def spectral_roll_off(self):
        return audioFeatureExtraction.stSpectralRollOff(self.section, .5, self.sample_rate)
        return

    def spectral_entropy(self):
        # Use the library's spectral energy computation
        return audioFeatureExtraction.stSpectralEntropy(self.section_fft)

    def spectral_flux(self):
        # Computes the average spectral flux given a sample
        flux_values = [audioFeatureExtraction.stSpectralFlux(self.section_fft[i + 1], self.section_fft[i]) for i in range(len(self.section_fft) - 1)]

        # Returns the mean spectral flux across all frames
        return mean(flux_values)

    def frequency_bins(self):
        return
