from django.urls import path

from orbiter.dashboard.views import send_email

app_name = "dashboard"


urlpatterns = [
    # send_email
    # standard views for index
    # view for all companies
    path("send-email/", send_email, name="send_email"),
]
