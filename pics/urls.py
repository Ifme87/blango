from django.urls import path
from django.urls import reverse_lazy
from . import views


urlpatterns = [
    path("", views.PicListView.as_view(), name="all"),
    path("<int:pk>/", views.PicDetailView.as_view(), name="pic_detail"),
    path(
        "create/",
        views.PicCreateView.as_view(success_url=reverse_lazy("all")),
        name="pic_create",
    ),
    path(
        "<int:pk>/update/",
        views.PicUpdateView.as_view(success_url=reverse_lazy("all")),
        name="pic_update",
    ),
    path(
        "<int:pk>/delete/",
        views.PicDeleteView.as_view(success_url=reverse_lazy("all")),
        name="pic_delete",
    ),
    path("pic_picture/<int:pk>/", views.stream_file, name="pic_picture"),
]
