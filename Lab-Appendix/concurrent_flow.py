import time
from prefect import flow, task, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner

@task(name="Download")
def download(name):
    time.sleep(5)
    return f"Download {name}"

@flow(name="Extract", task_runner=ConcurrentTaskRunner)
def extract():
    temp_list = []
    for name in ["A", "B", "C", "D"]:
        temp = download.submit(name)
        temp_list.append(temp)
    temp_list = [temp.result() for temp in temp_list]
    return temp_list

if __name__ == "__main__":
    final_list = extract()
    with open("./concurrent.txt", 'w+') as file:
        file.write('\n'.join(final_list)) 