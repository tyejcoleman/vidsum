import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\taiki\PycharmProjects\vidsum\stelarvision-280712-133392ddf85b.json'
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\denni\Downloads\Students\Tye\stelarvision-280712-133392ddf85b.json'

bucketname = "stelarvision2020"

from pydub import AudioSegment
from google.cloud import speech
from google.cloud import speech_v1
import wave
from google.cloud import storage

def mainprogram(audio_file_name):


    def stereo_to_mono(audio_file_name):
        sound = AudioSegment.from_wav(audio_file_name)
        sound = sound.set_channels(1)
        #sound.export(audio_file_name, format="wave")
        sound.export(audio_file_name, format="wav")



    def frame_rate_channel(audio_file_name):
        with wave.open(audio_file_name, 'rb') as wave_file:
            #frame_rate = wave_file.read.getframerate()
            frame_rate = wave_file.getframerate()
            #channels = wave_file.read.getnchannels()
            channels = wave_file.getnchannels()
            return frame_rate, channels


    def upload_blob(bucket_name, source_file_name, destination_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)


    def delete_blob(bucket_name, blob_name):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()


    def google_transcribe(audio_file_name):
        file_name = audio_file_name
        frame_rate, channels = frame_rate_channel(file_name)

        if channels > 1:
            stereo_to_mono(file_name)

        bucket_name = bucketname
        source_file_name = audio_file_name
        destination_blob_name = audio_file_name

        upload_blob(bucket_name, source_file_name, destination_blob_name)

        gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
        transcript = ''

        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            language_code='en-US',
            sample_rate_hertz=frame_rate,
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=10000)
        delete_blob(bucket_name, destination_blob_name)

        print(response)
        return response

    transcript = google_transcribe(audio_file_name) #this is the string
    return transcript
