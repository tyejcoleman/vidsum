import  io
from google.cloud import speech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\taiki\PycharmProjects\vidsum\stelarvision-280712-133392ddf85b.json'


def transcribe_file(content):
    """Transcribe the given audio file asynchronously."""

    client = speech.SpeechClient()



    """
     Note that transcription is limited to 60 seconds audio.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    #for result in response.results:
        # The first alternative is the most likely one for this portion.
       # print(u"Transcript: {}".format(result.alternatives[0].transcript))
      #  print("Confidence: {}".format(result.alternatives[0].confidence))

if __name__ == '__main__':
    with io.open('audio.mp3', "rb") as audio_file:
        content = audio_file.read()
    transcribe_file(content)