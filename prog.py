import os
import sys
from pytube import Search
from pytube import YouTube
import moviepy.editor as mp
import glob
import shutil


def download_videos(n, x):
    # Create a directory to store the videos
    if not os.path.exists("static/files/"+x):
        os.mkdir("static/files/"+x)

    # Search for videos of the singer
    query = x + " music videos"
    s = Search(query)
    searchResults = {}
    i = 0
    for v in s.results:
        if i < n and v.length < 600:
            try:
                searchResults[v.title] = v.watch_url
                youtubeObject = YouTube(v.watch_url)
                youtubeObject = youtubeObject.streams.get_highest_resolution().download(
                    output_path='static/files/'+x, filename=f"video{i+1}.mp4")
                print(f"Downloaded video {i + 1}: {v.title}")
                i = i+1
            except:
                print("error occured")


def convertToAudio(duration, n, x):
    if not os.path.exists("static/files/Audios"):
        os.mkdir("static/files/Audios")

    for i in range(n):
        clip = mp.VideoFileClip(
            f"static/files/{x}/video{i+1}.mp4").subclip(0, duration)
        clip.audio.write_audiofile(f"static/files/Audios/audio{i+1}.mp3")


def makeMashup(n, output):
    audio_clips = [mp.AudioFileClip(
        f"static/files/Audios/audio{i+1}.mp3") for i in range(0, n)]
    final_clip = mp.concatenate_audioclips(audio_clips)
    final_clip.write_audiofile(output)


# download_videos(3, "Taylor Swift")
# convertToAudio(20, 3)
# makeMashup(3)

def generateMashup(singer, vid, duration):
    download_videos(int(vid), singer)
    convertToAudio(int(duration), int(vid), singer)
    makeMashup(int(vid), "static/files/result.mp3")
    if os.path.exists("static/files/Audios"):
        shutil.rmtree(r"static/files/Audios", ignore_errors=True)
        print("Deleted directory successfully")


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print("ERROR: Number of arguments are not correct")
        exit()

    generateMashup(sys.argv[1], sys.argv[2], sys.argv[3])
    # download_videos(int(sys.argv[2]), sys.argv[1])
    # convertToAudio(int(sys.argv[3]), int(sys.argv[2]))
    # makeMashup(int(sys.argv[2]), sys.argv[4])
