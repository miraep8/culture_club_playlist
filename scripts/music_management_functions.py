# Note - env reqs that ffmpeg be in your path
# Also note, shamelessly making use of AI here
import os
import yt_dlp
import numpy as np
import librosa

from scipy.io import wavfile
from scipy.fft import fft, fftfreq



def yt_dlp_hook(d):
    global final_filename
    if d['status'] == 'finished':
        return(d['filename'])

def extract_yt_url_to_wav(output_path, song_id, url, download):
    video_title = ""
    ydl_opts = {
            'format': 'bestaudio/best',
            'extract_audio': True,
            'audioformat': 'wav',
            'outtmpl': f"{output_path}\\{song_id}.%(ext)s",
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',
                'nopostoverwrites': False,
            }],
            'writemetadata': True,
            'embedthumbnail': False,
            'progress_hooks': [yt_dlp_hook],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if (download): ydl.download([url])
            #info_dict = ydl.extract_info(url, download=False)
            #video_title = info_dict.get('title', None)

        print(f"\nDownload complete for: {url}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    return(f"{output_path}//{song_id}.wav")


def generate_fft_from_wav(wav_file, target_length_sec=10, pad_at_start_sec = 30, target_sr=200):
    """
    Loads, resamples, trims/pads, and calculates the FFT of an audio file.
    """
    # 1. Load and resample the audio to a consistent sample rate
    # librosa.load resamples automatically if sr is specified
    y, sr = librosa.load(wav_file, sr=target_sr)

    # Calculate the target number of samples
    target_samples = int(target_length_sec * sr)
    num_samples_to_skip = min(int(pad_at_start_sec * sr), len(y) - target_samples)

    # 2. Trim or Pad the audio to the same length (number of samples)
    if len(y) > target_samples:
        # Trim the audio
        y = y[num_samples_to_skip:num_samples_to_skip+target_samples]
    elif len(y) < target_samples:
        # Pad with zeros
        padding = np.zeros(target_samples - len(y))
        y = np.concatenate((y, padding))

    # Ensure the length is exactly the target samples (important for consistent FFT input)
    # This might be slightly different due to floating point numbers, but the above
    # logic should make them consistent for practical purposes.
    # Or, you can use numpy.fft.fft(y, n=target_samples) for direct padding/cropping.

    # 3. Apply a window function (optional but recommended to reduce spectral leakage)
    y = y * np.hanning(len(y))

    # 4. Calculate the FFT
    # The output length of the FFT will be the same as the input length 'n'
    fft_result = np.fft.fft(y)

    # Get the magnitude spectrum (absolute values)
    magnitude_spectrum = np.abs(fft_result)

    # Frequencies corresponding to the FFT bins
    freqs = np.fft.fftfreq(len(y), 1/sr)

    # The spectrum is symmetric, so only consider the first half (positive frequencies)
    half_length = len(magnitude_spectrum) // 2
    magnitude_spectrum = magnitude_spectrum[:half_length]
    freqs = freqs[:half_length]
    print(len(magnitude_spectrum))

    return magnitude_spectrum, freqs

