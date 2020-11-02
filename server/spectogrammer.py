import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def file_to_spectogram(filename):
    audio, sr = librosa.load(filename)
    D = np.abs(librosa.stft(audio))**2
    spectogram = librosa.feature.melspectrogram(y=audio, sr=sr, S=D)
    return spectogram, sr


def spectogram_to_db(S):
    return librosa.power_to_db(S, ref=np.max)


def save_spectogram(S, sr, filename):
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S, x_axis='time',
                                   y_axis='mel', sr=sr,
                                   fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    plt.savefig(filename+'_spectogram.png')
