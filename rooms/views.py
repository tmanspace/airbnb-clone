from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render
from django_countries import countries
from . import models

# Create your views here.


class HomeView(ListView):

    """ Home View Model """

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


def search(req):
    city = req.GET.get("city", "anywhere").capitalize()
    country = req.GET.get("country", "KR")
    room_type = int(req.GET.get("room_type", 0))
    price = int(req.GET.get("price", 0))
    guests = int(req.GET.get("guests", 0))
    rooms = int(req.GET.get("rooms", 0))
    baths = int(req.GET.get("baths", 0))
    beds = int(req.GET.get("beds", 0))
    bedrooms = int(req.GET.get("bedrooms", 0))
    s_amenities = req.GET.getlist("amenities", [])
    s_facilities = req.GET.getlist("facilities", [])
    superhost = req.GET.get("superhost", False)
    instant = req.GET.get("instant", False)
    print(s_amenities, s_facilities)

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "rooms": rooms,
        "baths": baths,
        "beds": beds,
        "bedrooms": bedrooms,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    # house_rules = models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        # "house_rules": house_rules,
    }

    # rooms = models.Room.objects.filter(**filter_args)

    return render(
        req,
        "rooms/search.html",
        {**form, **choices},
    )


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
