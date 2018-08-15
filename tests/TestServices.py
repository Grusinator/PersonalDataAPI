import unittest

from PersonalDataApi.services.sound_processing_services import SoundClassifier

class Test_TestServices(unittest.TestCase):
    def test_sound_classification(self):

        sound_clasifier = SoundClassifier()
        predictions = sound_clasifier.classify_sound(r"C:\Users\William S. Hansen\source\repos\web\PersonalDataApi\tests\testdata\sample.wav")

if __name__ == '__main__':
    unittest.main()
