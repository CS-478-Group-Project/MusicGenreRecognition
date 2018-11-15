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
    # Define some cool constants that will be used during feature extraction
    window_size = 8192 # Around about 0.2s window size, given sampling rate of 48000
    overlaps_per_window = 4 # 0.05s overlap



    def __init__(self):
        return

    # We may not be doing short time energy anymore...
    def __str__(self):
        return "Mean ZCR, ZCR StdDev, Spectral Roll Off, Spectral Entropy, Mean Spectral Flux, " \
                "b1, b2, b3, b4, b5, b6, Band Ratio StdDev, Band Energy StdDev"

    def extract(self, section, full_song, sampling_rate):
        self.section = section
        self.full_song = full_song
        self.sampling_rate = sampling_rate
        self.bands = [                  # Bands for rough instrument representation
                        [0, 200],       # b1
                        [200, 500],     # b2
                        [300, 700],     # b3
                        [700, 1600],    # b4
                        [1500, 3200],   # b5
                        [3200, int(sampling_rate / 2)]  # b6
        ]

        # Convert sample to frequency domain for cool stuff :)
        self.section_fft = abs(fft(section))

        # hasattr(x, '__iter__') might be useful

        features = []

        features.extend(list(self.zcr()))           # Returns a tuple, must extend
        features.append(self.spectral_roll_off())   # Append roll off
        features.append(self.spectral_entropy())    # Append spectral entropy
        features.append(self.spectral_flux())       # Append mean spectral flux

        band_energy_ratios, band_energy_sums, band_ratio_stdev, band_sum_stdev = self.frequency_bins()
        features.extend(band_energy_ratios)
        features.append(band_ratio_stdev)
        features.append(band_sum_stdev)

        assert (len(str(self).split(',')) == len(features)) # Enforce feature length correctly

        return features


    def zcr(self):
        # Compute the zero crossing rate for each window
        zcr_values = [audioFeatureExtraction.stZCR(np.array(window)) for window in overlapped_window(self.section, self.window_size, self.overlaps_per_window)]
        # Return the mean and standard deviation for our measured zcr values
        return mean(zcr_values), stdev(zcr_values)

    def short_time_energy(self):
        raise NotImplementedError("Short time energy not implemented!")
        return

    def spectral_roll_off(self):
        return audioFeatureExtraction.stSpectralRollOff(self.section, .5, self.sampling_rate)

    def spectral_entropy(self):
        # Use the library's spectral energy computation
        return audioFeatureExtraction.stSpectralEntropy(self.section_fft)

    def spectral_flux(self):
        # Computes the average spectral flux given a sample
        flux_values = [audioFeatureExtraction.stSpectralFlux(self.section_fft[i + 1], self.section_fft[i]) for i in range(len(self.section_fft) - 1)]

        # Returns the mean spectral flux across all frames
        return mean(flux_values)

    # Something to note, is that the last bin seems to (almost) always be 0
    # We can get rid of that last bin if it turns out to not give us any info
    def frequency_bins(self):
        band_energy_ratios = [[] for band in self.bands]
        band_energy_sums = [[] for band in self.bands]

        for window in overlapped_window(self.section, self.window_size, self.overlaps_per_window):
            # total_window_energy = audioFeatureExtraction.stEnergy(np.array(window))

            # Convert to frequency domain
            fft_window = abs(fft(window, self.sampling_rate))
            fft_window = fft_window[:int(len(window) / 2)]
            window_sum = sum(fft_window)

            # Create our frequency bins
            freq_bin_data = []
            for band in self.bands:
                current_bin = np.zeros(fft_window.shape[0])                 # Start with all zeros
                current_bin[band[0]:band[1]] = fft_window[band[0]:band[1]]  # Copy a band of data
                freq_bin_data.append(current_bin)                           # Add to our list

            # For each frequency bin, extract its energy ratio and total energy
            for i in range(len(freq_bin_data)):
                current_sum = sum(freq_bin_data[i])
                band_energy_ratios[i].append(current_sum / window_sum)
                band_energy_sums[i].append(current_sum)

        # Average the ratio data!
        band_energy_ratios = [mean(band_ratio) for band_ratio in band_energy_ratios]
        band_energy_sums = [mean(band_sum) for band_sum in band_energy_sums]

        # Compute standard deviation b/c why not
        band_ratio_stdev = stdev(band_energy_ratios)
        band_sum_stdev = stdev(band_energy_sums)

        # Return our stuff?
        return band_energy_ratios, band_energy_sums, band_ratio_stdev, band_sum_stdev
