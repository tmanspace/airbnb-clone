import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from django.contrib import messages
from django.template import RequestContext

# Create your views here.


class LoginView(View):
    def get(self, req):
        if req.user.username != "":
            return redirect(reverse("core:home"))
        form = forms.LoginForm(initial={"email": "serazutdinov.tim@gmail.com"})
        return render(req, "users/login.html", context={"form": form})

    def post(self, req):
        form = forms.LoginForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(req, username=email, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, f"Welcome back, {user.first_name}")
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
        "password1": "nice12Fg#",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password1)
        if user is not None:
            login(self.request, user)
        # user.verify_email()
        request_context = RequestContext(self.request)
        request_context.push({"my_user": user})
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
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            client_id = os.environ.get("GH_ID")
            client_secret = os.environ.get("GH_SECRET")
            request_gh = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = request_gh.json()
            error = result_json.get("error", None)  # If error from GH
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                api_req = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile = api_req.json()
                username = profile.get("login", None)
                if username is not None:
                    name = profile.get("name", None)
                    email = profile.get("email", None)
                    bio = profile.get("bio", "")
                    if name is None or email is None:
                        print("name or email are none")
                        raise GithubException
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method == models.User.LOGIN_GH:
                            # Trying log in through GH
                            login(request, user)
                        else:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        new_user = models.User.objects.create(
                            username=email,
                            bio=bio,
                            email=email,
                            first_name=name,
                            login_method=models.User.LOGIN_GH,
                        )
                        new_user.set_unusable_password()
                        new_user.save()
                        login(request, new_user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))


class ProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"
