## setup to lambda

デプロイする
```text
docker compose -f docker-compose-prod.yml build

aws ecr get-login-password --region ap-northeast-1 --profile=<プロファイル名> | docker login --username AWS --password-stdin <ECR Account Url>

docker tag python-youtube-converter-prod:latest <ECR Account Url>/python-youtube-converter-prod:latest

docker push <ECR Account Url>/python-youtube-converter-prod:latest

aws lambda update-function-code --function-name youtube-converter --image-uri <ECR Account Url>
```
---

## localで動かすために
ビルド
```shell
docker compose build
```

起動
```shell
docker compose up -d
```

コンテナに接続
```shell
docker compose exec python bash
```

コードを動かす
```shell
python main.py
```
---
