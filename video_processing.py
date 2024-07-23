"""Video processing."""

import os
import uuid
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip


def split_video(input_path, n_parts):
    """
    Split the video.

    :param input_path: input video path.
    :param n_parts: number of parts for splitting.
    """
    video = VideoFileClip(input_path)
    duration = video.duration
    part_duration = duration / n_parts

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = []
    for i in range(n_parts):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration
        unique_id = uuid.uuid4()
        output_path = os.path.join(output_dir, f"part_{i + 1}_{unique_id}.mp4")

        subclip = video.subclip(start_time, end_time)
        subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        generated_files.append(output_path)

    return output_dir, generated_files


def add_audio_to_video(video_path, audio_path, output_path):
    """
    Add audio file to video.

    :param video_path: path to video.
    :param audio_path: path to audio.
    :param output_path: path to output video.
    """
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    new_video = video.set_audio(audio)
    new_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
