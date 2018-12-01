import numpy as np
import librosa as rosa

class Chandra:

    '''
    data members declared

    sample
    full_song
    sampling_rate
    '''

    def __init__(self):
        pass

    def __str__(self):
        return "spectral_centroid_mean, spectral_centroid_var, spectral_centroid_std" \
                ",flatness_mean, flatness_var, flatness_std" \
                ", contrast_mean, contrast_var, contrast_std"

    '''
    :param sample: the entire song broken into sample sizes, see driver for more details on sample size
    :param full_song: entire song extracted from .wav file
    :param sampling_rate: number of samples per second
    :type full_song: .wav file extracted list
    :type sample: .wav file extracted list
    :type sampling_rate: integer
    :return: A list features
    :rtype: list of integers
    '''
    def extract(self, sample, full_song, sampling_rate):
        self.sample = sample
        self.full_song = full_song
        self.sampling_rate = sampling_rate

        features = []
        features += self.spectral_centroid()
        features += self.flatness()
        features += self.spectral_contrast()
        return features

    '''
    :return: spectral centroid features
    :rtype: list of floats
    
    Each frame of a magnitude spectrogram is normalized and treated as a distribution over frequency bins, 
    from which the mean (centroid) is extracted per frame.
    '''
    def spectral_centroid(self):
        centr = rosa.feature.spectral_centroid(y=self.sample.astype(float), sr=self.sampling_rate)
        centr_mean = np.mean(centr)
        centr_var = np.var(centr)
        centr_std = np.std(centr)
        return centr_mean, centr_var, centr_std

    '''
    :return: flatness features
    :rtype: list of floats
    
    Spectral flatness (or tonality coefficient) is a measure to quantify how much noise-like a sound is, as opposed 
    to being tone-like [1]. A high spectral flatness (closer to 1.0) indicates the spectrum is similar to white noise. 
    It is often converted to decibel.
    '''
    def flatness(self):
        flatness = rosa.feature.spectral_flatness(y=self.sample.astype(float))
        flatness_mean = np.mean(flatness)
        flatness_var = np.var(flatness)
        flatness_std = np.std(flatness)
        return flatness_mean, flatness_var, flatness_std

    '''
    :return: spectral contrast features
    :rtype: list of floats
    
    each row of spectral contrast values corresponds to a given octave-based frequency. For perfect harmonic sounds these
    distances are constant, while for non-harmonic sounds the distances may vary.
    '''
    def spectral_contrast(self):
        contrast = rosa.feature.spectral_contrast(y=self.sample.astype(float), sr=self.sampling_rate)
        contrast_mean = np.mean(contrast)
        contrast_var = np.var(contrast)
        contrast_std = np.std(contrast)
        return contrast_mean, contrast_var, contrast_std


    '''
    descriptions of functionality taken from Features for Content-Based Audio Retrieval(Vienna University of Technology)
    and Librosa's feature description
    '''