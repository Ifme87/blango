"""blango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import blango_auth.views
from django.contrib import admin
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from django.contrib.auth.views import LogoutView
from blango_auth.forms import BlangoRegistrationForm
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),                                 #Django Allauth for OAuth ID
    path("accounts/profile/", blango_auth.views.profile, name="profile"),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=BlangoRegistrationForm),
        name="django_registration_register",                                    #Django registration
    ),
    path("accounts/logout", LogoutView.as_view(next_page='index'), name='logout'),
    path("accounts/", include("django_registration.backends.activation.urls")), #include the two step activation URLs

    path('', views.index, name='index'),
    path('questions/', include("polls.urls"), name='questions'),
    path('pic/', include("pics.urls"), name='all'),
    path('blog/', include('blog.urls'), name='blog'),
]
