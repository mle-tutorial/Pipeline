# Lab1

## Deployment (CLI)

- Lab1에서는 CLI를 통해 deployment yaml file을 생성하고 배포합니다.

- `prefect deployment build ./flow.py:flow_function -n ip-logging-pipeline -q instance1`
- 위 커맨드로 생성된 yaml파일을 수정합니다.
```yaml
parameters: {
  "name": "HelloWorld"
}
```
- `prefect deployment apply flow_function-deployment.yaml`
- `prefect deployment ls`
- `prefect deployment run My_first_pipeline/ip-logging-pipeline`
- `prefect agent start -q 'instance1'`