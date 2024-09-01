from django.urls import re_path
from django.contrib.auth.views import LogoutView, LoginView
from .views import UserCreateView
from . import views

urlpatterns = [
    # re_path(r'^$', views.index, name='index'),
    re_path(r'^logout/$', LogoutView.as_view(), name="logout"),  # Logout URL
    re_path(r'^login/$', LoginView.as_view(template_name='fittingroom/login.html'), name="login"),  # Login URL
    re_path(r'^register/$', UserCreateView.as_view(), name="register"),  # Register URL
    re_path('image/', views.image_view, name='image'),
]