from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Friend, FriendRequest
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "name", "is_staff", "is_active",)
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ('Personal info', {'fields': ('name',)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Friend)
admin.site.register(FriendRequest)

