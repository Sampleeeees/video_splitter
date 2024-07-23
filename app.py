"""Main application file."""

import os
import uuid
import streamlit as st
from video_processing import split_video, add_audio_to_video
from audio_generation import initialize_pipeline, generate_audio
from utils import create_zip_archive


def initialize_session_states():
    """Initialize session states for user."""
    if 'video_parts' not in st.session_state:
        st.session_state.video_parts = []
    if 'output_directory' not in st.session_state:
        st.session_state.output_directory = None
    if 'uploaded_video_path' not in st.session_state:
        st.session_state.uploaded_video_path = None
    if 'selected_video_part' not in st.session_state:
        st.session_state.selected_video_part = 1


def upload_video_file():
    """Upload video file from user's computer."""
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file and st.session_state.uploaded_video_path is None:
        temp_directory = "temp"
        os.makedirs(temp_directory, exist_ok=True)
        video_path = os.path.join(temp_directory, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.uploaded_video_path = video_path
    return uploaded_file


def display_video_parts():
    """Display all video parts for selection."""
    for idx, file in enumerate(st.session_state.video_parts):
        st.write(f"Part {idx + 1}: {file}")


def select_video_part_to_add_audio():
    """Select video part to add generated audio."""
    st.session_state.selected_video_part = st.selectbox(
        f"Select the part (1-{len(st.session_state.video_parts)}) to add the generated audio",
        range(1, len(st.session_state.video_parts) + 1),
        index=st.session_state.selected_video_part - 1
    )
    video_part_path = st.session_state.video_parts[st.session_state.selected_video_part - 1]
    unique_id = uuid.uuid4()
    output_video_path = os.path.join(st.session_state.output_directory, f"part_{st.session_state.selected_video_part}_{unique_id}_with_audio.mp4")
    return video_part_path, output_video_path


def main():

    # Set title and description
    st.title("Video Splitter and Audio Adder")
    st.write("This application splits a video into parts, generates audio, and adds the audio to a specific part.")

    # Run initialize and upload video
    initialize_session_states()
    uploaded_video = upload_video_file()

    # Show new fields when video is uploaded
    if uploaded_video:
        # Input number of video parts
        number_of_parts = st.number_input("Enter the number of parts to split the video into", min_value=1, step=1)

        # When click to split, then start next steps
        if st.button("Split Video"):
            st.session_state.output_directory, st.session_state.video_parts = split_video(st.session_state.uploaded_video_path, number_of_parts)
            st.write(f"Video has been split into {number_of_parts} parts and saved in the '{st.session_state.output_directory}' directory")
            display_video_parts()

        if st.session_state.video_parts:
            video_part_path, output_video_path = select_video_part_to_add_audio()

            prompt = st.text_input("Enter the prompt for audio generation")
            negative_prompt = st.text_input("Enter the negative prompt for audio generation")

            if st.button("Generate and Add Audio"):
                pipeline = initialize_pipeline()
                audio_path, spectrogram_image = generate_audio(pipeline, prompt, negative_prompt)
                st.image(spectrogram_image, caption="Generated Spectrogram")
                add_audio_to_video(video_part_path, audio_path, output_video_path)
                st.session_state.video_parts.append(output_video_path)
                st.write(f"Audio added to video part {st.session_state.selected_video_part} and saved as {output_video_path}")
                st.session_state.zip_file_name = create_zip_archive(st.session_state.video_parts)

    if 'zip_file_name' in st.session_state:
        with open(st.session_state.zip_file_name, "rb") as f:
            st.download_button("Download ZIP", f, file_name=st.session_state.zip_file_name)


if __name__ == "__main__":
    main()
