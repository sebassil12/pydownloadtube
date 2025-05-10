import yt_dlp
import os
# Class to habdle downloading audio from YouTube
class Download:
    def __init__(self, output_path=None):
        self.output_path = output_path

    def download_audio(self, url, progress_hook=None):
        """
        Downloads audio from the given YouTube URL and saves it to the specified output path.
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        if progress_hook:
            ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
