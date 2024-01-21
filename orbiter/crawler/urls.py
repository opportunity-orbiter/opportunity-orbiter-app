from django.urls import path

from orbiter.crawler.views import execute_crawl_view


app_name = "crawler"


urlpatterns = [
    path("run-crawling/", execute_crawl_view, name="run-crawling"),
]
