from django.urls import path

from orbiter.dashboard.views import (
    CompanyDetailView,
    DashboardView,
    send_email,
    CompanyListView,
    execute_crawl_view,
)

app_name = "dashboard"


urlpatterns = [
    # send_email
    # standard views for index
    path("", DashboardView.as_view(), name="dashboard"),
    # view for all companies
    path("send-email/", send_email, name="send_email"),
    path("companies/", CompanyListView.as_view(), name="company-list"),
    # company detail view
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    # TODO implement the views for the other models
    path("run-crawling/", execute_crawl_view, name="run-crawling"),
]
