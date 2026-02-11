# Note - env reqs
import os
import yt_dlp
import argparse

def extract_yt_url_to_wav(output_path, url):

    ydl_opts = {
            'format': 'bestaudio/best',  # select the best audio format
            'extract_audio': True,      # Tell yt-dlp to extract the audio
            'audioformat': 'wav',       # Preferred audio format (requires FFmpeg)
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'), # output file name template
            'noplaylist': True,          # download only the single video, not a playlist
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0', # '0' specifies the best quality
                'nopostoverwrites': False,
            }],
            'writemetadata': True, # Optional: embeds metadata
            'embedthumbnail': False, # Optional: embeds thumbnail
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\nDownload complete for: {url}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Download_YT_files_as_wav',
                    description='Takes a Youtube Url and downloads then converts to .wav format',
                    epilog='Requires access to FFmpeg in your PATH variable')
    parser.add_argument('url')
    parser.add_argument('output_dir')
    args = parser.parse_args()
    extract_yt_url_to_wav(
        args.output_dir,
        args.url)
