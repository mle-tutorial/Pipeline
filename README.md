# Pipeline

## 환경

- `pip install -r requirements.txt` 로 prefect를 설치합니다.
- Database 실습에서 실행시킨 postgresql이 잘 실행되어 있는지 확인합니다.
- [Prefect Cloud 설정](https://docs.google.com/presentation/d/1gxGZ7YcWjlNO1HAczCoxAq8Aqk1MjBT50lrl99yEpQg/edit#slide=id.g1f3522884c7_0_50)을 참고하여 Cloud 설정을 하였는지 확인합니다.
- `bash prefect_database_setting.sh` 명령어로 prefect의 database로 postgresql을 사용하도록 합니다. 이후 `prefect orion start` 명령어로 로컬 환경에서 진행하셔도 괜찮습니다.

## 실습

- [Lab1](Lab1/README.md) : Database실습내용을 Crontab으로 자동화하기
- [Lab2](Lab2/README.md) : Prefect CLI로 deployment생성하기 Tutorial
- [Lab3](Lab3/README.md) : Python으로 deployment생성하기
- [Lab-Appendix](Lab-Appendix/README.md) : ConcurrentTaskFlow실습하기
- Slack Notification 자료를 참고하여 Notification 추가해보기
## Google Slide

- [Week6 슬라이드 자료](https://docs.google.com/presentation/d/15GUK2pxZF3qplmEg1yQEcr-mDFd6Fu7u-HeBIZmcx8A/edit#slide=id.g1c1aa30d9c5_0_56)
- [Slack Notification](https://docs.google.com/presentation/d/1FjiKFiQPKtuHeesaJS36i5ENtdwSKDVjH-DgcCJvoPY/edit#slide=id.p)
- [Prefect Cloud 설정](https://docs.google.com/presentation/d/1gxGZ7YcWjlNO1HAczCoxAq8Aqk1MjBT50lrl99yEpQg/edit#slide=id.g1f3522884c7_0_50)

<br>

# 참고자료
[개발환경 세팅하기(windows)](https://docs.google.com/presentation/d/1SE6P9tg3AGanryelHhF7qJ2hgwrOXZm8Q46O_7nXD6U/edit?usp=sharing)  
[개발환경 세팅하기(mac)](https://docs.google.com/presentation/d/1IbSSqU9mgfRvR511I_2zpWQVKgLyoiBhWu42mKWayWw/edit?usp=sharing)
