from yt_dlp import YoutubeDL
import uuid

class YoutubeDowonloader:
    def __init__(self) -> None:
        """Initialize the YoutubeDowonloader

        Args:
            url_list (list): list of urls
        """

        self.output_path = f'/tmp/{uuid.uuid4()}'
        self.ydl_opts = {
            "format": "mp3/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
            "outtmpl": self.output_path,
        }



    def download(self, url_list: list):
        """Download the given urls

        Args:
            urls (list): list of urls
        """
        with YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.download(url_list)
            print(self.ydl_opts["outtmpl"])
