from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AdminAddUserForm, AdminUpdateUserForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = AdminUpdateUserForm
    add_form = AdminAddUserForm

    list_display = ("email", "first_name", "last_name", "is_staff")

    list_filter = ("is_staff",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permission", {"fields": ("is_active", "is_staff")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide", ),
                "fields": (
                    "email", "first_name", "last_name", "password1", "password2",
                )
            }
        )
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "first_name", "last_name")

    filter_horizontal = ()


admin.site.register(User)
