# NaiaRelatedWordsAPI 

특정 단어와 연관된 단어 목록 제공하기 위한 API

```shell

docker build -t [CONTAINER_REPOSITORY]:[TAG]
    --build-arg ELS_HOST="${ELS_HOST}" \
    --build-arg ELS_USER="${ELS_USER}" \
    --build-arg ELS_PASSWORD="${ELS_PASSWORD}" \
    --build-arg ELS_INDEX="${ELS_INDEX}" \
    --build-arg SUPPORT=${SUPPORT}
    .

docker run -d --name [CONTAINER_NAME] --restart=always -p 8001:8001 [CONTAINER_REPOSITORY]:[TAG]
```

 - Running
```shell
uvicorn app.main:app --reload --port=8001 --host=0.0.0.0
```
