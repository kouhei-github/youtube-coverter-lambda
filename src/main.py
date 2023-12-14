import json
import os

from download import YoutubeDowonloader
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

bucket_name = 'youtube-mp3-image'

def lambda_handler(event, context):
    if __name__ == "__main__":
        body = {"url": "https://www.youtube.com/watch?v=ps-pHi81S_Q"}
    else:
        body = json.loads(event["body"])
    # pdf_file: str, google_drive_id: str, service_account_file: str
    URL_LIST = [
        body["url"],
        # Add more URLs as needed
    ]

    yd = YoutubeDowonloader()
    yd.download(URL_LIST)

    file_path = f'{yd.output_path}.mp3'

    uploaded_file_name = upload_file_to_s3(file_path, bucket_name, file_path.replace("/tmp/", ""))
    if uploaded_file_name:
        file_url = get_s3_object_url(bucket_name, uploaded_file_name)
        json_data = json.dumps({
            "file_name": file_url,
            "thumbnail": yd.thumbnail,
            "title": yd.title,
            "duration": yd.duration,
            "filesize": yd.filesize
        })
        os.remove(file_path)
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST"
            },
            'body': json_data
        }


def get_s3_object_url(bucket, object_name):
    return f"https://{bucket}.s3.amazonaws.com/{object_name}"


def upload_file_to_s3(file_name, bucket, object_name=None):
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
