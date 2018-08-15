import numpy as np
from scipy.io import wavfile

from PersonalDataApi.services.sound_classification.processor import WavProcessor, format_predictions

class SoundClassifier:
    proc = None
    def __init__(self):
        self.proc = WavProcessor()

    def classify_sound(self, wav_file):
        sr, data = wavfile.read(wav_file)
        if data.dtype != np.int16:
            raise TypeError('Bad sample type: %r' % data.dtype)
    
        predictions = self.proc.get_predictions(sr, data)

        return predictions
