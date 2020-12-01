from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render
from . import models

# Create your views here.


class HomeView(ListView):

    model = models.Room
    ordering = "name"
    paginate_by = 10
    context_object_name = "rooms"
    template_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


""" PAGINATOR """

# def all_rooms(req):
#     page = req.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(
#             req,
#             template_name="rooms/home.html",
#             context={"page": rooms},
#         )
#     except EmptyPage:
#         return redirect("/")
