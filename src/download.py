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
        self.thumbnail = ""
        self.title = ""
        self.duration = ""
        self.filesize = ""



    def download(self, url_list: list):
        """Download the given urls

        Args:
            urls (list): list of urls
        """
        with YoutubeDL(self.ydl_opts) as ydl:
            _ = ydl.download(url_list)
            info_dict = ydl.extract_info(url_list[0], download=False)
            self.title = info_dict.get('title', None)
            self.thumbnail = info_dict.get('thumbnail', None)
            self.duration = info_dict.get('duration', None)
            self.filesize = info_dict.get('filesize', None)
