from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from newspapers.models import Newspaper, Topic, Redactor


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info", {"fields": ("years_of_experience",)}
        ),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info", {"fields": ("years_of_experience",)}
        ),
    )
    search_fields = ("years_of_experience",)
    ordering = (
        "years_of_experience",
        "username",
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "published_date", "topic")
    search_fields = ("title",)
    ordering = ("published_date",)
    list_filter = ("topic",)

