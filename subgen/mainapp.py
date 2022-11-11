import videodownloader
import vidsum

link = input("What is the url to your Youtube video?")

movie_filename, subtitle_filename = videodownloader.download_video_srt(link)

vidsum.get_summary(movie_filename, subtitle_filename)