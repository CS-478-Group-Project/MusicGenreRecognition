import numpy as np
import librosa

class Jacob:
    def __init__(self):
        pass

    def __str__(self):
        return "RMSE, RMSE Variance, RMSE STD" \
                ", Median Spectral Bandwidth, Spectral Bandwidth Variance, Spectral Bandwidth STD"

    def rmse(self, section, frame_length):
        unframed_rmse = librosa.feature.rmse(y=section.astype(float), frame_length=frame_length)
        rmse = unframed_rmse[0,0]
        framed_rmse = librosa.feature.rmse(y=section.astype(float))
        rmse_variance = np.var(framed_rmse)
        rmse_std = np.std(framed_rmse)
        return [rmse, rmse_variance, rmse_std]

    def bandwidth(self, section, sr):
        framed_bandwidth = librosa.feature.spectral_bandwidth(y=section.astype(float), sr=float(sr))
        median_bandwidth = np.median(framed_bandwidth)
        bandwidth_variance = np.var(framed_bandwidth)
        bandwidth_std = np.std(framed_bandwidth)
        return [median_bandwidth, bandwidth_variance, bandwidth_std]

    def extract(self, section, full, sr):
        frame_length = section.shape[0]
        features = []
        features += self.rmse(section, frame_length)
        features += self.bandwidth(section, sr)
        return features