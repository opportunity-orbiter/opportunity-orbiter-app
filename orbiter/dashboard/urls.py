from django.urls import path

from orbiter.dashboard.views import (
    DashboardView,
    crawling,
    send_email,
    JobCreateView,
    JobListView,
    JobDetailView,
    JobEditView,
    CompanyCreateView,
    CompanyListView,
    CompanyDetailView,
    CompanyEditView,
    LocationCreateView,
    LocationListView,
    LocationDetailView,
    LocationEditView,
)

app_name = "dashboard"


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("send-email/", send_email, name="send_email"),
    path("companies/new/", CompanyCreateView.as_view(), name="company-create"),
    path("companies/", CompanyListView.as_view(), name="company-list"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("companies/<int:pk>/edit/", CompanyEditView.as_view(), name="company-edit"),
    path("jobs/new/", JobCreateView.as_view(), name="job-create"),
    path("jobs/", JobListView.as_view(), name="job-list"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("jobs/<int:pk>/edit/", JobEditView.as_view(), name="job-edit"),
    path("locations/new", LocationCreateView.as_view(), name="location-create"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("location/<int:pk>/edit", LocationEditView.as_view(), name="location-edit"),

    path("crawling/", crawling, name="crawling"),

]
