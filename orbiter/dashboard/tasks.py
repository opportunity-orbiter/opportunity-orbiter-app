from huey import crontab
from huey.contrib.djhuey import task, db_task
import time
import asyncio


from orbiter.dashboard.utils.execute_crawling import start_crawl_and_save


@task()
async def async_task(job_portal_url):
    # Simuliert eine asynchrone Operation
    # time.sleep(5)
    print("async task start")
    asyncio.run(start_crawl_and_save())
        

    return "Task Completed"
