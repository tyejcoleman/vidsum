import datetime
import os
import srt
from moviepy.editor import VideoFileClip
import speech2text
import youtube_dl
import sys
import random

def convert_to_video(r):
    clip = VideoFileClip(r + ".mp4")
    clip.audio.write_audiofile(r + ".wav")
    audio_file = open(r + ".wav")
    return audio_file

def subtitle_generation(response, bin_size=3):
    transcriptions = []
    index = 0
    bin_size = response.results[0].alternatives[0].words[-1].end_time.seconds - response.results[0].alternatives[0].words[0].start_time.seconds
    for result in response.results:
        try:
            if result.alternatives[0].words[0].start_time.seconds:
                # bin start -> for first word of result
                start_sec = result.alternatives[0].words[0].start_time.seconds
                start_microsec = result.alternatives[0].words[0].start_time.microseconds * 0.001
            else:
                # bin start -> For First word of response
                start_sec = 0
                start_microsec = 0
            end_sec = start_sec + bin_size  # bin end sec

            # for last word of result
            last_word_end_sec = result.alternatives[0].words[-1].end_time.seconds
            last_word_end_microsec = result.alternatives[0].words[-1].end_time.microseconds * 0.001

            # bin transcript
            transcript = result.alternatives[0].words[0].word

            index += 1  # subtitle index

            for i in range(len(result.alternatives[0].words) - 1):
                try:
                    word = result.alternatives[0].words[i + 1].word
                    word_start_sec = result.alternatives[0].words[i + 1].start_time.seconds
                    word_start_microsec = result.alternatives[0].words[
                                              i + 1].start_time.microseconds * 0.001  # 0.001 to convert nana -> micro
                    word_end_sec = result.alternatives[0].words[i + 1].end_time.seconds

                    if word_end_sec < end_sec:
                        transcript = transcript + " " + word
                    else:
                        previous_word_end_sec = result.alternatives[0].words[i].end_time.seconds
                        previous_word_end_microsec = result.alternatives[0].words[i].end_time.microseconds * 0.001

                        # append bin transcript
                        transcriptions.append(srt.Subtitle(index, datetime.timedelta(0, start_sec, start_microsec),
                                                           datetime.timedelta(0, previous_word_end_sec,
                                                                              previous_word_end_microsec), transcript))

                        # reset bin parameters
                        start_sec = word_start_sec
                        start_microsec = word_start_microsec
                        end_sec = start_sec + bin_size
                        transcript = result.alternatives[0].words[i + 1].word

                        index += 1
                    bin_size = result.alternatives[0].words[-1].end_time.seconds - result.alternatives[0].words[0].start_time.seconds
                except IndexError:
                    bin_size = result.alternatives[0].words[-1].end_time.seconds - result.alternatives[0].words[0].start_time.seconds
                    pass
            # append transcript of last transcript in bin
            transcriptions.append(srt.Subtitle(index, datetime.timedelta(0, start_sec, start_microsec),
                                               datetime.timedelta(0, last_word_end_sec, last_word_end_microsec),
                                               transcript))
            index += 1

        except IndexError:
            pass

    # turn transcription list into subtitles
    subtitles = srt.compose(transcriptions)
    return subtitles
