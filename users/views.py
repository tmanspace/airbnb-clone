from django.shortcuts import render
from django.views import View
from . import forms

# Create your views here.


class LoginView(View):

    def get(self, req):
        form = forms.LoginForm()
        return render(req, "users/login.html", context={"form" : form})

    def post(self, req):
        pass
