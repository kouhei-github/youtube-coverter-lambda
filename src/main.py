import json
import os
import glob
from download import YoutubeDownloader
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

bucket_name = 'youtube-mp3-image'


def lambda_handler(event, context):
    """
    AWS Lambda関数のハンドラー。HTTPリクエストに応答する。

    Args:
        event (dict): Lambda関数に渡されるイベントデータ。
        context (object): 実行環境に関する情報を提供するコンテキストオブジェクト。

    Returns:
        dict: HTTPステータスコード、ヘッダー、ボディを含むレスポンスオブジェクト。
    """

    # ローカル実行かどうかを判断する
    if __name__ == "__main__":
        body = {"url": "https://www.youtube.com/watch?v=ps-pHi81S_Q"}
    else:
        # LambdaイベントからボディをJSONとして読み込む
        body = json.loads(event["body"])

    # 一時ファイルを削除するための関数を呼び出す
    _delete_tmp_file()

    # 処理するURLリスト
    URL_LIST = [
        body["url"],
        # 必要に応じてさらにURLを追加
    ]

    # YouTubeダウンローダーのインスタンスを作成
    youtube_downloader = YoutubeDownloader()
    # ファイルパスを設定
    file_path = f'{youtube_downloader.output_path}.mp3'

    # YouTubeダウンローダーを使用して動画情報を取得
    movie_info = youtube_downloader.download(URL_LIST)

    # S3にファイルをアップロードし、アップロードされたファイル名を取得
    uploaded_file_name = upload_file_to_s3(file_path, bucket_name, file_path.replace("/tmp/", ""))

    # アップロードに成功した場合
    if uploaded_file_name:
        # S3オブジェクトのURLを取得
        file_url = get_s3_object_url(bucket_name, uploaded_file_name)
        # 応答用のJSONデータを作成
        json_data = json.dumps({
            "file_name": file_url,
            "thumbnail": movie_info["thumbnail"],
            "title": movie_info["title"],
            "duration": movie_info["duration"],
            "filesize": movie_info["filesize"]
        })
        # HTTPレスポンスを返す
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST"
            },
            'body': json_data
        }


def _delete_tmp_file():
    """

    Deletes all temporary mp3 files in the specified temporary directory.

    """
    tmp_dir = "/tmp"

    # get list of mp3 files
    mp3_files = glob.glob(os.path.join(tmp_dir, "*.mp3"))
    for mp3_file in mp3_files:
        os.remove(mp3_file)

def get_s3_object_url(bucket: str, object_name: str):
    """
    Args:
        bucket (str): The name of the S3 bucket where the object is stored.
        object_name (str): The name of the object for which the URL is generated.

    Returns:
        str: The URL of the S3 object.

    """
    return f"https://{bucket}.s3.amazonaws.com/{object_name}"


def upload_file_to_s3(file_name: str, bucket: str, object_name=None):
    """
    Uploads a file to an S3 bucket.

    Args:
        file_name (str): The name of the file to upload.
        bucket (str): The name of the S3 bucket to upload the file to.
        object_name (str, optional): The name to give the object in S3. If not provided, the file name will be used.

    Returns:
        str: The name of the object in S3 that was created or updated.

    Raises:
        NoCredentialsError: If there are no credentials available to access the S3 bucket.

    """
    # ファイル名がS3のオブジェクト名として使用されない場合は、オブジェクト名を指定
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        return "Credentials not available"
    return object_name



if __name__ == "__main__":
    payload = {}
    data = lambda_handler(payload,{},)
    print(data)
