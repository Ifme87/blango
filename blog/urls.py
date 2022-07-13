import blog.views
import debug_toolbar
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('', blog.views.index, name='index'),
    path('post/<slug>/', blog.views.post_detail, name="blog-post-detail"),
    path("ip/", blog.views.get_ip),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]