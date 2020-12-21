from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# Create your views here.


class LoginView(View):

    def get(self, req):
        if (req.user.username != ""):
            return redirect(reverse("core:home"))
        form = forms.LoginForm(initial={"email": "serazutdinov.tim@gmail.com"})
        return render(req, "users/login.html", context={"form" : form})

    def post(self, req):
        form = forms.LoginForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(req, username=email, password=password)
            if user is not None:
                login(req, user)
                return redirect(reverse("core:home"))
        return render(req, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Tim",
        "last_name": "Ser",
        "email": "hello@gmail.com",
        "password": "nice12Fg#",
        "password2": "nice12Fg#"
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_confirmed = True
        user.email_secret = ""
        user.save()
        # Add success message
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    pass
