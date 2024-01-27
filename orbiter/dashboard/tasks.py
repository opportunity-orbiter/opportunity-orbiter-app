from huey import crontab
from huey.contrib.djhuey import task, db_task
import time


from orbiter.dashboard.utils.execute_crawling import execute_crawling_function


@task()
def async_task():
    # Simuliert eine asynchrone Operation
    # time.sleep(5)
    json = execute_crawling_function()
    print(json)
    return "Task Completed"
