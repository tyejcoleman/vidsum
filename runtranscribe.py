import transcribe

text = transcribe.mainprogram(audio_file_name="audio2.wav")

with open("Meeting12.8.txt", "w+") as f:
    f.write(text)

