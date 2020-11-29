from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models

# Create your views here.


def all_rooms(req):
    page = req.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))
        return render(
            req,
            template_name="rooms/home.html",
            context={"page": rooms},
        )
    except EmptyPage:
        return redirect("/")
