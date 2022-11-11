from flask import Flask, render_template, request
import videodownloader
from subprocess import run, PIPE
import sys


app = Flask(__name__)

@app.route('/')
def video():
    return render_template('video.html')

@app.route('/', methods=['POST'])
def getvalue():
    link = request.form['link']
    movie, subtitle = videodownloader.download_video_srt(link)
    print("done")
    return render_template()
if __name__ == '__main__':
    app.run(debug=True)