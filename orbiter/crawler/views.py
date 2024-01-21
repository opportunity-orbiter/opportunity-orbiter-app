from django.http import HttpResponse
from django.shortcuts import render

from orbiter.crawler.utils.execute_crawling import execute_crawling_function


# Create your views here.
def execute_crawl_view(request):
    execute_crawling_function()
    return HttpResponse("Crawling script executed.")
