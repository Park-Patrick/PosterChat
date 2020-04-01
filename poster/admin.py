from django.contrib import admin
from .models import Poster, Comment, Conference


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PosterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Details",          {"fields": ["title", "subtitle", "description"]}),
        ("Image",            {"fields": ["image"]}),
        ("Date information", {"fields": ["created_on"]}),
    ]
    inlines = [CommentInline]


class PosterInline(admin.TabularInline):
    model = Poster
    extra = 3


class ConferenceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "institution", "description"]}),
        ("Users", {"fields": ["organizers", "attendees", "guests"]}),
    ]
    inlines = [PosterInline]


admin.site.register(Conference, ConferenceAdmin)
