from django.urls import path

from orbiter.laboratory.views import WebpageListView, send_email

app_name = "laboratory"


urlpatterns = [
    # send_email
    path("send-email/", send_email, name="send_email"),
    path("webpages/", WebpageListView.as_view(), name="webpage_list"),
]
