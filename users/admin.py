from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.


@admin.register(models.User)  #
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    # list_display = ("username", "language", "superhost")
    list_filter = UserAdmin.list_filter + ("superhost", "language", "currency")

    list_display = (
        "username",
        "email",
        "first_name",
        "currency",
        "superhost",
        "is_superuser",
        "email_confirmed",
        "email_secret"
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Banana", {"fields": ("avatar", "gender", "bio")}),
    )
