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
from .utils.execute_crawling import execute_crawling_function


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

# ----------Views Company ------------  

class CompanyCreateView(CreateView):
    model = Company
    template_name = "company_create.html"
    context_object_name = "company"
    ordering = ["-name"]
    paginate_by = 10
    form_class = CompanyForm
    success_url = reverse_lazy('dashboard:company-list')  # Redirect after successful create    

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

class CompanyEditView(DetailView):
    model = Company
    template_name = "company_list.html"
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CompanyForm(instance=self.object)
        return context

# ----------Views Location ------------  


class LocationCreateView(CreateView):
    model = Location
    template_name = "location_create.html"
    context_object_name = "location"
    ordering = ["-name"]
    paginate_by = 10
    form_class = LocationForm
    success_url = reverse_lazy('dashboard:location-list')  # Redirect after successful create    

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

class LocationEditView(DetailView):
    model = Location
    template_name = "location_list.html"
    context_object_name = "location"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LocationForm(instance=self.object)
        return context

# ----------Views JOBS ------------   

class JobCreateView(CreateView):
    model = Job
    template_name = "job_create.html"
    form_class = JobForm
    success_url = reverse_lazy('dashboard:job-list')    

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
    success_url = reverse_lazy('dashboard:job-list') 

class JobEditView(UpdateView):
    model = Job
    template_name = "job_edit.html"
    form_class = JobForm
    success_url = reverse_lazy('dashboard:job-list')
    



def execute_crawl_view(request):
    execute_crawling_function()
    return HttpResponse("Crawling script executed.")

# def open_company_form_create(request):



# def open_company_form_edit(request):



# TODO Delete, Edit and insert manually views
# create basic views for deleting jobs/company/other from database, editing existing jobs/company/other from list and a view to insert into database
