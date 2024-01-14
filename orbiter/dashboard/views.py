from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import EmailForm
from .models import Company, Location, Job


def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            send_mail(
                "Subject here",
                "Here is the message.",
                "hey@opportunity-orbiter.com",
                ["quirin.koch@gmail.com"],
                fail_silently=False,
            )

            return redirect("index")  # Redirect after sending
    else:
        form = EmailForm()

    return render(request, "email_form.html", {"form": form})


class DashboardView(ListView):
    model = Company
    template_name = "dashboard.html"
    context_object_name = "companies"
    ordering = ["-name"]
    paginate_by = 10


class CompanyListView(ListView):
    model = Company
    template_name = "company_list.html"
    context_object_name = "companies"
    ordering = ["-name"]
    paginate_by = 10


class CompanyDetailView(DetailView):
    model = Company
    template_name = "company_detail.html"
    context_object_name = "company"
    ordering = ["-name"]
    paginate_by = 10


class CompanyCreateView(CreateView):
    model = Company
    template_name = "company_create.html"
    context_object_name = "company"
    ordering = ["-name"]
    paginate_by = 10


class LocationListView(ListView):
    model = Location
    template_name = "location_list.html"
    context_object_name = "locations"
    ordering = ["-name"]
    paginate_by = 10


class JobListView(ListView):
    model = Job
    template_name = "job_list.html"
    context_object_name = "jobs"
    ordering = ["-name"]
    paginate_by = 10


class JobDetailView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"
    ordering = ["-name"]
    paginate_by = 10


# TODO Delete und edit views
