from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule

from model_training import training_flow

model_train = Deployment.build_from_flow(
    flow=training_flow,
    name="model_train",
    work_queue_name="wq_model_train",
    schedule=(CronSchedule(cron="0 19 * * 1,2,3,4,5", timezone="Asia/Seoul")),
)

if __name__ == "__main__":
    model_train.apply()