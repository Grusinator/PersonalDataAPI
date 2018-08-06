import speech_recognition as sr
import os

#from pydub import AudioSegment

def get_google_api_key():
    api_key_filename = r"C:\Users\William S. Hansen\source\api-keys\Free_Trial\PersonalData-9d8c53dee9bd.json"

    #try to read it local
    try:
        with open(api_key_filename) as f:
            GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
    except:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = os.environ['GOOGLE_CLOUD_SPEECH_CREDENTIALS']

    return GOOGLE_CLOUD_SPEECH_CREDENTIALS

def transcribe_file(audiofile, language="da-DK"):

    GOOGLE_CLOUD_SPEECH_CREDENTIALS = get_google_api_key()

    r = sr.Recognizer()

    with sr.AudioFile(audiofile) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, language=language, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)

    return text

def convert_wav_to_flac(wavfilepath):
    
    tempflacfilepath = "testme.flac"
    #song = AudioSegment.from_wav(wavfilepath)
    #song.export(tempflacfilepath, format = "flac")

    return tempflacfilepath

