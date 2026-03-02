from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department
from .models import Job



class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("role", "department"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("role", "department"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Job)