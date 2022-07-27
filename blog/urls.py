import blog.views
import debug_toolbar
from django.urls import path, include
from django.conf import settings

app_name = 'blog'
urlpatterns = [
    path('', blog.views.index, name='index'),
    path('post/<slug>/', blog.views.post_detail, name="blog-post-detail"),
    path('ip/', blog.views.get_ip),
    path('create/', blog.views.create_post, name="create-post")
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]