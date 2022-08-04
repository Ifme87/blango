from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("slug", "published_at", "id")


# Register your models here.

admin.site.register(Tag)
admin.site.register(
    Post, PostAdmin
)  # PostAdmin here customize Post class view in /admin
admin.site.register(Comment)
admin.site.register(AuthorProfile)
