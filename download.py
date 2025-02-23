import yt_dlp
import os
class Download:
    def __init__(self, output_path=None):
        if output_path is None:
            output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.output_path = output_path
       
    def download_audio(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

