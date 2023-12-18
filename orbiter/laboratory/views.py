from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from .forms import EmailForm
from .models import Webpage


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


class WebpageListView(ListView):
    model = Webpage
    template_name = "webpage_list.html"
    context_object_name = "webpages"
    ordering = ["-date"]
    paginate_by = 10
