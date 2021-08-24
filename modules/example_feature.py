import librosa
import numpy as np
from scipy import signal
from scipy.integrate import simps


# Class that contains the feature computation functions
class Features:

    def __init__(self, FREQ_CUTS):
        self.FREQ_CUTS = FREQ_CUTS  # list of Frequency Bands for the PSD
        self.n_PSD = len(FREQ_CUTS)

    def fft(self, data):
        """
        Compute the spectrum using FFT
        """
        fs, cough = data
        fftdata = np.fft.rfft(cough)
        return fftdata

    # Envelope Energy Peak Detection
    def EEPD(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of the feature
        names = []
        fs, cough = data
        fNyq = fs/2
        nPeaks = []
        freq_step = 50
        for fcl in range(50, 1000, freq_step):
            names = names + ['EEPD'+str(fcl)+'_'+str(fcl+freq_step)]
            fc = [fcl/fNyq, (fcl+50)/fNyq]
            b, a = signal.butter(1, fc, btype='bandpass')
            bpFilt = signal.filtfilt(b, a, cough)
            b, a = signal.butter(2, 10/fNyq, btype='lowpass')
            eed = signal.filtfilt(b, a, bpFilt**2)
            eed = eed/np.max(eed+1e-17)
            peaks, _ = signal.find_peaks(eed)
            nPeaks.append(peaks.shape[0])
        return np.array(nPeaks), names

    # Zero Crossing Rate
    def ZCR(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of the feature
        names = ['Zero_Crossing_Rate']
        fs, cough = data
        ZCR = (np.sum(np.multiply(cough[0:-1], cough[1:]) < 0)/(len(cough)-1))
        return np.ones((1, 1))*ZCR, names

    # RMS Power
    def RMSP(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of the feature
        names = ['RMS_Power']
        fs, cough = data
        RMS = np.sqrt(np.mean(np.square(cough)))
        return np.ones((1, 1))*RMS, names

    # Dominant Frequency
    def DF(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of the feature
        names = ['Dominant_Freq']
        fs, cough = data
        cough_fortan = np.asfortranarray(cough)
        freqs, psd = signal.welch(cough_fortan)
        DF = freqs[np.argmax(psd)]
        return np.ones((1, 1))*DF, names

    def spectral_features(self, data):
        names = ["Spectral_Centroid", "Spectral_Rolloff", "Spectral_Spread",
                 "Spectral_Skewness", "Spectral_Kurtosis", "Spectral_Bandwidth"]
        fs, x = data
        # magnitudes of positive frequencies
        magnitudes = np.abs(np.fft.rfft(x))
        length = len(x)
        freqs = np.abs(np.fft.fftfreq(length, 1.0/fs)
                       [:length//2+1])  # positive frequencies
        sum_mag = np.sum(magnitudes)

        # spectral centroid = weighted mean of frequencies wrt FFT value at each frequency
        spec_centroid = np.sum(magnitudes*freqs) / (sum_mag + 1e-12)

        # spectral roloff = frequency below which 95% of signal energy lies
        cumsum_mag = np.cumsum(magnitudes)
        spec_rolloff = np.min(np.where(cumsum_mag >= 0.95*sum_mag)[0])

        # spectral spread = weighted standard deviation of frequencies wrt FFT value
        spec_spread = np.sqrt(
            np.sum(((freqs-spec_centroid)**2)*magnitudes) / (sum_mag + 1e-12))

        # spectral skewness = distribution of the spectrum around its mean
        spec_skewness = np.sum(((freqs-spec_centroid)**3)
                               * magnitudes) / ((spec_spread**3)*sum_mag + 1e-12)

        # spectral kurtosis = flatness of spectrum around its mean
        spec_kurtosis = np.sum(((freqs-spec_centroid)**4)
                               * magnitudes) / ((spec_spread**4)*sum_mag + 1e-12)

        # spectral bandwidth = weighted spectral standard deviation
        p = 2
        spec_bandwidth = (np.sum(magnitudes*(freqs-spec_centroid)**p))**(1/p)

        return np.array([spec_centroid, spec_rolloff, spec_spread, spec_skewness, spec_kurtosis, spec_bandwidth]), names

    # Spectral Flatness and spectral standard deviation
    def SF_SSTD(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of the feature
        names = ['Spectral_Flatness', 'Spectral_StDev']
        fs, sig = data
        nperseg = min(900, len(sig))
        noverlap = min(600, int(nperseg/2))
        freqs, psd = signal.welch(sig, fs, nperseg=nperseg, noverlap=noverlap)
        psd_len = len(psd)
        gmean = np.exp((1/psd_len)*np.sum(np.log(psd + 1e-17)))
        amean = (1/psd_len)*np.sum(psd)
        SF = gmean/(amean + 1e-10)
        SSTD = np.std(psd)
        return np.array([SF, SSTD]), names

    # Spectral Slope and Spectral Decrease
    def SSL_SD(self, data):
        names = ['Spectral_Slope', 'Spectral_Decrease']
        b1 = 0
        b2 = 8000

        Fs, x = data
        s = np.absolute(np.fft.fft(x))
        s = s[:s.shape[0]//2]
        muS = np.mean(s)
        f = np.linspace(0, Fs/2, s.shape[0])
        muF = np.mean(f)

        bidx = np.where(np.logical_and(b1 <= f, f <= b2))
        slope = np.sum(((f-muF)*(s-muS))[bidx]) / np.sum((f[bidx]-muF)**2)

        k = bidx[0][1:]
        sb1 = s[bidx[0][0]]
        decrease = np.sum((s[k]-sb1)/(f[k]-1+1e-17)) / (np.sum(s[k]) + 1e-17)

        return np.array([slope, decrease]), names

    # MFCC
    def MFCC(self, data):
        # data: wav file of segment; fs, signal = wavfile.read(file)
        # output: value of MFCC coefficient
        names = []
        names_mean = []
        names_std = []
        fs, cough = data
        cough = cough.astype('float')
        n_mfcc = 13
        for i in range(n_mfcc):
            names_mean = names_mean + ['MFCC_mean'+str(i)]
            names_std = names_std + ['MFCC_std'+str(i)]
        names = names_mean + names_std
        mfcc = librosa.feature.mfcc(y=cough, sr=fs, n_mfcc=n_mfcc)
        mfcc_mean = mfcc.mean(axis=1)
        mfcc_std = mfcc.std(axis=1)
        mfcc = np.append(mfcc_mean, mfcc_std)
        return mfcc, names

    # Crest Factor
    def CF(self, data):
        """
        Compute the crest factor of the signal
        """
        fs, cough = data
        peak = np.amax(np.absolute(cough))
        RMS = np.sqrt(np.mean(np.square(cough)))
        return np.ones((1, 1))*peak/(RMS + 1e-10), ['Crest_Factor']

    def LGTH(self, data):
        "Compute the length of the segment in seconds"
        fs, cough = data
        return np.ones((1, 1))*(len(cough)/fs), ['Cough_Length']

    # Power spectral Density
    def PSD(self, data):
        feat = []
        fs, sig = data
        nperseg = min(900, len(sig))
        noverlap = min(600, int(nperseg/2))
        freqs, psd = signal.welch(sig, fs, nperseg=nperseg, noverlap=noverlap)
        dx_freq = freqs[1]-freqs[0]
        total_power = simps(psd, dx=dx_freq)
        for lf, hf in self.FREQ_CUTS:
            idx_band = np.logical_and(freqs >= lf, freqs <= hf)
            band_power = simps(psd[idx_band], dx=dx_freq)
            feat.append(band_power/(total_power + 1e-12))
        feat = np.array(feat)
        feat_names = [f'PSD_{lf}-{hf}' for lf, hf in self.FREQ_CUTS]
        return feat, feat_names
