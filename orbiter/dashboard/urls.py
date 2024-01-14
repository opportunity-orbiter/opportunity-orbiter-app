from django.urls import path

from orbiter.dashboard.views import WebpageListView, send_email

app_name = "dashboard"


urlpatterns = [
    # send_email
    # standard views for index
    path("", WebpageListView.as_view(), name="index"),
    # view for all companies
    path("send-email/", send_email, name="send_email"),
    path("webpages/", WebpageListView.as_view(), name="webpage_list"),
]
