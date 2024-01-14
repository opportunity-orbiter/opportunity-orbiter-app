from django.urls import path

from orbiter.dashboard.views import CompanyDetailView, send_email, CompanyListView

app_name = "dashboard"


urlpatterns = [
    # send_email
    # standard views for index
    # view for all companies
    path("send-email/", send_email, name="send_email"),
    path("companies/", CompanyListView.as_view(), name="company-list"),
    # company detail view
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
]
