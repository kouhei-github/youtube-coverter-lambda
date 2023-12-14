from yt_dlp import YoutubeDL
from typing import List
import uuid

class YoutubeDownloader:
    """
    YoutubeDownloader

        This class provides a way to download videos from YouTube using the YoutubeDL library. It initializes the object with default values for the options of YoutubeDL.

    Methods:

        __init__(self)
            Initializes the object with default values for ydl_opts.

        download(self, url_list: List[str])
            Downloads the videos from the specified URLs and returns information about the downloaded video.

            Args:
                url_list (List[str]): A list of URLs that need to be downloaded.

            Returns:
                dict: A dictionary containing information about the downloaded video. The dictionary has the following keys:
                    - "title": The title of the video, or None if the title is not available.
                    - "thumbnail": The URL of the video thumbnail, or None if the thumbnail is not available.
                    - "duration": The duration of the video in seconds, or None if the duration is not available.
                    - "filesize": The size of the video file in bytes, or None if the filesize is not available.
    """
    output_path = f'/tmp/{uuid.uuid4()}'
    def __init__(self) -> None:
        """
        Initializes the object with default values for ydl_opts.
        """
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

    def download(self, url_list: List[str]):
        """
        Args:
            url_list (List[str]): A list of URLs that need to be downloaded.

        Returns:
            dict: A dictionary containing information about the downloaded video. The dictionary has the following keys:
                - "title": The title of the video, or None if the title is not available.
                - "thumbnail": The URL of the video thumbnail, or None if the thumbnail is not available.
                - "duration": The duration of the video in seconds, or None if the duration is not available.
                - "filesize": The size of the video file in bytes, or None if the filesize is not available.
        """
        with YoutubeDL(self.ydl_opts) as ydl:
            _ = ydl.download(url_list)
            info_dict = ydl.extract_info(url_list[0], download=False)
            return {
                "title": info_dict.get('title', None),
                "thumbnail": info_dict.get('thumbnail', None),
                "duration": info_dict.get('duration', None),
                "filesize": info_dict.get('filesize', None)
            }
