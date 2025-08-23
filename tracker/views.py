from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tracker.forms import CustomUserCreationForm

User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class UserRegistrationView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("tracker:index")