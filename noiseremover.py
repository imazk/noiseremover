from moviepy import VideoFileClip
from scipy.io import wavfile
import noisereduce as nr
import subprocess
import os

# Extract audio from video
def extract_audio(input_video, output_audio, fps=16000, bitrate='96k', nbytes=2):
    videoclip = VideoFileClip(input_video)
    videoclip.audio.write_audiofile(output_audio, fps=fps, bitrate=bitrate, nbytes=nbytes)

# Remove noise from audio
def remove_noise(input_audio, output_audio):
    rate, data = wavfile.read(input_audio)
    if len(data.shape) > 1:  # Ensure mono audio
        data = data[:, 0]
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(output_audio, rate, reduced_noise)

# Merge audio and video using ffmpeg
def merge_audio_video(input_video, input_audio, output_video, audio_bitrate='96k'):
    subprocess.call([
        'ffmpeg',
        '-i', input_video,
        '-i', input_audio,
        '-map', '0:v',
        '-map', '1:a',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', audio_bitrate,
        '-shortest',
        '-y',
        output_video
    ])

# Clean up temporary files
def cleanup(*files):
    for file in files:
        os.remove(file)

if __name__ == "__main__":
    input_video = "noisyvideo.mp4"
    extracted_audio = "ExtractedAudio.wav"
    noise_reduced_audio = "nfaudio.wav"
    output_video = "nfvideo.mp4"

    # Step 1: Extract audio from video
    extract_audio(input_video, extracted_audio)

    # Step 2: Remove noise from extracted audio
    remove_noise(extracted_audio, noise_reduced_audio)

    # Step 3: Merge noise-reduced audio back with original video
    merge_audio_video(input_video, noise_reduced_audio, output_video)

    # Step 4: Clean up temporary audio files
    cleanup(extracted_audio, noise_reduced_audio)

    print("Successfully removed noise and merged audio with video")
