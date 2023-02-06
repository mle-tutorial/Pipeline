# Lab2

## Deployment (CLI)

- Lab2에서는 CLI를 통해 deployment yaml file을 생성하고 배포합니다.

- `prefect deployment build ./flow.py:ETL -n stock-pipeline -q queue1` 으로 yaml파일을 생성합니다.
- 위 커맨드로 생성된 yaml파일의 parameters 부분을 수정합니다.
```yaml
parameters: {
  "name": "Choonsik"
}
```

- `prefect deployment apply ETL-deployment.yaml`
- `prefect deployment ls`
- `prefect deployment run ETL/stock-pipeline`
- `prefect agent start -q 'queue1'`

## Prefect Web

- `prefect orion start` 명령어로 Prefect  Web UI를 확인할수 있도록 Prefect를 실행시킵니다.