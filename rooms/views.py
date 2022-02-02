from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render

# from django_countries import countries
from . import models, forms

# Create your views here.


class HomeView(ListView):

    """ Home View Model """

    model = models.Room
    ordering = "name"
    paginate_by = 12
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

    country = req.GET.get("country")

    if country:
        form = forms.SearchForm(req.GET)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            beds = form.cleaned_data.get("beds")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if beds is not None:
                filter_args["beds__gte"] = beds

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["superhost"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity

            for facility in facilities:
                filter_args["facilities"] = facility

            print(filter_args)

            qs = models.Room.objects.filter(**filter_args).order_by("name")

            paginator = Paginator(qs, 10, orphans=5)

            page = req.GET.get("page", 1)
            rooms = paginator.get_page(page)
            return render(
                req,
                "rooms/search.html",
                {"form": form, "rooms": rooms},
            )
    else:
        form = forms.SearchForm()

    return render(
        req,
        "rooms/search.html",
        {"form": form},
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
