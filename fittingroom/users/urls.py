from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import logout_then_login
from django.views.generic import TemplateView
from .views import UserCreateView

urlpatterns = [
    url(r'^register', UserCreateView.as_view(),name="register"),
    url(r'^logout', logout_then_login, name="logout"),
    url(r'^login', UserCreateView.as_view(), name="login")
]