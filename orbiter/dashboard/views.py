from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay
from django.db.models import Count
from orbiter.dashboard.utils.execute_crawling import start_crawl_and_save
import asyncio
from .tasks import async_task

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import EmailForm, CompanyForm, JobForm, LocationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now()
        start_current_month = today.replace(day=1)
        end_last_month = start_current_month - timedelta(days=1)

        # Unternehmen
        total_count_companies = Company.objects.count()
        last_month_total_companies = Company.objects.filter(
            created_at__lte=end_last_month
        ).count()

        # Jobs
        total_count_jobs = Job.objects.count()
        last_month_total_jobs = Job.objects.filter(
            created_at__lte=end_last_month
        ).count()

        # Prozentuale Differenz für Unternehmen berechnen
        percentage_difference_companies = self.calculate_percentage_difference(
            total_count_companies, last_month_total_companies
        )

        # Prozentuale Differenz für Jobs berechnen
        percentage_difference_jobs = self.calculate_percentage_difference(
            total_count_jobs, last_month_total_jobs
        )

        # Aktuelles Datum als date-Objekt festlegen
        today = timezone.now().date()  # Verwendung von .date() hier
        thirty_days_ago = today - timedelta(days=30)

        # Jobs pro Tag für die letzten 30 Tage zählen
        jobs_per_day = (
            Job.objects.filter(created_at__date__gte=thirty_days_ago)
            .annotate(day=TruncDay("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Liste für die letzten 30 Tage initialisieren
        job_counts = [0] * 30
        for job in jobs_per_day:
            # print(job)
            day_index = (
                job["day"].date() - thirty_days_ago
            ).days  # Stellen Sie sicher, dass beide vom Typ date sind
            if 0 <= day_index < 30:
                job_counts[day_index] = job["count"]
        # TODO reparieren print(job_counts)
        # Kontext aktualisieren
        # job_creation_dates = (
        #     Job.objects.all()
        #     .order_by("created_at")
        #     .values_list("created_at", flat=True)
        # )
        # print(job_creation_dates)

        context.update(
            {
                "total_count_companies": total_count_companies,
                "last_month_total_companies": last_month_total_companies,
                "percentage_difference_companies": percentage_difference_companies,
                "total_count_jobs": total_count_jobs,
                "last_month_total_jobs": last_month_total_jobs,
                "percentage_difference_jobs": percentage_difference_jobs,
                "job_counts": job_counts,
            }
        )

        return context

    def get_queryset(self):
        return Company.objects.annotate(jobs_count=Count("jobs"))

    def calculate_percentage_difference(self, current_total, last_month_total):
        if last_month_total > 0:
            return (current_total - last_month_total) / last_month_total * 100
        return 0  # Vermeidung einer Division durch Null


# ----------Views Company ------------


class CompanyCreateView(CreateView):
    model = Company
    template_name = "company_create.html"
    context_object_name = "company"
    ordering = ["-name"]
    paginate_by = 10
    form_class = CompanyForm
    success_url = reverse_lazy(
        "dashboard:company-list"
    )  # Redirect after successful create


class CompanyListView(ListView):
    model = Company
    template_name = "company_list.html"
    context_object_name = "companies"
    ordering = ["-name"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(
            jobs_count=Count("jobs")
        )  # Hier wird 'jobs' durch den tatsächlichen Namen des Reverse-Relations-Felds von Job zu Company ersetzt


class CompanyDetailView(DetailView):
    model = Company
    template_name = "company_detail.html"
    context_object_name = "company"
    ordering = ["-name"]
    paginate_by = 10


class CompanyEditView(UpdateView):
    model = Company
    template_name = "company_edit.html"
    form_class = CompanyForm
    success_url = reverse_lazy("dashboard:company-list")


# ----------Views Location ------------


class LocationCreateView(CreateView):
    model = Location
    template_name = "location_create.html"
    context_object_name = "location"
    ordering = ["-name"]
    paginate_by = 10
    form_class = LocationForm
    success_url = reverse_lazy(
        "dashboard:location-list"
    )  # Redirect after successful create


class LocationListView(ListView):
    model = Location
    template_name = "location_list.html"
    context_object_name = "locations"
    ordering = ["-name"]
    paginate_by = 10


class LocationDetailView(DetailView):
    model = Location
    template_name = "location_detail.html"
    context_object_name = "location"
    ordering = ["-name"]
    paginate_by = 10


class LocationEditView(UpdateView):
    model = Location
    template_name = "location_edit.html"
    form_class = LocationForm
    success_url = reverse_lazy("dashboard:location-list")


# ----------Views JOBS ------------


class JobCreateView(CreateView):
    model = Job
    template_name = "job_create.html"
    form_class = JobForm
    success_url = reverse_lazy("dashboard:job-list")


class JobListView(ListView):
    model = Job
    template_name = "job_list.html"
    context_object_name = "jobs"
    ordering = ["id"]
    paginate_by = 10


class JobDetailView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"
    success_url = reverse_lazy("dashboard:job-list")


class JobEditView(UpdateView):
    model = Job
    template_name = "job_edit.html"
    form_class = JobForm
    success_url = reverse_lazy("dashboard:job-list")


def crawling(request):
    if request.method == "POST":
        job_portal_url = request.POST.get('job_portal_url')
        company_id = request.POST.get('company_id')
        print(job_portal_url)
        print(company_id )

        # Trigger the asynchronous task
        # async_task(job_portal_url)

        asyncio.run(start_crawl_and_save(job_portal_url))
        return redirect("dashboard:dashboard")

    # The code here will be executed for GET requests or if the form is not submitted
    return render(request, "crawling_template.html")
