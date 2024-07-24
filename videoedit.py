from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import os

def cropvideo(video, startingtime, endingtime, id):
    try:
        croppedvideo = video.subclip(startingtime, endingtime)
        output_path = f'OutputFiles/{id}.mp4'
        croppedvideo.write_videofile(output_path, codec='libx264', audio_codec='aac')
        croppedvideo.close()
    except Exception as e:
        print(f"Error cropping video: {e}")

def speedupvideo(video, speed, id):
    try:
        spedupvideo = video.fx(vfx.speedx, speed)
        output_path = f'OutputFiles/{id}.mp4'
        spedupvideo.write_videofile(output_path, codec='libx264', audio_codec='aac')
        spedupvideo.close()
    except Exception as e:
        print(f"Error speeding up video: {e}")

def mergevideos(id):
    try:
        files = os.listdir('InputFiles/')
        clips = [VideoFileClip(os.path.join('InputFiles', file_)) for file_ in files if file_.startswith(str(id))]
        if not clips:
            raise ValueError("No video files found for merging.")
        finalvideo = concatenate_videoclips(clips, method='compose')
        output_path = f'OutputFiles/{id}.mp4'
        finalvideo.write_videofile(output_path, codec='libx264', audio_codec='aac')
        finalvideo.close()
        for clip in clips:
            clip.close()
    except Exception as e:
        print(f"Error merging videos: {e}")
