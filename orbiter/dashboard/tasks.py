from huey import crontab
from huey.contrib.djhuey import task, db_task
import time


from orbiter.dashboard.utils.execute_crawling import execute_crawling_function


@task()
def async_task(job_portal_url):
    # Simuliert eine asynchrone Operation
    # time.sleep(5)
    print("async task start")
    json = execute_crawling_function(job_portal_url)
    print(json)
    return "Task Completed"
