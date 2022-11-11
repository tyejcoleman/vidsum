import speech2text
import youtube_dl
import sys
sys.path.append("/users/taiki/appdata/local/packages/pythonsoftwarefoundation.python.3.8_qbz5n2kfra8p0/localcache/local-packages/python38/site-packages")

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': "sample_music" + '.%(ext)s',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
         'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
}

videolink = input("Copy video link: ")

ydl = youtube_dl.YoutubeDL(ydl_opts)
info_dict = ydl.extract_info(videolink, download=True)




def run():
    speech2text.mainprogram()


run()

def keywords():
    with open("sample_music.txt", 'r') as f:
        text = f.read()


    search_words = set([input("Enter keyword: ")])


    for sentence in text.split("."):
        words_in_sentence = set(sentence.split())
        if words_in_sentence.intersection(search_words) :
            print(sentence)
keywords()