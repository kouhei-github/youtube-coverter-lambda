FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# xzユーティリティのインストール
RUN yum install -y xz

RUN yum install tar -y

# ffmpegのバイナリをダウンロード
RUN curl -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xJf ffmpeg.tar.xz --strip-components=1 \
    && cp ffmpeg ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg.tar.xz ffmpeg ffprobe

# pipのアップデート
RUN pip install --upgrade pip

# pipでインストールしたいモジュールをrequirements.txtに記述しておいて、
# コンテナ内でpipにインストールさせる
# requirements.txtの書き方は[pip freeze]コマンドから参考に出来る
COPY ./container/requirements.txt ${LAMBDA_TASK_ROOT}
# アプリケーションコードをコンテナにコピー
COPY ./src ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt


CMD [ "main.lambda_handler" ]
