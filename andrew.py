import numpy as np
import librosa

class Andrew:

    def __init__(self):
        pass

    def __str__(self):
        return "Tempo, Total Beats, Average Beats, MFCC1"

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
    def extract(self, full, section, sr):
        self.full = full
        self.section = section
        self.sr = sr

    """
    :return: The BPM, total beats and average beats
    :rtype: list of floats
    """
    def tempo(self):
        # tempo = estimated tempo, beat_frames = array of frame numbers corresponding to beat events
        tempo, beat_frames = librosa.beat.beat_track(y=self.section, sr=self.sr)
        total_beats = np.sum(beat_frames)
        average_beats = np.mean(beat_frames)
        return [tempo, total_beats, average_beats]

    """
    :return: The MFCC features
    :rtype: list of floats
    """
    def MFCC(self):
        pass