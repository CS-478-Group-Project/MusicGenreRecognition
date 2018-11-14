import numpy as np
import librosa

class Andrew:

    def __init__(self):
        pass

    def __str__(self):
        return "Tempo, Total beats, Average beats" \
                ", MFCC mean, MFCC std, MFCC variance, MFCC delta mean, MFCC delta std, MFCC delta variance" \
                ", Chroma stft mean, Chroma stft std, chroma stft variance" \

    """
    :param full: full current song
    :param section: current section of the full song
    :param sr: the sampling rate: number of samples per second
    :type full: .wav file
    :type section: .wav file
    :type sr: integer
    :return: A list of each feature
    :rtype: list of integers
    """
    def extract(self, section, full, sr):
        self.section = section
        self.full = full
        self.sr = sr
        features = []
        features += self.tempo()
        features += self.MFCC()
        features += self.Chroma()
        return features

    """
    :return: The BPM, total beats and average beats
    :rtype: list of floats
    """
    def tempo(self):
        # tempo = estimated tempo, beat_frames = array of frame numbers corresponding to beat events
        tempo, beat_frames = librosa.beat.beat_track(y=self.section.astype(float), sr=float(self.sr))
        total_beats = np.sum(beat_frames)
        average_beats = np.mean(beat_frames)
        return [tempo, total_beats, average_beats]

    """
    :return: The MFCC features
    :rtype: list of floats

    An MFC is a representation of the shortterm power spectrum of a sound based on a 
    log power spectrums linear cosine transform on a nonlinear mel scale of frequency...
    """
    def MFCC(self):
        mfcc = librosa.feature.mfcc(y=self.section.astype(float), sr=float(self.sr))
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_mean = np.mean(mfcc)
        mfcc_std = np.std(mfcc)
        mfcc_var = np.var(mfcc)
        mfcc_delta_mean = np.mean(mfcc_delta)
        mfcc_delta_std = np.std(mfcc_delta)
        mfcc_delta_var = np.var(mfcc_delta)
        return [mfcc_mean, mfcc_std, mfcc_var, mfcc_delta_mean, mfcc_delta_std, mfcc_delta_var]

    def Chroma(self):
        chroma_stft = librosa.feature.chroma_stft(y=self.section.astype(float), sr=float(self.sr))
        chroma_stft_mean = np.mean(chroma_stft)
        chroma_stft_std = np.std(chroma_stft)
        chroma_stft_var = np.var(chroma_stft)
        return [chroma_stft_mean, chroma_stft_std, chroma_stft_var]