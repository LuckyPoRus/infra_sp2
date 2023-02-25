from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Users


class UserResource(resources.ModelResource):

    class Meta:
        model = Users
        fields = (
            "id",
            "username",
            "email",
            "role",
            "bio",
            "first_name",
            "last_name",
        )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource, ]
    list_display = (
        "username",
        "email",
        "role",
        "bio",
        "first_name",
        "last_name",
    )


admin.site.register(Users, UserAdmin)
