from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from blog.api.views import (
    #PostList, 
    #PostDetail, 
    UserDetail,
    TagViewSet,
    PostViewSet,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os

#viewsets and routers
router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("posts", PostViewSet),

#Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/",
    public=True,
)

urlpatterns = [
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]

#DRF auth with cookie
#for TokenAuthentication
urlpatterns += [                    
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    #reg exp paths for Swagger UI
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    #path for viewset, router
    path("", include(router.urls)),
    #URL-based filtering
    path(
        "posts/by-time/<str:period_name>/",
        PostViewSet.as_view({"get": "list"}),
        name="posts-by-time",
    ),
]

#to be able to retrieve json with '.json' suffix in url
#urlpatterns = format_suffix_patterns(urlpatterns) 