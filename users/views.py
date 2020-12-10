from django.shortcuts import render
from django.views import View

# Create your views here.


class LoginView(View):

    def get(self, req):
        return render(req, "users/login.html")

    def post(self, req):
        pass
