import yt_dlp
import os
class Download:
    def __init__(self, output_path=None):
        if output_path is None:
            potential_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            if os.path.exists(potential_path):
                self.output_path = potential_path
            else:
                self.output_path = './'
        self.output_path = output_path
        
    def download_audio(self, url) :
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

if __name__ == '__main__':
    url = input("Introduce la URL del video de YouTube: ")
    downloader = Download()
    downloader.download_audio(url)
    print("Descarga completada.")
