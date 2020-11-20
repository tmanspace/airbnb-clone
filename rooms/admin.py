from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" height="100px" />')

    get_thumbnail.short_description = "Thumbnail"


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "adress", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "baths", "beds", "bedrooms")},
        ),
        (
            "More about Spaces",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Host", {"fields": ["host"]}),
    )

    ordering = ("name",)

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "baths",
        "beds",
        "bedrooms",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )
    search_fields = ("^city", "host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    raw_id_fields = ("host",)

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()
