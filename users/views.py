from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms

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
