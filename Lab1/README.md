# Lab1

## Scheduling with Crontab

- crontab -e 명령어로 crontab 편집
- `{크론탭} {파이썬} {실행파일 절대경로} >> /var/log/cron.log 2>&1`
    - `{크론탭}` : EX) `0 3 * * *`
    - `{파이썬}` : `which python` 명령어로 어떤 파이썬 환경으로 실행시킬지 등록 EX) `/home/choonsik/miniconda3/envs/test/bin/python`
    - `{실행파일 절대경로}`: EX) `/home/Pipeline/Lab1/main.py`

- `crontab -li` 명령어로 잘 등록되었는지 확인