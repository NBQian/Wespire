from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView



urlpatterns = [
	path('auth/', include('djoser.urls')),
	path('auth/', include('djoser.urls.jwt')),
    path("admin/", admin.site.urls),
    path('', include('students.urls')),
]