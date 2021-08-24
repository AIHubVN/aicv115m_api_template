import numpy as np
import pandas as pd
from scipy.io import wavfile

from modules.example_feature import Features


def read_wav_file(filepath):
    sample_rate, waveform = wavfile.read(filepath)
    if waveform.ndim > 1:
        waveform = waveform[:, 0]
    return sample_rate, waveform


def make_acoustic_feat(X):
    # Class that contains the feature computation functions
    FREQ_CUTS = [(0, 200), (300, 425), (500, 650), (950, 1150),
                 (1400, 1800), (2300, 2400), (2850, 2950), (3800, 3900)]
    extractor = Features(FREQ_CUTS)
    features_fct_list = ['EEPD', 'ZCR', 'RMSP', 'DF', 'spectral_features',
                         'SF_SSTD', 'SSL_SD', 'MFCC', 'CF', 'LGTH', 'PSD']

    feat = []
    for filename in X.file_path.values:
        feature_values_vec = []
        d = read_wav_file(filename)

        for feature in features_fct_list:
            feature_values, feature_names = getattr(extractor, feature)(d)
            for value in feature_values:
                if isinstance(value, np.ndarray):
                    feature_values_vec.append(value[0])
                else:
                    feature_values_vec.append(value)

        feature_values_vec = np.array(feature_values_vec)
        feat.append(feature_values_vec)
    feat = np.array(feat)
    feat = np.nan_to_num(feat)
    feat = np.clip(feat, -np.finfo(np.float32).max, np.finfo(np.float32).max)

    return feat
