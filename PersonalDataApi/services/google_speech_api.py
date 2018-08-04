import speech_recognition as sr

#from pydub import AudioSegment

def transcribe_file(name):
    api_key_filename = r"C:\Users\William S. Hansen\source\api-keys\Free_Trial\PersonalData-9d8c53dee9bd.json"

    with open(api_key_filename) as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
 
    r = sr.Recognizer()

    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)

    return text

def convert_wav_to_flac(wavfilepath):
    
    tempflacfilepath = "testme.flac"
    #song = AudioSegment.from_wav(wavfilepath)
    #song.export(tempflacfilepath, format = "flac")

    return tempflacfilepath

