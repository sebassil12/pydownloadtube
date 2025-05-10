import yt_dlp
import os
# Class to handle downloading audio from YouTube
class Download:
    def __init__(self, output_path=None):
        self.output_path = output_path

    def download_audio(self, url, progress_hook=None):
        """
        Downloads audio from the given YouTube URL and saves it to the specified output path.
        """

        ## !!The parameters must be put in the settings screen 
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Download flag to stop th download for the user
        if progress_hook:
            ydl_opts['progress_hooks'] = [progress_hook]
        
        # yt_dlp is a powerful library for downloading videos and audio from various platforms
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
