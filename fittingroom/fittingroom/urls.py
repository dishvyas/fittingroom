from django.contrib import admin
from django.urls import path, include, re_path
from users import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', views.index, name='index'),
]