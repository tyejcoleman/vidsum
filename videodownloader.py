import youtube_dl
import sys
import os
import speech2text
import random
from google.cloud import storage



#from vidsum.code import subgen
#from subgen import convert_to_video, subtitle_generation
import subgen

sys.path.append(r'C:\Users\taiki\Desktop\Coding\VideoSummarizer_Subtitles\vidsum\code\subgen')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\taiki\PycharmProjects\vidsum\stelarvision-280712-133392ddf85b.json'


def download_video_srt(subs):
    r= random.randint(1,100000000)
    r=str(r)
    ydl_opts = {
        'format': 'best',
        'outtmpl':  r +'.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        'writesubtitles':True,
        'subtitleslangs':['en'],
        'write-auto-sub':True,
        'convert-subs':'srt',
        #'allsubtitles': True# Get all subtitles
    }

    movie_filename = r + '.mp4'
    subtitle_filename = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(subs), download=True)
        #print(result['requested_subtitles'])
        if result['requested_subtitles']==None:
            #subtitles were not provided
            print("No subtitles")
            #movie_filename = ydl.prepare_filename(result)
            subgen.convert_to_video(r)  # creates the audio file
            text = speech2text.mainprogram(audio_file_name= r + ".wav")  # audio variable is NOT the name
            response = subgen.subtitle_generation(response=text, bin_size=3)
            subtitle_filename = r + ".vtt"
            with open(subtitle_filename, "w+") as f:
                f.write(response)
            pass
        else:
            print("Video has subtitles")
            #movie_filename = ydl.prepare_filename(result)
            subtitle_info = result.get("requested_subtitles")
            #print(subtitle_info)
            subtitle_language = list(subtitle_info.keys())[0]
            subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
            subtitle_filename = r + "." + subtitle_language + "." + subtitle_ext
    return movie_filename, subtitle_filename

if __name__ == '__main__':

    link = input("What is the url to your Youtube video?")
    movie_filename, subtitle_filename = download_video_srt(link)


