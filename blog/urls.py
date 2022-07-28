from . import views
import debug_toolbar
from django.urls import path, include
from django.conf import settings

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug>/', views.post_detail, name="blog-post-detail"),
    path('ip/', views.get_ip),
    path('create/', views.create_post, name="create-post"),
    path("add_tag/", views.create_tag, name="so_tag_add"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]